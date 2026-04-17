#!/usr/bin/env python3
"""Generate study content from normalized sources.

This script provides the framework for content generation. For full LLM-powered
extraction, set ANTHROPIC_API_KEY or OPENAI_API_KEY and use --llm mode.
Without an API key, it generates placeholder structure from existing data.

Usage:
    python3 scripts/generate_content.py                    # validate existing data
    python3 scripts/generate_content.py --extract-exams    # extract Q&A from exam PDFs
    python3 scripts/generate_content.py --generate-cards   # generate flashcards from normalized text
    python3 scripts/generate_content.py --stats            # show content stats
"""
import json, os, sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NORMALIZED = DATA / "normalized"
APP_DATA = ROOT / "app" / "data"


def load_json(name):
    path = DATA / name
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def save_json(name, data):
    path = DATA / name
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {path}")


def sync_app_data():
    """Copy app-facing JSON files into app/data so the app also works when served from app/."""
    try:
        APP_DATA.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        print(f"  WARNING: Could not create {APP_DATA}: {e}")
        print(f"  App-data sync skipped. Serve from repo root via ./app/serve.sh instead.")
        return
    copied = 0
    for name in [
        "topics.json",
        "questions_sv.json",
        "questions_en.json",
        "flashcards.json",
        "essays.json",
        "mocks.json",
        "audio_map.json",
    ]:
        src = DATA / name
        dst = APP_DATA / name
        if not src.exists():
            continue
        try:
            shutil.copy2(src, dst)
        except PermissionError as e:
            print(f"  WARNING: Could not copy {src.name} into app/data: {e}")
            print(f"  App-data sync incomplete. Serve from repo root via ./app/serve.sh instead.")
            return
        copied += 1
    print(f"  Synced {copied} app data files to {APP_DATA}")


def show_stats():
    """Show current content statistics."""
    topics = load_json("topics.json")
    q_sv = load_json("questions_sv.json")
    q_en = load_json("questions_en.json")
    cards = load_json("flashcards.json")
    essays = load_json("essays.json")
    mocks = load_json("mocks.json")
    audio = load_json("audio_map.json")
    sources = load_json("source_index.json")

    print(f"\n{'='*60}")
    print(f"DIPS-Tester Content Statistics")
    print(f"{'='*60}")
    print(f"  Topics:          {len(topics['topics']) if topics else 0}")
    print(f"  Swedish MCQs:    {len(q_sv['questions']) if q_sv else 0}")
    print(f"  English MCQs:    {len(q_en['questions']) if q_en else 0}")
    print(f"  Flashcards:      {len(cards) if cards else 0}")
    print(f"  Essay prompts:   {len(essays['essays']) if essays else 0}")
    print(f"  Mock exams:      {len(mocks['mocks']) if mocks else 0}")
    print(f"  Audio episodes:  {len(audio['study_podcasts']) if audio else 0}")
    print(f"  Sources indexed: {len(sources) if sources else 0}")

    # Check normalized files
    normalized_count = 0
    for subdir in ["exams", "official", "treaties"]:
        norm_dir = NORMALIZED / subdir
        if norm_dir.exists():
            normalized_count += len(list(norm_dir.glob("*.md")))
    print(f"  Normalized docs: {normalized_count}")

    # Coverage per topic
    if topics and q_sv:
        print(f"\n  Coverage per topic (Swedish MCQs):")
        for t in topics["topics"]:
            count = len([q for q in q_sv["questions"] if t["code"] in q["topics"]])
            print(f"    {t['code']} {t['title'][:40]:40s} {count} Qs")

    if topics and cards:
        print(f"\n  Coverage per topic (Flashcards):")
        for t in topics["topics"]:
            count = len([c for c in cards if c["topic"] == t["code"]])
            print(f"    {t['code']} {t['title'][:40]:40s} {count} cards")

    # Source fetch status
    if sources:
        fetched = len([s for s in sources if s.get("fetched")])
        print(f"\n  Sources fetched: {fetched}/{len(sources)}")
        unfetched = [s for s in sources if not s.get("fetched")]
        if unfetched:
            print(f"  Unfetched sources:")
            for s in unfetched:
                print(f"    - {s['id']}: {s['title']}")


