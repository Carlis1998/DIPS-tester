#!/usr/bin/env python3
"""Build NotebookLM packet files for DIPS Spanish audio overviews."""
from __future__ import annotations
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from prompts.dips_notebooklm_es import NOTEBOOK_CARDS_ES, full_prompt_es, SOURCE_IDS_FOR_NOTEBOOK

OUT_DIR = PROJECT_ROOT / 'out' / 'notebooklm' / 'es_packets'
OUT_DIR.mkdir(parents=True, exist_ok=True)

source_index = json.loads((PROJECT_ROOT / 'data' / 'source_index.json').read_text(encoding='utf-8'))
source_map = {item['id']: item for item in source_index}

RESOURCE_HINTS = {
    'eu_treaty_teu': {
        'title': 'Treaty on European Union (TEU)',
        'url': 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:12012M/TXT',
        'note': 'Fetch manually if the raw source is missing.'
    },
    'res_qa_placeholder': {
        'title': 'European Commission / Consilium / SIEPS packet',
        'url': 'https://commission.europa.eu/about/organisation/college-commissioners_en',
        'note': 'Supplement with Consilium and SIEPS pages for current EU institutional context.'
    }
}

packets = []
for code, card in NOTEBOOK_CARDS_ES.items():
    sources = []
    for sid in SOURCE_IDS_FOR_NOTEBOOK.get(code, []):
        src = source_map.get(sid) or RESOURCE_HINTS.get(sid)
        if not src:
            continue
        sources.append({
            'id': sid,
            'title': src.get('title'),
            'url': src.get('url'),
            'local_path': src.get('local_path'),
            'note': src.get('note', ''),
        })
    packet = {
        'code': code,
        'title': card['title'],
        'prompt': full_prompt_es(code),
        'sources': sources,
    }
    packets.append(packet)

    md_lines = [f"# {code} — {card['title']}", '', '## Upload order', '']
    for i, src in enumerate(sources, 1):
        md_lines.append(f"{i}. {src['title']}")
        if src.get('url'):
            md_lines.append(f"   URL: {src['url']}")
        if src.get('local_path'):
            md_lines.append(f"   Local path: {src['local_path']}")
        if src.get('note'):
            md_lines.append(f"   Note: {src['note']}")
        md_lines.append('')
    md_lines.append('## Customize prompt')
    md_lines.append('')
    md_lines.append('```text')
    md_lines.append(packet['prompt'])
    md_lines.append('```')
    (OUT_DIR / f"{code}.md").write_text(chr(10).join(md_lines), encoding="utf-8")

(OUT_DIR / 'notebooks_es.json').write_text(json.dumps(packets, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"Wrote {len(packets)} NotebookLM packets to {OUT_DIR}")
