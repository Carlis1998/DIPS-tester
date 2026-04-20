#!/usr/bin/env python3
"""
DIPS - V2 NotebookLM Audio Generator
====================================
Runs DIPS NotebookLM audio generations in a TOGAF-style CLI.

Usage:
    python run_v2.py --lang en --slow
    python run_v2.py --lang es
    python run_v2.py --lang en --lessons N01 N02
    python run_v2.py --dry-run --lang en
    python run_v2.py --status --lang en
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT_STR = str(PROJECT_ROOT)
PREFERRED_PYTHON = Path('/Users/carlake/.pyenv/versions/3.11.9/bin/python3')
if os.environ.get('DIPS_RUN_V2_BOOTSTRAPPED') != '1' and PREFERRED_PYTHON.exists() and Path(sys.executable) != PREFERRED_PYTHON:
    env = os.environ.copy()
    env['DIPS_RUN_V2_BOOTSTRAPPED'] = '1'
    os.execve(str(PREFERRED_PYTHON), [str(PREFERRED_PYTHON), __file__, *sys.argv[1:]], env)

if PROJECT_ROOT_STR in sys.path:
    sys.path.remove(PROJECT_ROOT_STR)

from notebooklm import NotebookLMClient
from notebooklm.types import AudioFormat, AudioLength

sys.path.insert(0, PROJECT_ROOT_STR)

OUT_ROOT = PROJECT_ROOT / 'out' / 'notebooklm'
OUT_LOG = OUT_ROOT / 'logs'
OUT_LOG.mkdir(parents=True, exist_ok=True)

NOTEBOOK_NAME_TEMPLATE = 'DIPS Audio Course ({lang_upper})'
SUPPORTED_LANGUAGES = ['en', 'es']
MIN_AUDIO_SIZE_BYTES = 50_000
GENERATION_TIMEOUT = 4200.0
SOURCE_UPLOAD_TIMEOUT = 180.0
INTER_START_DELAY = 20
INTER_START_DELAY_SLOW = 90
START_RETRY_ATTEMPTS = 4
START_RETRY_DELAY = 45
RATE_LIMIT_RETRY_DELAYS = [180, 300, 600, 900]

RESOURCE_HINTS = {
    'eu_treaty_teu': {
        'title': 'Treaty on European Union (TEU)',
        'url': 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:12012M/TXT',
        'note': 'Use URL fallback because the local fetch may be missing or invalid.'
    },
    'res_qa_placeholder': {
        'title': 'European Commission / Consilium / SIEPS packet',
        'url': 'https://commission.europa.eu/about/organisation/college-commissioners_en',
        'note': 'Supplement with Consilium and SIEPS pages where useful.'
    },
}

UPLOADABLE_FILE_SUFFIXES = {'.pdf', '.txt', '.md', '.docx'}


def _load_prompts(lang: str):
    if lang == 'en':
        from prompts.dips_notebooklm_en import full_prompt_en, NOTEBOOK_CARDS_EN, SOURCE_IDS_FOR_NOTEBOOK
        return full_prompt_en, NOTEBOOK_CARDS_EN, SOURCE_IDS_FOR_NOTEBOOK
    if lang == 'es':
        from prompts.dips_notebooklm_es import full_prompt_es, NOTEBOOK_CARDS_ES, SOURCE_IDS_FOR_NOTEBOOK
        return full_prompt_es, NOTEBOOK_CARDS_ES, SOURCE_IDS_FOR_NOTEBOOK
    raise SystemExit(f"Unsupported language: {lang}")


def notebook_name(lang: str, code: str) -> str:
    return f"{NOTEBOOK_NAME_TEMPLATE.format(lang_upper=lang.upper())} - {code}"


def out_dir(lang: str) -> Path:
    d = OUT_ROOT / lang.upper() / 'audio'
    d.mkdir(parents=True, exist_ok=True)
    return d


def raw_path_for(code: str, lang: str) -> Path:
    return out_dir(lang) / f'DIPS_{code}_{lang}.mp4'


def should_skip(code: str, lang: str) -> bool:
    out = raw_path_for(code, lang)
    return out.exists() and out.stat().st_size > MIN_AUDIO_SIZE_BYTES


def log_event(event: dict, lang: str):
    event['_ts_iso'] = datetime.now(timezone.utc).isoformat()
    event['lang'] = lang
    ts = datetime.now(timezone.utc).strftime('%Y%m%d')
    path = OUT_LOG / f'dips_audio_{lang}_{ts}.jsonl'
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False) + chr(10))


def load_source_index() -> dict[str, dict]:
    entries = json.loads((PROJECT_ROOT / 'data' / 'source_index.json').read_text(encoding='utf-8'))
    return {item['id']: item for item in entries}


def resolve_source_specs(code: str, source_ids_for_notebook: dict, source_map: dict) -> tuple[list[dict], list[str]]:
    specs: list[dict] = []
    warnings: list[str] = []
    for sid in source_ids_for_notebook.get(code, []):
        src = source_map.get(sid)
        if src is None:
            src = RESOURCE_HINTS.get(sid)
        if not src:
            warnings.append(f'{code}: source id {sid} not found')
            continue

        title = src.get('title', sid)
        url = src.get('url')
        local_rel = src.get('local_path')
        local_path = PROJECT_ROOT / local_rel if local_rel else None

        if local_path and local_path.exists() and local_path.suffix.lower() in UPLOADABLE_FILE_SUFFIXES:
            specs.append({'id': sid, 'mode': 'file', 'title': title, 'path': local_path})
            continue

        if url:
            specs.append({'id': sid, 'mode': 'url', 'title': title, 'url': url})
            continue

        if local_path and local_path.exists():
            warnings.append(f'{code}: local file exists but is not uploadable, using neither file nor URL: {local_path.name}')
        else:
            warnings.append(f'{code}: missing local source and no usable URL for {sid}')
    return specs, warnings


def validate_setup(codes: list[str], lang: str, full_prompt_fn, cards: dict, source_ids_for_notebook: dict, source_map: dict):
    print('Validating setup...')
    errors = []
    for code in codes:
        if code not in cards:
            errors.append(f'Unknown notebook code: {code}')
            continue
        prompt = full_prompt_fn(code)
        if len(prompt) < 200:
            errors.append(f'Prompt too short for {code}')
        specs, warnings = resolve_source_specs(code, source_ids_for_notebook, source_map)
        if not specs:
            errors.append(f'No usable sources resolved for {code}')
        for w in warnings:
            print('  WARNING:', w)
    if errors:
        print('Validation failed:')
        for err in errors:
            print('  -', err)
        sys.exit(1)
    print(f'All {len(codes)} notebooks validated.')


async def find_or_create_notebook(client: NotebookLMClient, name: str):
    for nb in await client.notebooks.list():
        if nb.title == name:
            return nb
    return await client.notebooks.create(name)


async def ensure_sources(client: NotebookLMClient, notebook_id: str, code: str, source_ids_for_notebook: dict, source_map: dict) -> list[str]:
    existing = await client.sources.list(notebook_id)
    ready = [s for s in existing if getattr(s, 'is_ready', False)]
    specs, warnings = resolve_source_specs(code, source_ids_for_notebook, source_map)
    for w in warnings:
        print('  WARNING:', w)

    uploaded_ids: list[str] = []

    def _match_existing(spec: dict):
        if spec['mode'] == 'file':
            names = {spec['title'], spec['path'].name}
            for src in ready:
                if getattr(src, 'title', None) in names:
                    return src
        else:
            for src in ready:
                if getattr(src, 'url', None) == spec['url']:
                    return src
            for src in ready:
                if getattr(src, 'title', None) == spec['title']:
                    return src
        return None

    for spec in specs:
        existing_src = _match_existing(spec)
        if existing_src:
            uploaded_ids.append(existing_src.id)
            continue

        if spec['mode'] == 'file':
            print(f"  Uploading file: {spec['path'].name}")
            src = await client.sources.add_file(notebook_id, spec['path'], wait=True, wait_timeout=SOURCE_UPLOAD_TIMEOUT)
        else:
            print(f"  Adding URL: {spec['url']}")
            src = await client.sources.add_url(notebook_id, spec['url'], wait=True, wait_timeout=SOURCE_UPLOAD_TIMEOUT)
        uploaded_ids.append(src.id)

    return uploaded_ids


async def start_generation(client: NotebookLMClient, notebook_id: str, code: str, prompt: str, source_ids: list[str], lang: str, notebook_label: str) -> str | None:
    last_error = None
    for attempt in range(1, START_RETRY_ATTEMPTS + 1):
        try:
            status = await client.artifacts.generate_audio(
                notebook_id,
                source_ids=source_ids,
                language=lang,
                instructions=prompt,
                audio_format=AudioFormat.DEEP_DIVE,
                audio_length=AudioLength.DEFAULT,
            )
            if status.task_id:
                log_event({'lesson': code, 'status': 'started', 'task_id': status.task_id, 'notebook_id': notebook_id, 'notebook_name': notebook_label}, lang)
                return status.task_id
            if status.error:
                raise RuntimeError(status.error)
            raise RuntimeError('Empty task_id returned')
        except Exception as e:
            last_error = repr(e)
            lower = str(e).lower()
            is_rate = 'rate limit' in lower or 'quota' in lower or 'empty task_id' in lower
            print(f'  [retry] {code} attempt {attempt}/{START_RETRY_ATTEMPTS}: {e}')
            if attempt < START_RETRY_ATTEMPTS:
                delay = RATE_LIMIT_RETRY_DELAYS[min(attempt - 1, len(RATE_LIMIT_RETRY_DELAYS) - 1)] if is_rate else START_RETRY_DELAY
                print(f'          waiting {delay}s before retry...')
                await asyncio.sleep(delay)
    log_event({'lesson': code, 'status': 'start_failed', 'error': last_error, 'notebook_id': notebook_id, 'notebook_name': notebook_label}, lang)
    return None


async def wait_and_download(client: NotebookLMClient, notebook_id: str, task_id: str, code: str, lang: str, title: str):
    out_path = raw_path_for(code, lang)
    try:
        final = await client.artifacts.wait_for_completion(notebook_id, task_id, timeout=GENERATION_TIMEOUT)
        if final.is_complete:
            await client.artifacts.download_audio(notebook_id, str(out_path), artifact_id=task_id)
            if out_path.exists() and out_path.stat().st_size > MIN_AUDIO_SIZE_BYTES:
                size_mb = out_path.stat().st_size / (1024 * 1024)
                try:
                    await client.artifacts.rename(notebook_id, task_id, f'{code} - {title}')
                except Exception:
                    pass
                print(f'  DONE {code} ({size_mb:.1f} MB)')
                log_event({'lesson': code, 'status': 'ok', 'size_mb': size_mb, 'artifact_id': task_id}, lang)
                return
            print(f'  WARNING {code}: downloaded file too small')
            log_event({'lesson': code, 'status': 'file_too_small', 'artifact_id': task_id}, lang)
            return
        if final.is_failed:
            print(f'  FAILED {code}: {final.error}')
            log_event({'lesson': code, 'status': 'failed', 'error': final.error, 'artifact_id': task_id}, lang)
            return
        print(f'  Unexpected status for {code}: {final.status}')
        log_event({'lesson': code, 'status': 'unexpected', 'final_status': final.status, 'artifact_id': task_id}, lang)
    except Exception as e:
        print(f'  ERROR {code}: {e}')
        log_event({'lesson': code, 'status': 'error', 'error': repr(e), 'artifact_id': task_id}, lang)


async def run_generation(codes: list[str], lang: str, dry_run: bool, slow: bool, full_prompt_fn, cards: dict, source_ids_for_notebook: dict, source_map: dict):
    to_generate = [code for code in codes if not should_skip(code, lang)]
    already_done = [code for code in codes if should_skip(code, lang)]

    if already_done:
        print(f"Already complete ({len(already_done)}): {', '.join(already_done)}")
    if not to_generate:
        print('All requested notebooks already have audio files.')
        return

    if dry_run:
        print('DRY RUN -- no NotebookLM API calls')
        for code in to_generate:
            specs, warnings = resolve_source_specs(code, source_ids_for_notebook, source_map)
            print(f"\n{code} - {cards[code]['title']}")
            print(f"  Prompt length: {len(full_prompt_fn(code))} chars")
            for spec in specs:
                ref = spec['path'].name if spec['mode'] == 'file' else spec['url']
                print(f"  - {spec['mode']}: {ref}")
            for w in warnings:
                print(f"  WARNING: {w}")
        return

    inter_delay = INTER_START_DELAY_SLOW if slow else INTER_START_DELAY
    client = await NotebookLMClient.from_storage()
    async with client:
        for idx, code in enumerate(to_generate, start=1):
            title = cards[code]['title']
            nb_name = notebook_name(lang, code)
            print(f"\n=== {code} - {title} ===")
            notebook = await find_or_create_notebook(client, nb_name)
            print(f"Notebook: {notebook.title} ({notebook.id})")
            source_ids = await ensure_sources(client, notebook.id, code, source_ids_for_notebook, source_map)
            if not source_ids:
                print(f'  No usable sources for {code}, skipping.')
                continue
            task_id = await start_generation(client, notebook.id, code, full_prompt_fn(code), source_ids, lang, nb_name)
            if task_id:
                await wait_and_download(client, notebook.id, task_id, code, lang, title)
            if idx != len(to_generate):
                await asyncio.sleep(inter_delay)


def main():
    parser = argparse.ArgumentParser(description='DIPS -- V2 NotebookLM Audio Generator')
    parser.add_argument('--lang', default='en', choices=SUPPORTED_LANGUAGES, help='Audio language (default: en)')
    parser.add_argument('--lessons', nargs='+', default=None, help='Notebook codes such as N01 N02. Default: all.')
    parser.add_argument('--dry-run', action='store_true', help='Validate prompts and sources without NotebookLM API calls')
    parser.add_argument('--status', action='store_true', help='Show which audio files already exist and exit')
    parser.add_argument('--slow', action='store_true', help='Use a slower delay between generations')
    args = parser.parse_args()

    full_prompt_fn, cards, source_ids_for_notebook = _load_prompts(args.lang)
    all_codes = list(cards.keys())
    lessons = args.lessons or all_codes
    for code in lessons:
        if code not in cards:
            print(f"Unknown notebook code: {code} (valid: {', '.join(all_codes)})")
            sys.exit(1)

    source_map = load_source_index()

    print('=' * 60)
    print('DIPS -- V2 NotebookLM Audio Generator')
    print(f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f'Language: {args.lang}')
    print(f"Project root: {PROJECT_ROOT}")
    print('=' * 60)

    if args.status:
        done = [code for code in all_codes if should_skip(code, args.lang)]
        missing = [code for code in all_codes if not should_skip(code, args.lang)]
        print(f"\nComplete ({len(done)}/{len(all_codes)}):")
        for code in done:
            size_mb = raw_path_for(code, args.lang).stat().st_size / (1024 * 1024)
            print(f"  {code} - {cards[code]['title']} ({size_mb:.1f} MB)")
        if missing:
            print(f"\nMissing ({len(missing)}):")
            for code in missing:
                print(f"  {code} - {cards[code]['title']}")
            print(f"\nTo generate: python run_v2.py --lang {args.lang} --lessons {' '.join(missing)}")
        return

    validate_setup(lessons, args.lang, full_prompt_fn, cards, source_ids_for_notebook, source_map)
    asyncio.run(run_generation(lessons, args.lang, args.dry_run, args.slow, full_prompt_fn, cards, source_ids_for_notebook, source_map))

    done = [code for code in all_codes if should_skip(code, args.lang)]
    missing = [code for code in all_codes if not should_skip(code, args.lang)]
    print('\n' + '=' * 60)
    print(f'TOTAL: {len(done)}/{len(all_codes)} audio files complete')
    if missing:
        print(f"Still missing: {', '.join(missing)}")
        print(f"To retry: python run_v2.py --lang {args.lang} --lessons {' '.join(missing)}")
    else:
        print(f"ALL {len(all_codes)} NOTEBOOKS COMPLETE!")
        print(f"Audio output: {out_dir(args.lang)}")
    print('=' * 60)


if __name__ == '__main__':
    main()
