"""
DIPS NotebookLM EN prompts
==========================
Master prompt + topic briefs for English audio overviews.
"""

from prompts.dips_notebooklm_es import NOTEBOOK_CARDS_ES as NOTEBOOK_CARDS_EN, SOURCE_IDS_FOR_NOTEBOOK

MASTER_PROMPT_EN = """
Create a Deep Dive Audio Overview in clear, natural English for a candidate preparing for Sweden's Diplomat Programme admission exam.

The output language is English. Do not teach vocabulary explicitly and do not spend time defining basic diplomatic terms unless needed for clarity. Assume the listener is already familiar with the field and wants substance, structure, and precision.

The goal is to help the listener understand the topic deeply and retain the most important facts, timelines, institutions, actors, legal concepts, and policy implications.

Style requirements:
- Use clear, idiomatic spoken English.
- Sound intelligent, calm, structured, and analytically useful.
- Prioritize explanation, comparison, chronology, and causal links.
- Avoid sounding like a glossary, a classroom worksheet, or a list of bullet points read aloud.
- Avoid repetitive bilingual translations unless absolutely necessary.
- Keep Swedish names, offices, and institutions accurate, but explain them naturally.
- When discussing controversial topics, remain precise, balanced, and fact-based.

Structure requirements:
1. Start with a strong opening that explains why this topic matters for the 2026 exam and for Swedish diplomacy.
2. Give the essential background and timeline.
3. Explain the key institutions, actors, and legal or political mechanisms.
4. Move to the current situation and why it matters now.
5. End with a compact synthesis: what the listener must remember for the exam.

Production requirements:
- Aim for a substantial, well-developed audio overview, not a short summary.
- Do not compress too aggressively.
- Repeat the most important dates, turning points, and distinctions when necessary for retention.
- Use the uploaded sources actively and prioritize the most authoritative sources.
- If sources differ in emphasis, present the mainstream interpretation supported by the strongest sources.

Important:
Focus on understanding over terminology.
Do not add artificial vocabulary sections.
Do not end with a long glossary.
Instead, reinforce key concepts by using them naturally throughout the episode.
Use fully natural English throughout.
""".strip()


def topic_brief_en(code: str) -> str:
    c = NOTEBOOK_CARDS_EN[code]
    lines = [
        f"TOPIC:\n{c['topic']}",
        "\nPRIORITY FOCUS:",
        *[f"- {x}" for x in c['priority_focus']],
        "\nKEY DATES / ACTORS / INSTITUTIONS:",
        *[f"- {x}" for x in c['key_dates']],
        *[f"- {x}" for x in c['key_actors']],
        *[f"- {x}" for x in c['institutions']],
        f"\nCURRENT RELEVANCE:\n{c['current_relevance']}",
        f"\nEXAM RISK:\n{c['exam_risk']}",
    ]
    if c.get('extra_rule'):
        lines.append(f"\nImportant:\n{c['extra_rule']}")
    return "\n".join(lines)


def full_prompt_en(code: str) -> str:
    return MASTER_PROMPT_EN + "\n\n" + topic_brief_en(code)
