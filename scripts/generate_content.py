#!/usr/bin/env python3
"""Generate and validate DIPS study content."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NORMALIZED = DATA / "normalized"
APP_DATA = ROOT / "app" / "data"


def load_json(name):
    path = DATA / name
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sync_app_data():
    """Copy app-facing JSON files into app/data so the app also works when served from app/."""
    try:
        APP_DATA.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        print(f"  WARNING: Could not create {APP_DATA}: {e}")
        print("  App-data sync skipped. Serve from repo root via ./app/serve.sh instead.")
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
        "question_batteries.json",
    ]:
        src = DATA / name
        dst = APP_DATA / name
        if not src.exists():
            continue
        try:
            shutil.copy2(src, dst)
        except PermissionError as e:
            print(f"  WARNING: Could not copy {src.name} into app/data: {e}")
            print("  App-data sync incomplete. Serve from repo root via ./app/serve.sh instead.")
            return
        copied += 1
    print(f"  Synced {copied} app data files to {APP_DATA}")


def show_stats():
    topics = load_json("topics.json")
    q_sv = load_json("questions_sv.json")
    q_en = load_json("questions_en.json")
    cards = load_json("flashcards.json")
    essays = load_json("essays.json")
    mocks = load_json("mocks.json")
    audio = load_json("audio_map.json")
    sources = load_json("source_index.json")
    batteries = load_json("question_batteries.json")

    print(f"\n{'=' * 60}")
    print("DIPS-Tester Content Statistics")
    print(f"{'=' * 60}")
    print(f"  Topics:            {len(topics['topics']) if topics else 0}")
    print(f"  Swedish MCQs:      {len(q_sv['questions']) if q_sv else 0}")
    print(f"  English MCQs:      {len(q_en['questions']) if q_en else 0}")
    print(f"  Flashcards:        {len(cards) if cards else 0}")
    print(f"  Essay prompts:     {len(essays['essays']) if essays else 0}")
    print(f"  Mock exams:        {len(mocks['mocks']) if mocks else 0}")
    print(f"  Audio episodes:    {len(audio['study_podcasts']) if audio else 0}")
    print(f"  Question batteries:{batteries['battery_count'] if batteries else 0}")
    print(f"  Sources indexed:   {len(sources) if sources else 0}")

    normalized_count = 0
    for subdir in ["exams", "official", "treaties"]:
        norm_dir = NORMALIZED / subdir
        if norm_dir.exists():
            normalized_count += len(list(norm_dir.glob("*.md")))
    print(f"  Normalized docs:   {normalized_count}")

    if topics and q_sv:
        print("\n  Coverage per topic (Swedish MCQs):")
        for topic in topics["topics"]:
            count = len([q for q in q_sv["questions"] if topic["code"] in q["topics"]])
            print(f"    {topic['code']} {topic['title'][:40]:40s} {count} Qs")

    if topics and cards:
        print("\n  Coverage per topic (Flashcards):")
        for topic in topics["topics"]:
            count = len([c for c in cards if c["topic"] == topic["code"]])
            print(f"    {topic['code']} {topic['title'][:40]:40s} {count} cards")

    if batteries:
        print("\n  Extracted question batteries:")
        for battery in batteries["batteries"][:12]:
            print(f"    {battery['exam_year']} {battery['section_id']:18s} {battery['question_count']} questions")

    if sources:
        fetched = len([s for s in sources if s.get("fetched")])
        print(f"\n  Sources fetched: {fetched}/{len(sources)}")
        unfetched = [s for s in sources if not s.get("fetched")]
        if unfetched:
            print("  Unfetched sources:")
            for source in unfetched:
                print(f"    - {source['id']}: {source['title']}")


def extract_question_batteries():
    script = ROOT / "scripts" / "extract_question_batteries.py"
    print("\nRunning structured question-battery extraction...")
    result = subprocess.run([sys.executable, str(script)], cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)
    sync_app_data()


def validate_data():
    errors = []

    q_sv = load_json("questions_sv.json")
    q_en = load_json("questions_en.json")
    cards = load_json("flashcards.json")
    topics = load_json("topics.json")
    mocks = load_json("mocks.json")

    topic_codes = set(t["code"] for t in topics["topics"]) if topics else set()

    if q_sv:
        for question in q_sv["questions"]:
            for topic in question["topics"]:
                if topic not in topic_codes:
                    errors.append(f"Question {question['id']}: unknown topic {topic}")
            if question["answer"] not in question["options"]:
                errors.append(f"Question {question['id']}: answer '{question['answer']}' not in options")

    if q_en:
        for question in q_en["questions"]:
            for topic in question["topics"]:
                if topic not in topic_codes:
                    errors.append(f"Question {question['id']}: unknown topic {topic}")

    if cards:
        for card in cards:
            if card["topic"] not in topic_codes:
                errors.append(f"Card {card['id']}: unknown topic {card['topic']}")

    if mocks and q_sv:
        q_ids = set(q["id"] for q in q_sv["questions"])
        for mock in mocks["mocks"]:
            for section in mock["sections"]:
                if section["type"] == "mcq":
                    for qid in section.get("question_ids", []):
                        if qid not in q_ids:
                            errors.append(f"Mock {mock['id']}: unknown question {qid}")

    if errors:
        print(f"\nValidation errors ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\nAll data validates OK.")

    return len(errors) == 0


def main():
    if "--stats" in sys.argv:
        show_stats()
        sync_app_data()
    elif "--extract-batteries" in sys.argv:
        extract_question_batteries()
    else:
        print("Validating existing data...")
        validate_data()
        show_stats()
        sync_app_data()


if __name__ == "__main__":
    main()
