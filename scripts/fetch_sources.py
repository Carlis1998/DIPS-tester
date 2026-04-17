#!/usr/bin/env python3
"""Fetch official DIPS sources into raw/ directories.

Usage:
    python3 scripts/fetch_sources.py              # fetch all unfetched
    python3 scripts/fetch_sources.py --tier 0     # only TIER 0 (exam PDFs)
    python3 scripts/fetch_sources.py --tier 1     # only TIER 1 (primary docs)
    python3 scripts/fetch_sources.py --force       # re-fetch already fetched
"""
import json, os, sys, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SOURCE_INDEX = DATA / "source_index.json"


def load_index():
    with open(SOURCE_INDEX) as f:
        return json.load(f)


def save_index(index):
    with open(SOURCE_INDEX, "w") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"  Updated {SOURCE_INDEX}")


def fetch_file(url, dest_path, timeout=30):
    """Download a URL to dest_path. Returns True on success."""
    dest = ROOT / dest_path
    dest.parent.mkdir(parents=True, exist_ok=True)

    print(f"  Fetching: {url}")
    print(f"       -> {dest}")

    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (DIPS-Tester study tool)"
    })

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if len(data) < 100:
                print(f"  WARNING: Very small response ({len(data)} bytes), may not be valid")
            with open(dest, "wb") as f:
                f.write(data)
            print(f"  OK: {len(data):,} bytes")
            return True
    except urllib.error.HTTPError as e:
        print(f"  FAILED: HTTP {e.code} — {url}")
        return False
    except urllib.error.URLError as e:
        print(f"  FAILED: Network error — {e.reason}")
        return False
    except Exception as e:
        print(f"  FAILED: {e}")
        return False


# Define which sources belong to which tier
TIER_MAP = {
    "exam_pdf": 0,
    "qa_pdf": 0,
    "policy_speech": 1,
    "policy_doc": 1,
    "treaty": 1,
    "flashcard_deck": 2,
}


def main():
    force = "--force" in sys.argv
    tier_filter = None
    if "--tier" in sys.argv:
        idx = sys.argv.index("--tier")
        if idx + 1 < len(sys.argv):
            tier_filter = int(sys.argv[idx + 1])

    index = load_index()
    fetched_count = 0
    failed_count = 0
    skipped_count = 0
    failed_sources = []

    print(f"\n{'='*60}")
    print(f"DIPS Source Fetcher")
    print(f"{'='*60}")
    print(f"Sources in index: {len(index)}")
    print(f"Force re-fetch: {force}")
    print(f"Tier filter: {tier_filter if tier_filter is not None else 'all'}")
    print(f"{'='*60}\n")

    for entry in index:
        source_tier = TIER_MAP.get(entry["type"], 3)

        if tier_filter is not None and source_tier != tier_filter:
            continue

        if entry.get("fetched") and not force:
            print(f"SKIP (already fetched): {entry['id']}")
            skipped_count += 1
            continue

        print(f"\n--- {entry['id']} (tier {source_tier}) ---")
        print(f"    Title: {entry['title']}")

        ok = fetch_file(entry["url"], entry["local_path"])

        if ok:
            entry["fetched"] = True
            entry["fetched_at"] = datetime.now().isoformat()
            fetched_count += 1
        else:
            entry["fetched"] = False
            entry["fetch_error"] = f"Failed at {datetime.now().isoformat()}"
            failed_count += 1
            failed_sources.append(entry)

        # Be polite — don't hammer servers
        time.sleep(1)

    save_index(index)

    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"  Fetched:  {fetched_count}")
    print(f"  Failed:   {failed_count}")
    print(f"  Skipped:  {skipped_count}")

    if failed_sources:
        print(f"\n--- MANUAL ACTION REQUIRED ---")
        print(f"The following sources could not be fetched automatically.")
        print(f"Please download them manually and place them at the indicated paths:\n")
        for s in failed_sources:
            print(f"  Source:  {s['title']}")
            print(f"  URL:     {s['url']}")
            print(f"  Put at:  {ROOT / s['local_path']}")
            print()

    print(f"\nDone. Run 'python3 scripts/normalize_sources.py' next.")


if __name__ == "__main__":
    main()
