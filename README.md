# DIPS Tester

Practice tool for the Swedish Diplomatic Programme (Diplomatprogrammet) written exam.

Static GitHub Pages app — no backend, mobile-first, localStorage for progress.

## Quick Start

```bash
# 1. Fetch official sources (exams, treaties, etc.)
python3 scripts/fetch_sources.py --tier 0    # exam PDFs first
python3 scripts/fetch_sources.py --tier 1    # primary documents

# 2. Normalize fetched sources into structured text
python3 scripts/normalize_sources.py

# 3. Check content stats
python3 scripts/generate_content.py --stats

# 4. Serve the app locally
./app/serve.sh
# Open http://localhost:8080/app/
```

## Project Structure

```
DIPS-Tester/
  raw/                          # Downloaded source files
    exams/                      #   Old exam PDFs (2019-2025)
    official/                   #   Utrikesdeklaration, Q&A, etc.
    treaties/                   #   Vienna conventions, UN Charter, etc.
    current-affairs/            #   News scrapes
    podcasts/                   #   Podcast downloads
  data/                         # Structured content (JSON)
    source_index.json           #   Master index of all sources
    topics.json                 #   10 topic areas (T01-T10)
    questions_sv.json           #   Swedish MCQs
    questions_en.json           #   English MCQs
    flashcards.json             #   Flashcards per topic
    essays.json                 #   Essay prompts with outlines
    mocks.json                  #   Mock exam definitions
    resources.json              #   Categorized links (test vs. study)
    audio_map.json              #   10 podcast episodes (SV + ES)
    normalized/                 #   Normalized markdown from raw/
  scripts/
    fetch_sources.py            #   Download official sources
    normalize_sources.py        #   PDF/HTML -> structured markdown
    generate_content.py         #   Content generation & validation
    build_bundle.py             #   Single-file HTML bundle
  app/                          # Static web app (GitHub Pages)
    index.html                  #   Main SPA with all views
    manifest.json               #   PWA manifest
    sw.js                       #   Service worker for offline
    serve.sh                    #   Local dev server
    data/                       #   App-local JSON copies for GitHub Pages /app deploy
  out/
    SV/audio/                   #   Swedish audio files
    ES/audio/                   #   Spanish audio files
    EN/audio/                   #   English audio files
    bundles/                    #   Self-contained HTML bundles
    logs/                       #   Build logs
```

## App Pages

| View | Description |
|------|-------------|
| **Hem** | Overview, quick start, progress, what to study first |
| **Amnen (T01-T10)** | Per-topic study with MCQs, flashcards, subtopics, and matching audio plan |
| **Ovningsprov** | Timed mock exams mirroring real DIPS structure |
| **Uppsats** | Essay prompts with timer and outline scaffolding |
| **Drill** | Hard-bucket grind across all topics |
| **Kallor** | Official sources, podcasts, and reference databases |

## Content Model

- **10 topics** matching DIPS exam areas (Sweden, intl. orgs, law, conflicts, economy, history, culture, climate, vocabulary, essay)
- **Source provenance**: every item tagged `official`, `secondary`, or `community`
- **Bilingual**: Swedish MCQs for facts, English for some essays
- **Audio**: 10 planned podcast episodes in Swedish + Spanish

## Adding Content

1. Add MCQs to `data/questions_sv.json` following the existing schema
2. Add flashcards to `data/flashcards.json`
3. Add essay prompts to `data/essays.json`
4. Run `python3 scripts/generate_content.py` to validate

## Deploy to GitHub Pages

1. Push this repo to GitHub
2. Go to Settings > Pages > Source: Deploy from branch
3. Set branch to `main` and folder to `/app`
4. The app serves from `https://username.github.io/DIPS-Tester/`

Because the Pages root is `/app`, the app also includes `app/data/` copies of the JSON files.
If you regenerate content, refresh those files before pushing.

## Manual Source Files

The fetch script will report which files it couldn't download automatically.
Place manually downloaded files at the paths shown in the output:

| Source | Place at |
|--------|----------|
| Exam PDFs (if 404) | `raw/exams/dips_exam_YEAR.pdf` |
| Utrikesdeklarationen (HTML page) | `raw/official/utrikesdeklarationen_2026.html` |
| Paywalled content (Landguiden, FT) | Not required — used as reference only |

## Tech Stack

- Plain HTML + CSS + vanilla JS (no framework, no build step)
- JSON data files loaded via fetch()
- localStorage for all progress tracking
- Service worker for offline PWA support
- Python 3 scripts for source pipeline (no pip dependencies required for basic use)