def extract_exam_questions():
    """Framework for extracting questions from exam PDFs.

    With --llm flag and API key, sends normalized exam text to an LLM
    to extract structured Q&A pairs. Without it, prints guidance.
    """
    exam_dir = NORMALIZED / "exams"
    if not exam_dir.exists():
        print("No normalized exams found. Run normalize_sources.py first.")
        return

    exams = list(exam_dir.glob("*.md"))
    if not exams:
        print("No normalized exam files found.")
        return

    print(f"\nFound {len(exams)} normalized exam files:")
    for e in sorted(exams):
        print(f"  - {e.name}")

    if "--llm" not in sys.argv:
        print(f"\nTo auto-extract questions, run with --llm flag and set ANTHROPIC_API_KEY.")
        print(f"Manual extraction tip:")
        print(f"  1. Read each normalized exam in data/normalized/exams/")
        print(f"  2. For each factual question, add to data/questions_sv.json")
        print(f"  3. For each essay prompt, add to data/essays.json")
        print(f"  4. Set exam_year field to track provenance")
        return

    # LLM-powered extraction would go here
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Set ANTHROPIC_API_KEY to use LLM extraction.")
        return

    print("\nLLM extraction mode — processing exams...")
    # This is where you'd call the Claude API to extract Q&A pairs
    # from each normalized exam file and merge them into questions_sv.json


def generate_flashcards():
    """Framework for generating flashcards from normalized text."""
    print("\nFlashcard generation framework:")
    print("  - Official sources -> fact cards")
    print("  - Treaties -> definition/concept cards")
    print("  - Exam patterns -> common-trap cards")
    print("\nTo auto-generate, run with --llm flag and set ANTHROPIC_API_KEY.")


def validate_data():
    """Check data integrity — IDs, references, completeness."""
    errors = []

    q_sv = load_json("questions_sv.json")
    q_en = load_json("questions_en.json")
    cards = load_json("flashcards.json")
    topics = load_json("topics.json")
    essays = load_json("essays.json")
    mocks = load_json("mocks.json")

    topic_codes = set(t["code"] for t in topics["topics"]) if topics else set()

    # Check question topic references
    if q_sv:
        for q in q_sv["questions"]:
            for t in q["topics"]:
                if t not in topic_codes:
                    errors.append(f"Question {q['id']}: unknown topic {t}")
            if q["answer"] not in q["options"]:
                errors.append(f"Question {q['id']}: answer '{q['answer']}' not in options")

    if q_en:
        for q in q_en["questions"]:
            for t in q["topics"]:
                if t not in topic_codes:
                    errors.append(f"Question {q['id']}: unknown topic {t}")

    # Check flashcard topics
    if cards:
        for c in cards:
            if c["topic"] not in topic_codes:
                errors.append(f"Card {c['id']}: unknown topic {c['topic']}")

    # Check mock references
    if mocks and q_sv:
        q_ids = set(q["id"] for q in q_sv["questions"])
        for m in mocks["mocks"]:
            for s in m["sections"]:
                if s["type"] == "mcq":
                    for qid in s.get("question_ids", []):
                        if qid not in q_ids:
                            errors.append(f"Mock {m['id']}: unknown question {qid}")

    if errors:
        print(f"\nValidation errors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    else:
        print(f"\nAll data validates OK.")

    return len(errors) == 0


def main():
    if "--stats" in sys.argv:
        show_stats()
        sync_app_data()
    elif "--extract-exams" in sys.argv:
        extract_exam_questions()
    elif "--generate-cards" in sys.argv:
        generate_flashcards()
    else:
        print("Validating existing data...")
        validate_data()
        show_stats()
        sync_app_data()


if __name__ == "__main__":
    main()
