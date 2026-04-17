"""
DIPS NotebookLM ES prompts
==========================
Master prompt + topic briefs for Spanish audio overviews.
"""

MASTER_PROMPT_ES = """
Create a Deep Dive Audio Overview in clear, natural Spanish for a candidate preparing for Sweden's Diplomat Programme admission exam.

The output language is Spanish. Do not teach vocabulary explicitly and do not spend time defining basic diplomatic terms unless needed for clarity. Assume the listener is already familiar with the field and wants substance, structure, and precision.

The goal is to help the listener understand the topic deeply and retain the most important facts, timelines, institutions, actors, legal concepts, and policy implications.

Style requirements:
- Use clear, idiomatic spoken Spanish.
- Sound intelligent, calm, structured, and analytically useful.
- Prioritize explanation, comparison, chronology, and causal links.
- Avoid sounding like a glossary, a classroom worksheet, or a list of bullet points read aloud.
- Avoid repetitive bilingual translations unless absolutely necessary.
- Keep Swedish names, offices, and institutions accurate, but explain them naturally in Spanish.
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
Use fully natural Spanish throughout. Do not drift into English except for proper names or official titles when strictly necessary.
""".strip()

NOTEBOOK_CARDS_ES = {
    "N01": {
        "title": "Svensk utrikespolitik och Utrikesdeklarationen 2026",
        "topic": "Swedish foreign policy doctrine and priorities in 2026, with special attention to the Foreign Policy Declaration and the transition from non-alignment to NATO membership.",
        "priority_focus": [
            "The historical arc from neutrality/non-alignment to NATO membership",
            "The priorities of the 2026 Foreign Policy Declaration",
            "Sweden's posture toward Ukraine, Russia, the EU, NATO, and key regions",
            "The relationship between security policy, trade, development cooperation, and Sweden's international profile",
        ],
        "key_dates": ["1814", "1995", "24 February 2022", "7 March 2024", "18 February 2026"],
        "key_actors": ["Maria Malmer Stenergard", "Ulf Kristersson", "Benjamin Dousa"],
        "institutions": ["UD", "NATO", "EU", "OSCE"],
        "current_relevance": "This is the clearest bridge between Swedish domestic priorities and the international system in 2026.",
        "exam_risk": "Likely essay topic or broad analysis question on Sweden's role in the world.",
    },
    "N02": {
        "title": "FN-systemet och FN-stadgan",
        "topic": "The United Nations system, the UN Charter, the Security Council, and Sweden's role in multilateral diplomacy.",
        "priority_focus": [
            "The six principal organs",
            "The most important Charter principles and articles",
            "The Security Council: structure, veto, legitimacy, and reform debate",
            "Sweden's historical and current role in the UN system",
            "Agenda 2030 as part of the multilateral architecture",
        ],
        "key_dates": ["1945", "2015"],
        "key_actors": ["Dag Hammarskjöld", "António Guterres"],
        "institutions": ["UNGA", "UNSC", "ECOSOC", "ICJ", "Secretariat"],
        "current_relevance": "The UN remains central to war, sanctions, legitimacy, development, and international law debates in 2026.",
        "exam_risk": "High probability of institutional or Charter-based questions.",
    },
    "N03": {
        "title": "EU:s institutioner och von der Leyen II-kommissionen",
        "topic": "The European Union's institutional system, the von der Leyen II Commission, and Sweden's role in the EU.",
        "priority_focus": [
            "The seven institutions and what each one does",
            "The current Commission and the most relevant portfolios",
            "Sweden's place in EU decision-making",
            "Enlargement, competitiveness, security, migration, and regulation as current priority areas",
        ],
        "key_dates": ["1951", "1957", "1992", "2009", "1 January 1995"],
        "key_actors": ["Ursula von der Leyen", "António Costa", "Kaja Kallas", "Jessika Roswall"],
        "institutions": ["Commission", "Council", "European Council", "Parliament", "CJEU", "ECB"],
        "current_relevance": "EU politics in 2026 are inseparable from security, enlargement, trade, and regulation.",
        "exam_risk": "Very likely section question or comparison question.",
    },
    "N04": {
        "title": "NATO och Sveriges medlemskap",
        "topic": "NATO's role in European security and Sweden's accession as a historic turning point in Swedish foreign and security policy.",
        "priority_focus": [
            "NATO's purpose, structure, and key treaty articles",
            "The 2022 Strategic Concept",
            "Finland's and Sweden's accession processes",
            "What Sweden contributes militarily and strategically",
            "NATO's role in deterrence against Russia and support to Ukraine",
        ],
        "key_dates": ["4 April 1949", "16 May 2022", "4 April 2023", "7 March 2024"],
        "key_actors": ["Mark Rutte", "Jens Stoltenberg", "Ulf Kristersson", "Pål Jonson"],
        "institutions": ["NAC", "Article 5", "Article 4", "SHAPE"],
        "current_relevance": "This is one of the defining changes in Swedish statecraft in the current era.",
        "exam_risk": "Extremely high.",
    },
    "N05": {
        "title": "Wienkonventionerna och diplomatisk praktik",
        "topic": "The Vienna Conventions as the legal foundation of diplomacy, consular practice, and treaty law.",
        "priority_focus": [
            "Diplomatic relations: functions, immunities, mission inviolability, persona non grata",
            "Consular relations and how consular status differs",
            "Treaty law: ratification, interpretation, reservations, entry into force, termination",
            "Swedish practice and why these rules matter in real diplomacy",
        ],
        "key_dates": ["1961", "1963", "1969"],
        "key_actors": ["VCDR", "VCCR", "VCLT"],
        "institutions": ["Regeringsformen Chapter 10"],
        "current_relevance": "This is core legal literacy for any diplomat and often appears in exam settings.",
        "exam_risk": "Classic legal competence question.",
    },
    "N06": {
        "title": "Ukraina 2022–2026",
        "topic": "Russia's war against Ukraine from the full-scale invasion in February 2022 to the diplomatic and military situation in 2026.",
        "priority_focus": [
            "The pre-war context from 2014 onward",
            "Major military and political turning points since February 2022",
            "Sweden's response: military, humanitarian, diplomatic, and strategic",
            "The EU and NATO response",
            "The negotiation phase and strategic uncertainty in 2025–2026",
        ],
        "key_dates": ["2014", "24 February 2022"],
        "key_actors": ["Zelensky", "Putin", "Lavrov"],
        "institutions": ["EU", "NATO", "sanctions", "frozen assets"],
        "current_relevance": "This war reshaped European security and Swedish foreign policy.",
        "exam_risk": "Very likely essay or current-affairs analysis topic.",
    },
    "N07": {
        "title": "Mellanöstern: Gaza, Iran, Libanon, Syrien efter Assad",
        "topic": "The Middle East after 7 October 2023, including the Gaza war, regional escalation, and the political consequences of the fall of the Assad regime.",
        "priority_focus": [
            "The 7 October attack and the war in Gaza",
            "The humanitarian and legal dimensions",
            "Hezbollah, Lebanon, Iran-Israel escalation",
            "The collapse of Assad's rule and regional realignment",
            "Sweden's and Europe's positions",
        ],
        "key_dates": ["7 October 2023"],
        "key_actors": ["Hamas", "Netanyahu", "Hezbollah", "Iran"],
        "institutions": ["ICJ", "ICC", "EU"],
        "current_relevance": "This remains one of the most exam-relevant geopolitical theatres because it combines war, diplomacy, international law, and regional power politics.",
        "exam_risk": "High, especially as an essay or synthesis question.",
    },
    "N08": {
        "title": "Regeringen Kristersson och svensk politik 2022–2026",
        "topic": "Sweden's political system, the Kristersson government, the Tidö framework, and the domestic political landscape ahead of the 2026 election.",
        "priority_focus": [
            "How the Swedish political system works",
            "The composition and logic of the Kristersson government",
            "The most important ministers and portfolios",
            "Key domestic issues shaping the political environment before the 2026 election",
        ],
        "key_dates": ["11 September 2022", "March 2024", "September 2026"],
        "key_actors": ["Ulf Kristersson", "Maria Malmer Stenergard", "Elisabeth Svantesson", "Pål Jonson"],
        "institutions": ["Riksdag", "Speaker", "government offices", "major agencies"],
        "current_relevance": "Essential for the Sweden section of the exam and for understanding how foreign policy is anchored at home.",
        "exam_risk": "High in factual and institutional sections.",
    },
    "N09": {
        "title": "Trump II och den transatlantiska relationen",
        "topic": "Donald Trump's second presidency and its implications for transatlantic relations, NATO, Ukraine, trade, and Swedish strategic choices.",
        "priority_focus": [
            "The administration's foreign-policy orientation",
            "Pressure on Europe over defense spending and dependence",
            "Trade frictions, tariffs, and industrial policy tensions",
            "Implications for Ukraine policy and European security",
            "What this means specifically for Sweden",
        ],
        "key_dates": ["20 January 2025"],
        "key_actors": ["Donald Trump", "Marco Rubio", "Pete Hegseth", "JD Vance"],
        "institutions": ["NATO", "EU", "White House", "USTR"],
        "current_relevance": "This topic affects nearly every part of Europe's security and economic environment.",
        "exam_risk": "Very plausible essay topic in 2026.",
    },
    "N10": {
        "title": "Folkrätt: ICJ, ICC, Europadomstolen och CJEU",
        "topic": "The essential architecture of international law, with special emphasis on the difference between the ICJ and the ICC and on the most important current cases.",
        "priority_focus": [
            "The difference between state responsibility and individual criminal responsibility",
            "What the ICJ does and how its jurisdiction works",
            "What the ICC does and how its jurisdiction works",
            "How the ECtHR and the CJEU differ from both",
            "Why these distinctions matter in current conflicts and legal debates",
        ],
        "key_dates": ["1945", "1950", "1998", "2002"],
        "key_actors": ["South Africa v. Israel", "Ukraine-related ICC warrants"],
        "institutions": ["ICJ", "ICC", "ECtHR", "CJEU"],
        "current_relevance": "This is one of the most common conceptual traps and therefore highly testable.",
        "exam_risk": "Very high.",
        "extra_rule": "Return to the ICJ/ICC distinction repeatedly and explain it through examples, not just definitions.",
    },
}

SOURCE_IDS_FOR_NOTEBOOK = {
    'N01': ['utrikesdeklarationen_2026', 'utrikesdeklarationen_2025', 'nationell_sakerhetsstrategi_2024', 'dips_qa_2026'],
    'N02': ['un_charter', 'udhr'],
    'N03': ['eu_treaty_teu', 'res_qa_placeholder'],
    'N04': ['nato_treaty', 'dips_exam_2025'],
    'N05': ['vienna_diplomatic_1961', 'vienna_consular_1963', 'vienna_treaties_1969'],
    'N06': ['utrikesdeklarationen_2026', 'nationell_sakerhetsstrategi_2024'],
    'N07': ['echr_convention'],
    'N08': ['dips_qa_2026'],
    'N09': ['dips_exam_2025'],
    'N10': ['un_charter', 'echr_convention'],
}


def topic_brief_es(code: str) -> str:
    c = NOTEBOOK_CARDS_ES[code]
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

def full_prompt_es(code: str) -> str:
    return MASTER_PROMPT_ES + "\n\n" + topic_brief_es(code)
