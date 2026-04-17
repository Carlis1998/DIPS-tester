#!/usr/bin/env python3
"""Normalize fetched raw sources into structured markdown in data/normalized/.

Handles PDF, HTML, and TXT inputs.

Usage:
    python3 scripts/normalize_sources.py
    python3 scripts/normalize_sources.py --source dips_exam_2024
"""
import json, os, re, sys, subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NORMALIZED = DATA / "normalized"
SOURCE_INDEX = DATA / "source_index.json"


def load_index():
    with open(SOURCE_INDEX) as f:
        return json.load(f)


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using available tools."""
    # Try pdftotext (poppler) first
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Try python-based extraction
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
        return "\n\n".join(text_parts)
    except ImportError:
        pass

    # Try PyPDF2
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        text_parts = []
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
        return "\n\n".join(text_parts)
    except ImportError:
        pass

    print(f"  WARNING: No PDF extraction tool available. Install one of:")
    print(f"    pip install pdfplumber")
    print(f"    pip install PyPDF2")
    print(f"    brew install poppler  (for pdftotext)")
    return None


def extract_text_from_html(html_path):
    """Extract readable text from HTML."""
    with open(html_path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    # Strip HTML tags (simple approach)
    text = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    # Decode common entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def normalize_entry(entry):
    """Convert a source entry into a normalized markdown file."""
    source_path = ROOT / entry["local_path"]

    if not source_path.exists():
        print(f"  SKIP: File not found — {source_path}")
        return False

    # Determine output directory
    source_type = entry["type"]
    if "exam" in source_type:
        out_dir = NORMALIZED / "exams"
    elif source_type == "treaty":
        out_dir = NORMALIZED / "treaties"
    else:
        out_dir = NORMALIZED / "official"

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{entry['id']}.md"

    # Extract text based on file type
    suffix = source_path.suffix.lower()
    if suffix == ".pdf":
        body = extract_text_from_pdf(source_path)
        if body is None:
            print(f"  FAILED: Could not extract text from {source_path}")
            return False
    elif suffix in (".html", ".htm"):
        body = extract_text_from_html(source_path)
    elif suffix in (".txt", ".md"):
        with open(source_path, "r", encoding="utf-8", errors="replace") as f:
            body = f.read()
    elif suffix == ".json":
        with open(source_path, "r", encoding="utf-8") as f:
            body = json.dumps(json.load(f), indent=2, ensure_ascii=False)
    else:
        print(f"  SKIP: Unsupported format {suffix}")
        return False

    if not body or len(body.strip()) < 50:
        print(f"  WARNING: Very little text extracted ({len(body.strip())} chars)")

    # Write normalized markdown with frontmatter
    md = f"""---
id: {entry['id']}
title: {entry['title']}
year: {entry.get('year', 'unknown')}
lang: {entry.get('lang', 'unknown')}
source_class: {entry.get('source_class', 'unknown')}
source_url: {entry.get('url', '')}
normalized_at: {datetime.now().isoformat()}
---

# {entry['title']}

{body}
"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"  OK: {out_path} ({len(body):,} chars)")
    return True


def main():
    target_source = None
    if "--source" in sys.argv:
        idx = sys.argv.index("--source")
        if idx + 1 < len(sys.argv):
            target_source = sys.argv[idx + 1]

    index = load_index()
    ok_count = 0
    fail_count = 0
    skip_count = 0

    print(f"\n{'='*60}")
    print(f"DIPS Source Normalizer")
    print(f"{'='*60}\n")

    for entry in index:
        if target_source and entry["id"] != target_source:
            continue

        if not entry.get("fetched"):
            print(f"SKIP (not fetched): {entry['id']}")
            skip_count += 1
            continue

        print(f"\n--- {entry['id']} ---")
        if normalize_entry(entry):
            ok_count += 1
        else:
            fail_count += 1

    print(f"\n{'='*60}")
    print(f"Normalized: {ok_count}  |  Failed: {fail_count}  |  Skipped: {skip_count}")
    print(f"Output in: {NORMALIZED}")
    print(f"\nNext: python3 scripts/generate_content.py")


if __name__ == "__main__":
    main()
