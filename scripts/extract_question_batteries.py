#!/usr/bin/env python3
"""Extract structured DIPS question batteries from normalized exam markdown.

This script parses the factual question-battery sections from normalized exam files
and writes them to data/question_batteries.json for later app use, LLM enrichment,
or manual answer-key completion.

Usage:
    python3 scripts/extract_question_batteries.py
    python3 scripts/extract_question_batteries.py --exam 2023
"""
import json
import re
import sys
from hashlib import sha1
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NORMALIZED_EXAMS = DATA / "normalized" / "exams"
OUT_PATH = DATA / "question_batteries.json"

SECTION_DEFS = [
    ("sverige", "Samhallsorientering - Sverige", re.compile(r"^Samhällsorientering\s*[–-]\s*Sverige", re.I), "T01"),
    ("globalt", "Samhallsorientering - Globalt", re.compile(r"^Samhällsorientering\s*[–-]\s*Globalt", re.I), "T02"),
    ("historia_geografi", "Historia, geografi", re.compile(r"^Historia,\s*geografi", re.I), "T06"),
    ("kultur", "Kultur", re.compile(r"^Kultur(?:\s+och\s+utbildning|,.*)?\s*(?:mm|m\.m\.)?", re.I), "T07"),
    ("ordforstaelse", "Ordforstaelse", re.compile(r"^Ordförståelse\s*mm|^Ordforstaelse\s*mm", re.I), "T09"),
]

MAIN_Q_RE = re.compile(r"^\s*(\d{1,2})[\.,)]\s*(.*\S)?\s*$")
LABEL_RE = re.compile(r"^\s*([A-Za-zÅÄÖåäö])\)\s*(.*\S)?\s*$")
PAREN_LABEL_RE = re.compile(r"^\s*\(([A-Za-zÅÄÖåäö])\)\s*(.*\S)?\s*$")
MAX_ANSWERS_RE = re.compile(r"ange max\s+([a-zåäö0-9]+)", re.I)
WORD_NUMBERS = {
    "ett": 1, "en": 1, "tva": 2, "två": 2, "tre": 3, "fyra": 4,
    "fem": 5, "sex": 6, "sju": 7, "atta": 8, "åtta": 8,
}


def clean_line(line: str) -> str:
    line = line.replace("\x0c", " ").replace("…", "...")
    line = line.replace("–", "-")
    line = re.sub(r"[.]{6,}", " ", line)
    line = re.sub(r"\s+", " ", line).strip()
    return line


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2:
            return parts[1]
    return text


def parse_year(text: str):
    m = re.search(r"^year:\s*(\d{4})$", text, re.M)
    return int(m.group(1)) if m else None


def detect_sections(body: str):
    lines = body.splitlines()
    hits = []
    for idx, line in enumerate(lines):
        cleaned = clean_line(line)
        for section_id, title, pattern, topic in SECTION_DEFS:
            if pattern.search(cleaned):
                hits.append((idx, section_id, title, topic, cleaned))
                break

    sections = []
    seen = set()
    for i, (start, section_id, title, topic, heading) in enumerate(hits):
        end = hits[i + 1][0] if i + 1 < len(hits) else len(lines)
        block = "\n".join(lines[start:end]).strip()
        fingerprint = (section_id, re.sub(r"\s+", " ", block[:1200]))
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        sections.append({
            "section_id": section_id,
            "title": title,
            "topic_hint": topic,
            "heading": heading,
            "body": block,
        })
    return sections


def split_question_blocks(section_body: str):
    lines = section_body.splitlines()[1:]
    questions = []
    current = None
    for raw in lines:
        line = clean_line(raw)
        if not line:
            continue
        match = MAIN_Q_RE.match(line)
        if match:
            if current:
                questions.append(current)
            current = {"number": int(match.group(1)), "lines": []}
            if match.group(2):
                current["lines"].append(match.group(2).strip())
        elif current is not None:
            current["lines"].append(line)
    if current:
        questions.append(current)
    return questions


