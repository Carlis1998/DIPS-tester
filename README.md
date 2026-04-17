# DIPS Tester

Practice tool for the Swedish Diplomatic Programme (Diplomatprogrammet) written exam.

Static GitHub Pages app, no backend, mobile-first, localStorage for progress.

## Quick Start

```bash
# 1. Fetch official sources
python3 scripts/fetch_sources.py --tier 0
python3 scripts/fetch_sources.py --tier 1

# 2. Normalize fetched sources
python3 scripts/normalize_sources.py

# 3. Extract structured question batteries from old exams
python3 scripts/generate_content.py --extract-batteries

# 4. Inspect stats and sync app/data
python3 scripts/generate_content.py --stats

# 5. Serve the app locally
./app/serve.sh
# Open http://localhost:8080/app/
```

## What is new

The repo now extracts the large factual **frågebatterier** from normalized exam PDFs into:

- `data/question_batteries.json`
- `app/data/question_batteries.json`

This includes sections such as:

- `Samhällsorientering - Sverige`
- `Samhällsorientering - Globalt`
- `Historia, Geografi`
- `Kultur`
- `Ordförståelse`

The extractor preserves:

- exam year
- section title
- question number
- prompt text
- subquestions such as `a)`, `b)`, `c)`
- multiple-choice options where they are present in the source text
- simple metadata such as `max_answers`

Important: this extraction is **structure-first**, not answer-key generation. It is meant to make the exam batteries reusable in the repo and app pipeline. It does not invent correct answers for open questions.

## Recommended workflow

### Full pipeline

```bash
python3 scripts/fetch_sources.py --tier 0
python3 scripts/fetch_sources.py --tier 1
python3 scripts/normalize_sources.py
python3 scripts/generate_content.py --extract-batteries
python3 scripts/generate_content.py --stats
```

### Re-run only battery extraction

```bash
python3 scripts/generate_content.py --extract-batteries
```

### Parse just one exam manually

```bash
python3 scripts/extract_question_batteries.py --exam 2023
```

## How to use `question_batteries.json`

This file is the right source for the next steps:

1. build free-response training views in the app
2. generate flashcards from battery questions
3. generate candidate answer keys manually or with an LLM
4. convert selected multiple-choice items into graded `questions_sv.json`
5. create mock exams from real historical sections

## Reality Check

The repository now contains more exam material than the visible app has turned into interactive questions.

- fetched official exam PDFs: 2019, 2021, 2022, 2023, 2024, 2025
- structured question batteries extracted so far: mainly 2023-2025
- current interactive MCQ layer in the app: still much smaller than the extracted archive

So yes: there is already more exam substance in the repo than the frontend currently exposes.
The app is useful now, but the full exam archive is richer than the current `questions_sv.json` and `flashcards.json`.

## Manual files to check yourself

If the fetch script misses anything, these are the most important files to verify manually:

- all official DIPS exam PDFs in `raw/exams/`
- the Q&A PDF in `raw/official/`
- `Utrikesdeklarationen 2025` and `2026`
- the treaty PDFs in `raw/treaties/`

If a source fails to download automatically, place it at the path shown by `fetch_sources.py`, then rerun normalization and extraction.

## Project Structure

```text
DIPS-Tester/
  raw/
    exams/
    official/
    treaties/
    current-affairs/
    podcasts/
  data/
    source_index.json
    topics.json
    questions_sv.json
    questions_en.json
    flashcards.json
    essays.json
    mocks.json
    resources.json
    audio_map.json
    question_batteries.json
    normalized/
  scripts/
    fetch_sources.py
    normalize_sources.py
    extract_question_batteries.py
    generate_content.py
    build_bundle.py
  app/
    index.html
    manifest.json
    sw.js
    serve.sh
  out/
    SV/audio/
    ES/audio/
    EN/audio/
    bundles/
    logs/
```

## App notes

The app can keep using the existing MCQ/flashcard JSON files, while `question_batteries.json` becomes the structured source for richer DIPS-specific training later.
The mock and resources views should be treated as the bridge between the lightweight app layer and the actual original PDFs.

## Deploy to GitHub Pages

1. Push this repo to GitHub
2. Go to Settings -> Pages -> Deploy from branch
3. Copy `app/` into `docs/`
4. Set branch to `main` and folder to `/docs`
5. Serve from `https://username.github.io/DIPS-Tester/`


## NotebookLM (Spanish audio overviews)

The repo now includes a practical NotebookLM production package:

- `notebooklm/PRODUCTION_SPEC.md`
- `prompts/dips_notebooklm_es.py`
- `scripts/build_notebooklm_packets.py`

Build the packet files:

```bash
python3 scripts/build_notebooklm_packets.py
```

This writes:

- `out/notebooklm/es_packets/notebooks_es.json`
- one Markdown packet per notebook in `out/notebooklm/es_packets/`

Each packet contains:
- upload order
- source URLs / local paths
- a full Spanish-audio Customize prompt

Recommended workflow:
1. Run `python3 scripts/build_notebooklm_packets.py`
2. Open one packet, e.g. `out/notebooklm/es_packets/N01.md`
3. Create a NotebookLM notebook
4. Upload the listed sources in order
5. Paste the generated prompt into Customize
6. Set NotebookLM output language to Spanish
7. Generate the audio overview

This package is intentionally lighter and cleaner than the old TOGAF prompt style: fewer sources, less vocabulary coaching, more emphasis on structure and analytical usefulness.
