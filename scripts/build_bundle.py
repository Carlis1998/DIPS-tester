#!/usr/bin/env python3
"""Build a single self-contained HTML file that bundles the entire DIPS study app.

Usage:  python3 scripts/build_bundle.py
Output: out/bundles/dips-study-bundle.html
"""
import json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"
DATA = ROOT / "data"
OUT = ROOT / "out" / "bundles"


def load(path):
    with open(path) as f:
        return f.read().strip()


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # Load all JSON data
    topics_json = load(DATA / "topics.json")
    questions_sv_json = load(DATA / "questions_sv.json")
    questions_en_json = load(DATA / "questions_en.json")
    flashcards_json = load(DATA / "flashcards.json")
    essays_json = load(DATA / "essays.json")
    mocks_json = load(DATA / "mocks.json")
    audio_map_json = load(DATA / "audio_map.json")

    # Load the main app HTML
    index_html = load(APP / "index.html")

    # Find the </head> tag and inject data
    data_script = f"""<script>
window.DIPS_DATA = {{
  topics: {topics_json},
  questions_sv: {questions_sv_json},
  questions_en: {questions_en_json},
  flashcards: {flashcards_json},
  essays: {essays_json},
  mocks: {mocks_json},
  audio_map: {audio_map_json}
}};
window.BUNDLE_MODE = true;
</script>"""

    # Inject before </head>
    bundle_html = index_html.replace("</head>", data_script + "\n</head>")

    # Replace fetch() calls with inline data access
    # The app code checks window.BUNDLE_MODE to use embedded data

    out_path = OUT / "dips-study-bundle.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(bundle_html)

    size = os.path.getsize(out_path)
    print(f"Built: {out_path}")
    print(f"Size: {size:,} bytes ({size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