def parse_inline_options(line: str):
    parts = re.split(r"\b([A-D])\)\s*", line)
    if len(parts) < 5:
        return []
    options = []
    for idx in range(1, len(parts), 2):
        label = parts[idx]
        text = parts[idx + 1].strip(" ,;") if idx + 1 < len(parts) else ""
        if text:
            options.append({"label": label, "text": text})
    return options


def parse_max_answers(text: str):
    match = MAX_ANSWERS_RE.search(text)
    if not match:
        return None
    raw = match.group(1).lower()
    if raw.isdigit():
        return int(raw)
    return WORD_NUMBERS.get(raw)


def classify_question(prompt: str, labels, options, raw_text: str):
    text = f"{prompt} {raw_text}".lower()
    if "para ihop" in text:
        return "matching"
    if "ringa in rätt svar" in text or options or any(lbl[0].isupper() for lbl in labels):
        return "mcq"
    if len(labels) >= 1:
        return "multi_part"
    if "ange max" in text:
        return "list"
    return "short_answer"


def parse_question(question, exam_year: int, section_id: str):
    lines = question["lines"]
    prompt_parts = []
    labeled = []
    current = None
    options = []

    for line in lines:
        inline_options = parse_inline_options(line)
        if inline_options and not labeled:
            options = inline_options
            current = None
            continue

        label_match = LABEL_RE.match(line) or PAREN_LABEL_RE.match(line)
        if label_match:
            current = [label_match.group(1), label_match.group(2) or ""]
            labeled.append(current)
            continue

        if current is not None and labeled:
            current[1] = f"{current[1]} {line}".strip()
        else:
            prompt_parts.append(line)

    prompt = " ".join(p for p in prompt_parts if p).strip()
    raw_text = " ".join(lines).strip()
    max_answers = parse_max_answers(raw_text)
    kind = classify_question(prompt, labeled, options, raw_text)

    subquestions = [{"label": label, "prompt": text.strip()} for label, text in labeled if text.strip()]

    if kind == "mcq" and not options and subquestions:
        options = [{"label": item["label"].upper(), "text": item["prompt"]} for item in subquestions]
        subquestions = []

    entry = {
        "id": f"B{exam_year}_{section_id}_Q{question['number']:02d}",
        "number": question["number"],
        "kind": kind,
        "prompt": prompt or raw_text,
        "raw_text": raw_text,
    }
    if subquestions:
        entry["subquestions"] = subquestions
    if options:
        entry["options"] = options
    if max_answers is not None:
        entry["max_answers"] = max_answers
    return entry


def extract_batteries_from_exam(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    exam_year = parse_year(text)
    body = strip_frontmatter(text)
    batteries = []
    for section in detect_sections(body):
        q_blocks = split_question_blocks(section["body"])
        questions = [parse_question(q, exam_year, section["section_id"]) for q in q_blocks]
        batteries.append({
            "id": f"battery_{exam_year}_{section['section_id']}",
            "exam_id": path.stem,
            "exam_year": exam_year,
            "section_id": section["section_id"],
            "title": section["title"],
            "topic_hint": section["topic_hint"],
            "heading": section["heading"],
            "question_count": len(questions),
            "questions": questions,
            "fingerprint": sha1((path.stem + section['section_id'] + section['body'][:2000]).encode("utf-8")).hexdigest()[:12],
        })
    return batteries


def main():
    exam_filter = None
    if "--exam" in sys.argv:
        idx = sys.argv.index("--exam")
        if idx + 1 < len(sys.argv):
            exam_filter = sys.argv[idx + 1]

    all_batteries = []
    exam_count = 0
    for path in sorted(NORMALIZED_EXAMS.glob("*.md")):
        if exam_filter and exam_filter not in path.name:
            continue
        extracted = extract_batteries_from_exam(path)
        if extracted:
            exam_count += 1
            all_batteries.extend(extracted)

    payload = {
        "generated_from": "normalized exam markdown",
        "exam_count": exam_count,
        "battery_count": len(all_batteries),
        "batteries": all_batteries,
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Saved: {OUT_PATH}")
    print(f"Exams parsed: {exam_count}")
    print(f"Batteries: {len(all_batteries)}")
    for battery in all_batteries[:5]:
        print(f"  - {battery['id']}: {battery['question_count']} questions")


if __name__ == "__main__":
    main()
