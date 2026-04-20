"""
DIPS 2026 Världsledare Plansch v3 - WITH VISUAL ANCHORS

Builds an A3 plansch where each leader has a circular visual anchor.
- If a photo exists at photos/{key}.jpg, it's embedded
- Otherwise, a gradient initial avatar is generated

Run: python3 build_plansch_v3.py
Output: DIPS_2026_Varldsledare_v3.pdf
"""
import os
import base64
import weasyprint

PHOTO_DIR = "photos"
OUTPUT_HTML = "plansch_v3.html"
OUTPUT_PDF = "DIPS_2026_Varldsledare_v3.pdf"

# Region palette
REGION = {
    'norden':  ('#005293', '#2b7fc7'),
    'nordam':  ('#b22234', '#e85a6a'),
    'storm':   ('#003399', '#5575c7'),
    'ovriga':  ('#4a7c59', '#7eaf8e'),
    'russ':    ('#6a1b9a', '#a44bc7'),
    'asien':   ('#d4691e', '#f09456'),
    'mena':    ('#8b5e00', '#c69523'),
    'afrika':  ('#7a3b2e', '#b0694f'),
    'latam':   ('#0c8346', '#45b572'),
    'org':     ('#1a1a1a', '#5a5a5a'),
}

def photo_or_avatar(key, initials, region):
    """Return HTML for portrait: real photo if available, else initial avatar."""
    jpg_path = os.path.join(PHOTO_DIR, f"{key}.jpg")
    png_path = os.path.join(PHOTO_DIR, f"{key}.png")
    path = jpg_path if os.path.exists(jpg_path) else (png_path if os.path.exists(png_path) else None)
    if path:
        with open(path, 'rb') as f:
            data = base64.b64encode(f.read()).decode()
        ext = 'jpeg' if path.endswith('.jpg') else 'png'
        return f'<span class="portrait"><img src="data:image/{ext};base64,{data}" alt="{initials}"/></span>'
    # Generate initial-avatar
    c1, c2 = REGION[region]
    return f'''<span class="portrait avatar" style="background: radial-gradient(circle at 30% 30%, {c2}, {c1});">{initials}</span>'''


# ============ DATA ============
# Each leader: (key, initials, region, flag, land, leader_name, role, sub_line, note/alert)
# role: pm, pres, kansler, taoiseach, mon, de-facto, trans

LEADERS = {
    "norden_baltikum": {
        "title": "Norden & Baltikum",
        "tag": "Högsta prioritet — sitta perfekt",
        "region_class": "norden",
        "big": True,
        "rows": [
            ("kristersson", "UK", "norden", "🇸🇪", "SVERIGE", "Ulf Kristersson", "PM",
             "<b>Parti:</b> Moderaterna (M) · <b>UM:</b> Maria Malmer Stenergard (M)", None),
            ("orpo", "PO", "norden", "🇫🇮", "FINLAND", "Petteri Orpo", "PM",
             "<b>Parti:</b> Samlingspartiet / Kansallinen Kokoomus (Kok.) · <b>Pres:</b> Alexander Stubb · <b>UM:</b> Elina Valtonen",
             "note:Dubbelspårigt: PM + pres båda provrelevanta"),
            ("store", "JS", "norden", "🇳🇴", "NORGE", "Jonas Gahr Støre", "PM",
             "<b>Parti:</b> Arbeiderpartiet (Ap) · <b>UM:</b> Espen Barth Eide (Ap)", None),
            ("frederiksen", "MF", "norden", "🇩🇰", "DANMARK", "Mette Frederiksen", "PM",
             "<b>Parti:</b> Socialdemokratiet (S) · <b>UM:</b> Lars Løkke Rasmussen (M)", None),
            ("frostadottir", "KF", "norden", "🇮🇸", "ISLAND", "Kristrún Frostadóttir", "PM",
             "<b>Parti:</b> Samfylkingin / Social Democratic Alliance (S) · <b>Pres:</b> Halla Tómasdóttir", None),
            ("michal", "KM", "norden", "🇪🇪", "ESTLAND", "Kristen Michal", "PM",
             "<b>Parti:</b> Reformierakond / Reformpartiet (RE) · <b>UM:</b> Margus Tsahkna", None),
            ("silina", "ES", "norden", "🇱🇻", "LETTLAND", "Evika Siliņa", "PM",
             "<b>Parti:</b> Jaunā Vienotība / New Unity (JV) · <b>UM:</b> Baiba Braže", None),
            ("ruginiene", "IR", "norden", "🇱🇹", "LITAUEN", "Inga Ruginienė", "PM",
             "<b>Parti:</b> Lietuvos socialdemokratų partija (LSDP) · <b>Pres:</b> Nausėda · <b>UM:</b> K. Budrys",
             "note:Ny PM sedan 25 sep 2025 (efter Paluckas)"),
        ],
    },
    "nordamerika": {
        "title": "Nordamerika",
        "tag": "Stormakt",
        "region_class": "nordam",
        "big": False,
        "rows": [
            ("trump", "DT", "nordam", "🇺🇸", "USA", "Donald J. Trump", "PRES",
             "<b>Parti:</b> Republican Party (GOP) · <b>VP:</b> JD Vance · <b>State:</b> Marco Rubio · <b>Försv:</b> Hegseth", None),
            ("carney", "MC", "nordam", "🇨🇦", "KANADA", "Mark Carney", "PM",
             "<b>Parti:</b> Liberal Party of Canada (LPC) · sedan mars 2025 · majoritet apr 2026", None),
            ("sheinbaum", "CS", "nordam", "🇲🇽", "MEXIKO", "Claudia Sheinbaum", "PRES",
             "<b>Parti:</b> Movimiento Regeneración Nacional (Morena) · första kvinnan", None),
        ],
    },
    "stora_eu_uk": {
        "title": "Stora EU & UK",
        "tag": "Må-sitta-absolut",
        "region_class": "storm",
        "big": True,
        "rows": [
            ("merz", "FM", "storm", "🇩🇪", "TYSKLAND", "Friedrich Merz", "KANSLER",
             "<b>Parti:</b> Christlich Demokratische Union (CDU) · sedan maj 2025 · koalition m. SPD", None),
            ("macron", "EM", "storm", "🇫🇷", "FRANKRIKE", "Emmanuel Macron", "PRES",
             "<b>Parti:</b> Renaissance (RE) · <b>PM:</b> Sébastien Lecornu · <b>UM:</b> JN Barrot",
             "note:Provfälla: pres styr UP, INTE PM"),
            ("starmer", "KS", "storm", "🇬🇧", "UK", "Keir Starmer", "PM",
             "<b>Parti:</b> Labour Party (Lab) · sedan juli 2024 · <b>UM:</b> David Lammy", None),
            ("meloni", "GM", "storm", "🇮🇹", "ITALIEN", "Giorgia Meloni", "PM",
             "<b>Parti:</b> Fratelli d'Italia (FdI) · sedan okt 2022", None),
            ("sanchez", "PS", "storm", "🇪🇸", "SPANIEN", "Pedro Sánchez", "PM",
             "<b>Parti:</b> Partido Socialista Obrero Español (PSOE) · minoritetsregering", None),
            ("jetten", "RJ", "storm", "🇳🇱", "NEDERLÄNDERNA", "Rob Jetten", "PM",
             "<b>Parti:</b> Democrats 66 (D66) · sedan 23 feb 2026",
             "note:NY: efterträdde Schoof (PVV-krasch juni 2025)"),
            ("tusk", "DT2", "storm", "🇵🇱", "POLEN", "Donald Tusk", "PM",
             "<b>Parti:</b> Platforma Obywatelska / Civic Platform (PO) · <b>Pres:</b> Karol Nawrocki · <b>UM:</b> R. Sikorski",
             "note:Provfälla: olika läger PM vs pres"),
            ("dewever", "BD", "storm", "🇧🇪", "BELGIEN", "Bart De Wever", "PM",
             "<b>Parti:</b> Nieuw-Vlaamse Alliantie (N-VA) · sedan feb 2025", None),
        ],
    },
    "ovriga_eu": {
        "title": "Övriga EU + Ukraina",
        "tag": "Viktiga",
        "region_class": "ovriga",
        "big": False,
        "rows": [
            ("zelensky", "VZ", "ovriga", "🇺🇦", "UKRAINA", "Volodymyr Zelensky", "PRES",
             "<b>Parti:</b> Sluha Narodu / Servant of the People (SN) · <b>UM:</b> Andrii Sybiha · <b>PM:</b> Yulia Svyrydenko", None),
            ("babis", "AB", "ovriga", "🇨🇿", "TJECKIEN", "Andrej Babiš", "PM",
             "<b>Parti:</b> ANO 2011 (ANO) · sedan 9 dec 2025 (INTE Fiala)",
             "alert:NYTT: skifte fr. Fiala, EU/Ukr-skeptisk"),
            ("orban", "VO", "ovriga", "🇭🇺", "UNGERN", "Viktor Orbán", "PM (AVGÅR)",
             "<b>Parti:</b> Fidesz - Magyar Polgari Szovetseg (Fidesz) · <b>Tillträder:</b> Péter Magyar (Tisza)",
             "alert:⚠ MAKTSKIFTE: Tisza vann 2/3 majoritet 12 apr 2026"),
            ("bolojan", "IB", "ovriga", "🇷🇴", "RUMÄNIEN", "Ilie Bolojan", "PM",
             "<b>Parti:</b> Partidul National Liberal (PNL) · <b>Pres:</b> Nicusor Dan", None),
            ("stocker", "CS2", "ovriga", "🇦🇹", "ÖSTERRIKE", "Christian Stocker", "KANSLER",
             "<b>Parti:</b> Osterreichische Volkspartei (OVP) · OVP-SPO-NEOS sedan mars 2025", None),
            ("montenegro", "LM", "ovriga", "🇵🇹", "PORTUGAL", "Luís Montenegro", "PM",
             "<b>Parti:</b> Partido Social Democrata (PSD) · <b>Pres:</b> Antonio Jose Seguro (PS)", None),
            ("mitsotakis", "KM2", "ovriga", "🇬🇷", "GREKLAND", "Kyriakos Mitsotakis", "PM",
             "<b>Parti:</b> Nea Dimokratia / New Democracy (ND)", None),
            ("martin", "MM", "ovriga", "🇮🇪", "IRLAND", "Micheál Martin", "TAOISEACH",
             "<b>Parti:</b> Fianna Fail (FF) · sedan jan 2025", None),
            ("gyurov", "AG", "ovriga", "🇧🇬", "BULGARIEN", "Andrey Gyurov", "PM (tillf.)",
             "<b>Parti:</b> Prodalzhavame Promyanata / We Continue the Change (PP) · <b>Pres:</b> Iliana Yotova",
             "alert:⚠ VAL IDAG 19 APR 2026 — Radev favorit"),
        ],
    },
    "ryssland_balkan": {
        "title": "Ryssland & Balkan",
        "tag": "Spänning",
        "region_class": "russ",
        "big": False,
        "rows": [
            ("putin", "VP", "russ", "🇷🇺", "RYSSLAND", "Vladimir Putin", "PRES",
             "<b>Parti:</b> Yedinaya Rossiya / United Russia (UR) · <b>UM:</b> Sergej Lavrov · <b>PM:</b> Misjustin", None),
            ("lukashenko", "AL", "russ", "🇧🇾", "BELARUS", "Aleksandr Lukasjenko", "PRES",
             "<b>Parti:</b> ingen formell partibindning · nära Moskva", None),
            ("sandu", "MS", "russ", "🇲🇩", "MOLDAVIEN", "Maia Sandu", "PRES",
             "<b>Parti:</b> Partidul Actiune si Solidaritate (PAS) · EU-orienterad", None),
            ("erdogan", "RE", "russ", "🇹🇷", "TURKIET", "Recep Tayyip Erdoğan", "PRES",
             "<b>Parti:</b> Adalet ve Kalkinma Partisi (AKP) · presidentstyre", None),
            ("vucic", "AV", "russ", "🇷🇸", "SERBIEN", "Aleksandar Vučić", "PRES",
             "<b>Parti:</b> Srpska napredna stranka (SNS) · dominerande figur", None),
            ("plenkovic", "AP", "russ", "🇭🇷", "KROATIEN", "Andrej Plenković", "PM",
             "<b>Parti:</b> Hrvatska demokratska zajednica (HDZ) · EU/NATO-kurs", None),
        ],
    },
    "asien": {
        "title": "Asien & Pacific",
        "tag": "Strategiska tyngdpunkter",
        "region_class": "asien",
        "big": True,
        "rows": [
            ("xi", "XJ", "asien", "🇨🇳", "KINA", "Xi Jinping", "PRES",
             "<b>Parti:</b> Communist Party of China (CPC/CCP) · <b>PM:</b> Li Qiang · <b>UM:</b> Wang Yi",
             "note:Triaden: Xi först, PM + UM nivå 2"),
            ("takaichi", "ST", "asien", "🇯🇵", "JAPAN", "Sanae Takaichi", "PM",
             "<b>Parti:</b> Liberal Democratic Party (LDP) · första kvinnan · sedan okt 2025", None),
            ("lee", "LJ", "asien", "🇰🇷", "SYDKOREA", "Lee Jae-myung", "PRES",
             "<b>Parti:</b> Democratic Party of Korea (DPK) · sedan juni 2025", None),
            ("kim", "KJ", "asien", "🇰🇵", "NORDKOREA", "Kim Jong-un", "HÖGSTA L.",
             "<b>Parti:</b> Workers' Party of Korea (WPK) · generalsekr.", None),
            ("modi", "NM", "asien", "🇮🇳", "INDIEN", "Narendra Modi", "PM",
             "<b>Parti:</b> Bharatiya Janata Party (BJP) · <b>UM:</b> S. Jaishankar · <b>Pres:</b> Murmu", None),
            ("sharif", "SS", "asien", "🇵🇰", "PAKISTAN", "Shehbaz Sharif", "PM",
             "<b>Parti:</b> Pakistan Muslim League (N) (PML-N) · <b>Pres:</b> Asif Ali Zardari", None),
            ("prabowo", "PS2", "asien", "🇮🇩", "INDONESIEN", "Prabowo Subianto", "PRES",
             "<b>Parti:</b> Gerindra / Great Indonesia Movement Party · sedan okt 2024", None),
            ("albanese", "AA", "asien", "🇦🇺", "AUSTRALIEN", "Anthony Albanese", "PM",
             "<b>Parti:</b> Australian Labor Party (ALP) · omvald maj 2025", None),
        ],
    },
    "mena": {
        "title": "Mellanöstern & MENA",
        "tag": "Provkritisk",
        "region_class": "mena",
        "big": False,
        "rows": [
            ("netanyahu", "BN", "mena", "🇮🇱", "ISRAEL", "Benjamin Netanyahu", "PM",
             "<b>Parti:</b> Likud · <b>Pres:</b> Isaac Herzog", None),
            ("abbas", "MA", "mena", "🇵🇸", "PALESTINA", "Mahmoud Abbas", "PRES",
             "<b>Parti:</b> Fatah / Palestinian National Liberation Movement · PA / Ramallah", None),
            ("pezeshkian", "MP", "mena", "🇮🇷", "IRAN", "Masoud Pezeshkian", "PRES",
             "<b>Block:</b> reformistisk oberoende · <b>Rahbar:</b> Ali Khamenei (HÖGSTA)",
             "note:Provfälla: Khamenei styr, ej pres."),
            ("mbs", "MB", "mena", "🇸🇦", "SAUDIARABIEN", "Mohammed bin Salman", "DE FACTO",
             "Kungahus: Al Saud · Kronprins & PM · <b>Kung:</b> Salman",
             "note:Provfälla: MBS styr i praktiken"),
            ("sisi", "AS2", "mena", "🇪🇬", "EGYPTEN", "Abdel Fattah al-Sisi", "PRES",
             "Partilos militärbakgrund · sedan 2014", None),
            ("sharaa", "AS3", "mena", "🇸🇾", "SYRIEN", "Ahmad al-Sharaa", "ÖVERGÅNG",
             "HTS-bakgrund · president under overgång (PM-post avskaffad)",
             "alert:Assad föll 8 dec 2024 · al-Sharaa pres 29 jan 2025"),
            ("aoun", "JA", "mena", "🇱🇧", "LIBANON", "Joseph Aoun", "PRES",
             "Partilos / armebakgrund · <b>PM:</b> Nawaf Salam · konfessionell", None),
            ("abdullah", "AII", "mena", "🇯🇴", "JORDANIEN", "Abdullah II", "KUNG",
             "Hashemitiska dynastin", None),
            ("akhannouch", "AA2", "mena", "🇲🇦", "MAROCKO", "Aziz Akhannouch", "PM",
             "<b>Parti:</b> Rassemblement National des Independants (RNI) · <b>Kung:</b> Mohammed VI", None),
        ],
    },
    "afrika": {
        "title": "Afrika",
        "tag": "Urval",
        "region_class": "afrika",
        "big": False,
        "rows": [
            ("ramaphosa", "CR", "afrika", "🇿🇦", "SYDAFRIKA", "Cyril Ramaphosa", "PRES",
             "<b>Parti:</b> African National Congress (ANC) · G20-ordf. 2025", None),
            ("tinubu", "BT", "afrika", "🇳🇬", "NIGERIA", "Bola Tinubu", "PRES",
             "<b>Parti:</b> All Progressives Congress (APC) · sedan maj 2023", None),
            ("ruto", "WR", "afrika", "🇰🇪", "KENYA", "William Ruto", "PRES",
             "<b>Parti:</b> United Democratic Alliance (UDA)", None),
            ("abiy", "AA3", "afrika", "🇪🇹", "ETIOPIEN", "Abiy Ahmed", "PM",
             "<b>Parti:</b> Prosperity Party (PP) · Nobels fredspris 2019", None),
            ("kagame", "PK", "afrika", "🇷🇼", "RWANDA", "Paul Kagame", "PRES",
             "<b>Parti:</b> Rwandan Patriotic Front (RPF)", None),
            ("tshisekedi", "FT", "afrika", "🇨🇩", "DR KONGO", "Félix Tshisekedi", "PRES",
             "<b>Parti:</b> Union for Democracy and Social Progress (UDPS) · M23/Rwanda-spänning", None),
            ("burhan", "AB2", "afrika", "🇸🇩", "SUDAN", "Abdel Fattah al-Burhan", "DE FACTO",
             "Sudanese Armed Forces (SAF) · krig mot RSF sedan 2023", None),
        ],
    },
    "latam": {
        "title": "Latinamerika",
        "tag": "Presidentstyrt",
        "region_class": "latam",
        "big": False,
        "rows": [
            ("lula", "LL", "latam", "🇧🇷", "BRASILIEN", "Luiz Inácio Lula da Silva", "PRES",
             "<b>Parti:</b> Partido dos Trabalhadores (PT) · COP30-värd 2025", None),
            ("milei", "JM", "latam", "🇦🇷", "ARGENTINA", "Javier Milei", "PRES",
             "<b>Parti:</b> La Libertad Avanza (LLA) · libertarian", None),
            ("boric", "GB", "latam", "🇨🇱", "CHILE", "Gabriel Boric", "PRES",
             "<b>Parti:</b> Frente Amplio (FA)", None),
            ("petro", "GP", "latam", "🇨🇴", "COLOMBIA", "Gustavo Petro", "PRES",
             "<b>Parti:</b> Pacto Histórico (PH)", None),
            ("maduro", "NM2", "latam", "🇻🇪", "VENEZUELA", "Nicolás Maduro", "PRES",
             "<b>Parti:</b> Partido Socialista Unido de Venezuela (PSUV) · omstridd", None),
            ("diazcanel", "MD", "latam", "🇨🇺", "KUBA", "Miguel Díaz-Canel", "PRES",
             "<b>Parti:</b> Partido Comunista de Cuba (PCC)", None),
        ],
    },
}

# Organisations-chefer
ORG_CHIEFS = [
    ("guterres", "AG2", "FN", "António Guterres"),
    ("rutte", "MR", "NATO", "Mark Rutte"),
    ("vdl", "UvL", "EU-kom.", "Ursula von der Leyen"),
    ("costa", "AC", "Eur.rådet", "António Costa"),
    ("kallas", "KK", "HR/VP", "Kaja Kallas"),
    ("metsola", "RM", "Europarl.", "Roberta Metsola"),
    ("lagarde", "CL", "ECB", "Christine Lagarde"),
    ("okonjo", "NO", "WTO", "N. Okonjo-Iweala"),
    ("georgieva", "KG", "IMF", "Kristalina Georgieva"),
    ("banga", "AjB", "VB", "Ajay Banga"),
]

# Role to CSS class
ROLE_CLASS = {
    "PM": "pm", "KANSLER": "pm", "TAOISEACH": "pm",
    "PRES": "pres",
    "KUNG": "mon",
    "DE FACTO": "de-facto", "HÖGSTA L.": "de-facto",
    "ÖVERGÅNG": "trans",
    "PM (AVGÅR)": "pm", "PM (tillf.)": "pm",
}


def render_country(row):
    key, initials, region, flag, land, name, role, sub_line, extra = row
    role_class = ROLE_CLASS.get(role.split("(")[0].strip(), "pm")
    portrait = photo_or_avatar(key, initials, region)
    extra_html = ""
    if extra:
        if extra.startswith("note:"):
            extra_html = f'<div class="note">{extra[5:]}</div>'
        elif extra.startswith("alert:"):
            extra_html = f'<div class="alert">{extra[6:]}</div>'
    return f'''
    <div class="country">
      {portrait}
      <div class="flag">{flag}</div>
      <div class="info">
        <div class="land">{land}</div>
        <div><span class="leader">{name}</span> <span class="role {role_class}">{role}</span></div>
        <div class="sub-line">{sub_line}</div>
        {extra_html}
      </div>
    </div>'''


def render_region(key, data):
    big_class = " big" if data["big"] else ""
    inner = ""
    if data["big"] and len(data["rows"]) >= 6:
        # Two columns inside big regions
        inner = '<div class="two-col-grid">'
        for row in data["rows"]:
            inner += render_country(row)
        inner += '</div>'
    else:
        for row in data["rows"]:
            inner += render_country(row)
    return f'''
    <div class="region {data["region_class"]}{big_class}">
      <div class="region-title">{data["title"]} <span class="tag">{data["tag"]}</span></div>
      {inner}
    </div>'''


def render_orgs():
    html = '<div class="orgs-title">★ Chefer för internationella organisationer 2026 ★</div>'
    html += '<div class="orgs-grid">'
    for key, initials, org, name in ORG_CHIEFS:
        portrait = photo_or_avatar(key, initials, "org")
        html += f'''
        <div class="org-item">
          {portrait}
          <div><span class="org-tag">{org}</span> {name}</div>
        </div>'''
    html += '</div>'
    return html


# ============ CSS ============
CSS = """
@page { size: A3 portrait; margin: 7mm; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  font-family: "DejaVu Sans", "Noto Sans", sans-serif;
  font-size: 7.8pt;
  line-height: 1.2;
  color: #1a1a1a;
  background: #fafaf7;
}
.page { page-break-after: always; position: relative; }
.page:last-child { page-break-after: auto; }

/* HEADER */
header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: 2mm 4mm 1.5mm;
  border-bottom: 2pt solid #1a1a1a;
  margin-bottom: 2mm;
}
.title-block h1 {
  font-family: "DejaVu Serif", Georgia, serif;
  font-size: 22pt;
  font-weight: 900;
  letter-spacing: -0.5pt;
  line-height: 0.95;
}
.title-block h1 span { color: #c1272d; }
.title-block .sub {
  font-size: 8.5pt;
  margin-top: 0.8mm;
  color: #555;
  font-style: italic;
}
.meta-block {
  text-align: right;
  font-size: 7pt;
  color: #333;
}
.meta-block .date {
  font-weight: 700;
  font-size: 8.5pt;
  color: #c1272d;
}
.meta-block .verified {
  background: #1a1a1a;
  color: #fafaf7;
  padding: 0.8mm 1.8mm;
  margin-top: 0.8mm;
  display: inline-block;
  font-size: 6.5pt;
  letter-spacing: 0.5pt;
  text-transform: uppercase;
}

/* LEGEND */
.legend {
  display: flex;
  gap: 3mm;
  padding: 1mm 4mm;
  font-size: 6.8pt;
  background: #f0ede5;
  border-left: 3pt solid #1a1a1a;
  margin: 0 0 1.5mm;
  flex-wrap: wrap;
  align-items: center;
}
.legend b { font-size: 7.2pt; margin-right: 1.5mm; }
.legend-item { display: inline-flex; align-items: center; gap: 1mm; }
.dot { width: 2.2mm; height: 2.2mm; border-radius: 50%; display: inline-block; }
.dot.pm { background: #2d6a7a; }
.dot.pres { background: #c1272d; }
.dot.mon { background: #b8860b; }
.dot.de-facto { background: #6a1b9a; }
.dot.trans { background: #555; }

/* GRID */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5mm;
  padding: 0 4mm;
}
.region {
  border: 1pt solid #1a1a1a;
  background: #fff;
  padding: 1.1mm 1.5mm 1.5mm;
  break-inside: avoid;
}
.region.big { grid-column: span 2; }

.region-title {
  font-family: "DejaVu Serif", Georgia, serif;
  font-size: 9pt;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.6pt;
  padding-bottom: 0.6mm;
  margin-bottom: 1.0mm;
  border-bottom: 1.5pt solid #1a1a1a;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.region-title .tag {
  font-family: "DejaVu Sans", sans-serif;
  font-size: 6.3pt;
  font-weight: 400;
  color: #888;
  letter-spacing: 0;
  text-transform: none;
  font-style: italic;
}

.region.norden { border-top: 3pt solid #005293; }
.region.norden .region-title { color: #005293; }
.region.storm { border-top: 3pt solid #003399; }
.region.storm .region-title { color: #003399; }
.region.ovriga { border-top: 3pt solid #4a7c59; }
.region.ovriga .region-title { color: #4a7c59; }
.region.nordam { border-top: 3pt solid #b22234; }
.region.nordam .region-title { color: #b22234; }
.region.russ { border-top: 3pt solid #6a1b9a; }
.region.russ .region-title { color: #6a1b9a; }
.region.asien { border-top: 3pt solid #d4691e; }
.region.asien .region-title { color: #d4691e; }
.region.mena { border-top: 3pt solid #8b5e00; }
.region.mena .region-title { color: #8b5e00; }
.region.latam { border-top: 3pt solid #0c8346; }
.region.latam .region-title { color: #0c8346; }
.region.afrika { border-top: 3pt solid #7a3b2e; }
.region.afrika .region-title { color: #7a3b2e; }

.two-col-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 3mm;
}

/* COUNTRY ROW */
.country {
  display: grid;
  grid-template-columns: 9mm 5mm 1fr;
  gap: 1.2mm;
  padding: 0.45mm 0;
  border-bottom: 0.3pt dotted #ccc;
  align-items: start;
}
.country:last-child { border-bottom: none; }

.portrait {
  width: 8mm;
  height: 8mm;
  border-radius: 50%;
  display: block;
  overflow: hidden;
  position: relative;
  border: 0.8pt solid #1a1a1a;
}
.portrait img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.portrait.avatar {
  font-family: "DejaVu Serif", Georgia, serif;
  font-weight: 900;
  font-size: 6.5pt;
  color: white;
  text-align: center;
  line-height: 8mm;
  letter-spacing: -0.3pt;
  text-shadow: 0.3pt 0.3pt 0.5pt rgba(0,0,0,0.3);
}

.flag {
  font-size: 10pt;
  font-family: "Noto Color Emoji", "DejaVu Sans";
  text-align: center;
  line-height: 1.3;
  padding-top: 0.2mm;
}
.info { font-size: 6.9pt; line-height: 1.14; }
.land {
  font-weight: 700;
  font-size: 7.4pt;
  text-transform: uppercase;
  letter-spacing: 0.3pt;
}
.leader { font-weight: 600; display: inline; }
.role {
  display: inline-block;
  font-size: 5.8pt;
  font-weight: 700;
  padding: 0.1mm 0.7mm;
  border-radius: 1mm;
  margin-left: 0.8mm;
  vertical-align: 1px;
  letter-spacing: 0.3pt;
  color: white;
}
.role.pm { background: #2d6a7a; }
.role.pres { background: #c1272d; }
.role.mon { background: #b8860b; }
.role.de-facto { background: #6a1b9a; }
.role.trans { background: #555; }

.sub-line { font-size: 5.7pt; color: #555; margin-top: 0.15mm; }
.sub-line b { font-weight: 700; color: #333; }

.note {
  font-size: 6.2pt;
  color: #8a3a1e;
  font-style: italic;
  margin-top: 0.3mm;
  padding: 0.2mm 1.2mm;
  background: #fff4e6;
  border-left: 1.5pt solid #d4691e;
}
.alert {
  font-size: 6.2pt;
  color: #c1272d;
  font-weight: 700;
  margin-top: 0.3mm;
  padding: 0.2mm 1.2mm;
  background: #fff0f0;
  border-left: 1.5pt solid #c1272d;
}

/* ORG CHEFER */
.orgs {
  margin: 2mm 4mm 0;
  padding: 1.5mm 2.5mm;
  background: #1a1a1a;
  color: #fafaf7;
}
.orgs-title {
  font-family: "DejaVu Serif", Georgia, serif;
  font-weight: 900;
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 1pt;
  margin-bottom: 1.5mm;
  color: #f0d043;
  text-align: center;
}
.orgs-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.5mm 2.5mm;
  font-size: 6.8pt;
}
.org-item {
  display: grid;
  grid-template-columns: 8mm 1fr;
  gap: 1.5mm;
  align-items: center;
}
.org-item .portrait {
  width: 7mm; height: 7mm;
  font-size: 5.5pt;
  line-height: 7mm;
}
.org-tag {
  color: #f0d043;
  font-weight: 700;
  display: block;
  font-size: 6.5pt;
  letter-spacing: 0.3pt;
}

footer {
  margin: 1.5mm 4mm 0;
  display: flex;
  justify-content: space-between;
  font-size: 6pt;
  color: #888;
  border-top: 0.5pt solid #ccc;
  padding-top: 0.6mm;
}

/* ========== PAGE 2 ========== */
.page2 header .title-block h1 span { color: #0c8346; }

.section-title {
  font-family: "DejaVu Serif", Georgia, serif;
  font-size: 12pt;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.6pt;
  margin: 2.5mm 4mm 1.2mm;
  padding-bottom: 0.7mm;
  border-bottom: 2pt solid #1a1a1a;
}

.two-col {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 3mm;
  padding: 0 4mm;
  margin-bottom: 2mm;
}
.priority-box {
  background: #fff;
  border: 1pt solid #1a1a1a;
  border-top: 4pt solid #c1272d;
  padding: 2.5mm;
}
.priority-box h3 {
  font-size: 8.5pt;
  font-weight: 900;
  margin-bottom: 1.2mm;
  text-transform: uppercase;
  letter-spacing: 0.5pt;
}
.priority-box p {
  font-size: 7pt;
  line-height: 1.35;
  margin-bottom: 1.2mm;
}
.priority-box .tier {
  font-weight: 700;
  color: #c1272d;
}
.triads {
  background: #fff;
  border: 1pt solid #1a1a1a;
  border-top: 4pt solid #003399;
  padding: 2.5mm;
}
.triads h3 {
  font-size: 8.5pt;
  font-weight: 900;
  margin-bottom: 1.2mm;
  text-transform: uppercase;
  letter-spacing: 0.5pt;
}
.triads ul { list-style: none; font-size: 7pt; }
.triads li {
  padding: 0.8mm 0;
  border-bottom: 0.3pt dotted #ccc;
}
.triads li:last-child { border: none; }
.triads .country-name {
  font-weight: 700;
  color: #003399;
  display: inline-block;
  min-width: 21mm;
}

.traps {
  margin: 0 4mm 2mm;
  border: 1pt solid #1a1a1a;
  border-top: 4pt solid #b8860b;
}
.traps-header {
  background: #1a1a1a;
  color: #f0d043;
  padding: 1.5mm 2.5mm;
  font-family: "DejaVu Serif", Georgia, serif;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 1pt;
  font-size: 9pt;
}
.traps table {
  width: 100%;
  border-collapse: collapse;
  font-size: 6.8pt;
}
.traps th, .traps td {
  padding: 1.2mm 2.5mm;
  text-align: left;
  vertical-align: top;
  border-bottom: 0.3pt solid #ddd;
}
.traps th {
  background: #f0ede5;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 6.5pt;
  letter-spacing: 0.5pt;
}
.traps td:first-child {
  font-weight: 700;
  color: #8b5e00;
  width: 26mm;
}

.structure {
  padding: 0 4mm;
  margin-bottom: 2mm;
}
.structure-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.8mm;
}
.struct-card {
  padding: 2mm;
  border: 1pt solid #1a1a1a;
  background: #fff;
}
.struct-card h4 {
  font-size: 7.5pt;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.4pt;
  margin-bottom: 0.8mm;
  padding-bottom: 0.4mm;
  border-bottom: 1pt solid #1a1a1a;
}
.struct-card.pm-sys { border-top: 3pt solid #2d6a7a; }
.struct-card.pm-sys h4 { color: #2d6a7a; }
.struct-card.pres-sys { border-top: 3pt solid #c1272d; }
.struct-card.pres-sys h4 { color: #c1272d; }
.struct-card.mon-sys { border-top: 3pt solid #b8860b; }
.struct-card.mon-sys h4 { color: #b8860b; }
.struct-card.special-sys { border-top: 3pt solid #6a1b9a; }
.struct-card.special-sys h4 { color: #6a1b9a; }
.struct-card ul { list-style: none; font-size: 6.8pt; line-height: 1.4; }
.struct-card li { padding: 0.2mm 0; }

.drill {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3mm;
  padding: 0 4mm;
  margin-bottom: 2mm;
}
.drill-box {
  background: #fff;
  border: 1pt solid #1a1a1a;
  padding: 2.5mm;
}
.drill-box.daily { border-top: 4pt solid #0c8346; }
.drill-box.memory { border-top: 4pt solid #6a1b9a; }
.drill-box h3 {
  font-size: 8.5pt;
  font-weight: 900;
  margin-bottom: 1.2mm;
  text-transform: uppercase;
  letter-spacing: 0.5pt;
}
.drill-box ol, .drill-box ul {
  font-size: 7pt;
  padding-left: 4.5mm;
  line-height: 1.4;
}
.drill-box li { margin-bottom: 0.6mm; }
.drill-box .check {
  display: inline-block;
  width: 2.5mm;
  height: 2.5mm;
  border: 0.5pt solid #333;
  margin-left: 1.8mm;
  vertical-align: middle;
}
.drill-box .tip {
  background: #f0ede5;
  padding: 1.5mm;
  font-style: italic;
  font-size: 6.8pt;
  margin-top: 1.5mm;
  border-left: 2pt solid #6a1b9a;
}

.photo-note {
  margin: 1.5mm 4mm 0;
  padding: 1.3mm 2mm;
  background: #fff8e6;
  border-left: 3pt solid #d4691e;
  font-size: 6.5pt;
  font-style: italic;
  line-height: 1.3;
}
.photo-note b { font-style: normal; color: #8b5e00; }
"""

# ============ BUILD HTML ============

def build():
    grid_html = ""
    for key, data in LEADERS.items():
        grid_html += render_region(key, data)

    # Photo-availability note
    photos_available = sum(1 for region in LEADERS.values() for row in region["rows"]
                          if os.path.exists(os.path.join(PHOTO_DIR, f"{row[0]}.jpg")))
    total = sum(len(r["rows"]) for r in LEADERS.values())

    photo_status = ""
    if photos_available == 0:
        photo_status = f'''
        <div class="photo-note">
          <b>📷 Om porträtten:</b> Färgkodade initial-cirklar används som visuella ankare eftersom bildnedladdning från Wikipedia inte är tillgänglig i denna miljö. För att lägga in riktiga foton: skapa mappen <code>photos/</code>, lägg ~70 JPG-filer med filnamn enligt nyckellistan (ex. <code>kristersson.jpg</code>, <code>macron.jpg</code>), kör skriptet igen. Mest effektivt: ladda ner från Wikipedia via  <code>python3 download_photos.py</code> (medföljer i paketet).
        </div>'''
    else:
        photo_status = f'<div class="photo-note"><b>📷 Portätter:</b> {photos_available} av {total} ledare har riktiga foton inlagda.</div>'

    html = f'''<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<title>DIPS 2026 Världsledare v3</title>
<style>{CSS}</style>
</head>
<body>

<div class="page">
  <header>
    <div class="title-block">
      <h1>VÄRLDSLEDARE <span>2026</span></h1>
      <div class="sub">DIPS skriftliga prov · Verifierad studieplansch v3 · Med visuella ankare</div>
    </div>
    <div class="meta-block">
      <div class="date">AKTUELL 19 APRIL 2026</div>
      <div>A3 · Lägg upp på väggen</div>
      <span class="verified">✓ Verifierad mot källor</span>
    </div>
  </header>

  <div class="legend">
    <b>ROLLKOD:</b>
    <span class="legend-item"><span class="dot pm"></span> PM/Kansler/Taoiseach</span>
    <span class="legend-item"><span class="dot pres"></span> President</span>
    <span class="legend-item"><span class="dot mon"></span> Monark</span>
    <span class="legend-item"><span class="dot de-facto"></span> De facto</span>
    <span class="legend-item"><span class="dot trans"></span> Övergång</span>
    <b style="margin-left: auto; color: #c1272d;">⚠ = Pågående maktskifte</b>
  </div>

  <div class="grid">
    {grid_html}
  </div>

  {photo_status}

  <footer>
    <span>DIPS 2026 · Skriftliga provet 18 maj 2026 · Stockholm</span>
    <span>Plansch v3 · Verifierad 19 apr 2026 · Sida 1/2</span>
  </footer>
</div>

<div class="page page2">
  <header>
    <div class="title-block">
      <h1>FÖRHÖRSBLAD <span>+ PROVFÄLLOR</span></h1>
      <div class="sub">Aktiv återkallning · täck sida 1 och förhör dig själv</div>
    </div>
    <div class="meta-block">
      <div class="date">AKTUELL 19 APRIL 2026</div>
      <div>Skriv ut i svartvitt</div>
      <span class="verified">⚡ Kör dagligen</span>
    </div>
  </header>

  <div class="orgs">
    {render_orgs()}
  </div>

  <div class="section-title">1 · Prioritetsordning & triader</div>
  <div class="two-col">
    <div class="priority-box">
      <h3>Lärordning — lager för lager</h3>
      <p><span class="tier">TIER 1 (kan inte missa):</span> Norden & Baltikum · USA · Kina · Ryssland · Ukraina · Tyskland · Frankrike · UK · Polen · Italien · Israel · Iran · Saudiarabien · Turkiet.</p>
      <p><span class="tier">TIER 2 (bör sitta):</span> Övriga Norden-UM, Japan, Sydkorea, Indien, Brasilien, Mexiko, Sydafrika, Egypten, Spanien, Nederländerna, Belgien, Ungern (maktskifte), Tjeckien (nytt), Bulgarien (nytt).</p>
      <p><span class="tier">TIER 3 (nice to have):</span> Övriga Afrika, Latam, Balkan, Sydostasien.</p>
      <p style="margin-top: 1.5mm; background: #f0ede5; padding: 1.5mm; border-left: 2pt solid #c1272d;"><b>Minnesregel:</b> lär ALLTID i samma ordning — Europa + stormakter först, sedan Mellanöstern, Asien, till sist Latam och Afrika.</p>
    </div>
    <div class="triads">
      <h3>Triader som måste sitta samtidigt</h3>
      <ul>
        <li><span class="country-name">🇫🇮 Finland:</span> Orpo (PM) + Stubb (pres) + Valtonen (UM)</li>
        <li><span class="country-name">🇫🇷 Frankrike:</span> Macron (pres) + Lecornu (PM) + Barrot (UM)</li>
        <li><span class="country-name">🇵🇱 Polen:</span> Tusk (PM, KO) + Nawrocki (pres, PiS) + Sikorski (UM)</li>
        <li><span class="country-name">🇮🇷 Iran:</span> Pezeshkian (pres) + Khamenei (Rahbar) — Khamenei styr</li>
        <li><span class="country-name">🇨🇳 Kina:</span> Xi (pres) + Li Qiang (PM) + Wang Yi (UM)</li>
        <li><span class="country-name">🇺🇸 USA:</span> Trump (pres) + Vance (VP) + Rubio (State)</li>
        <li><span class="country-name">🇷🇺 Ryssland:</span> Putin (pres) + Misjustin (PM) + Lavrov (UM)</li>
        <li><span class="country-name">🇸🇪 Sverige:</span> Kristersson (PM) + Malmer Stenergard (UM)</li>
        <li><span class="country-name">🇺🇦 Ukraina:</span> Zelensky (pres) + Svyrydenko (PM) + Sybiha (UM)</li>
      </ul>
    </div>
  </div>

  <div class="section-title">2 · Statsskick & maktprincip</div>
  <div class="structure">
    <div class="structure-grid">
      <div class="struct-card pm-sys">
        <h4>Parlamentariska (PM styr)</h4>
        <ul>
          <li>🇸🇪 🇳🇴 🇩🇰 🇫🇮 🇮🇸</li>
          <li>🇩🇪 🇬🇧 🇮🇹 🇪🇸 🇳🇱</li>
          <li>🇧🇪 🇦🇹 🇮🇪 🇵🇹 🇬🇷</li>
          <li>🇯🇵 🇮🇳 🇦🇺 🇨🇦 🇮🇱</li>
        </ul>
      </div>
      <div class="struct-card pres-sys">
        <h4>Presidentstyrda</h4>
        <ul>
          <li>🇺🇸 🇫🇷 🇷🇺 🇹🇷 🇲🇽</li>
          <li>🇧🇷 🇦🇷 🇰🇷 🇮🇩 🇪🇬</li>
          <li>🇨🇱 🇨🇴 🇻🇪 🇺🇦 🇿🇦</li>
          <li>🇰🇪 🇳🇬 🇨🇩</li>
        </ul>
      </div>
      <div class="struct-card mon-sys">
        <h4>Monarki / de facto</h4>
        <ul>
          <li>🇯🇴 Abdullah II (kung)</li>
          <li>🇸🇦 MBS (de facto)</li>
          <li>🇲🇦 Mohammed VI (reell)</li>
          <li>🇰🇵 Kim Jong-un</li>
          <li>🇸🇩 al-Burhan (SAF)</li>
          <li>🇸🇪 Carl XVI Gustaf (ceremoniell)</li>
        </ul>
      </div>
      <div class="struct-card special-sys">
        <h4>Särskild / övergång</h4>
        <ul>
          <li>🇮🇷 Iran: Rahbar över pres</li>
          <li>🇱🇧 Libanon: konfessionell</li>
          <li>🇵🇸 Palestina: PA vs Hamas</li>
          <li>🇸🇾 Syrien: övergång 2025–2030</li>
          <li>🇨🇳 Kina: parti > stat</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="traps">
    <div class="traps-header">⚠ Provfällor — vad som faktiskt frågas</div>
    <table>
      <tr>
        <th>Provfälla</th>
        <th>Vad som ska sitta</th>
        <th>Vanligt fel</th>
      </tr>
      <tr><td>Frankrike</td><td>Presidenten är nyckeln i utrikespolitiken. PM finns men är inte första namn.</td><td>Att svara "Lecornu" på UP-frågor.</td></tr>
      <tr><td>Finland</td><td>Både president (Stubb) OCH PM (Orpo) är provrelevanta.</td><td>Att bara kunna ena halvan.</td></tr>
      <tr><td>Iran</td><td>Högsta ledaren (Khamenei) styr — inte presidenten Pezeshkian.</td><td>Att svara "Pezeshkian" på makt-frågor.</td></tr>
      <tr><td>Saudiarabien</td><td>Kronprins MBS är de facto-ledare. Kung Salman är formellt statschef.</td><td>Att inte skilja formell vs reell makt.</td></tr>
      <tr><td>Kina</td><td>Xi först (pres + partisekr + CMC). Li Qiang (PM), Wang Yi (UM) = nivå 2.</td><td>Att svara "PM Li" på stormaktsfrågor.</td></tr>
      <tr><td>Polen</td><td>PM och president är olika läger: Tusk (KO) vs Nawrocki (PiS-stödd).</td><td>Att anta samma parti.</td></tr>
      <tr><td>Ungern</td><td>Orbán sittande PM 19 apr 2026 MEN Magyar (Tisza) vann 12 apr med 2/3. Tillträder maj 2026.</td><td>Att svara utan tidsram.</td></tr>
      <tr><td>Tjeckien</td><td>Babiš (ANO) är PM sedan 9 dec 2025 — INTE Fiala.</td><td>Gammal info: Fiala.</td></tr>
      <tr><td>Nederländerna</td><td>Rob Jetten (D66) är PM sedan 23 feb 2026. Schoof/PVV rasade juni 2025.</td><td>Gammal info: Schoof/Wilders.</td></tr>
      <tr><td>Bulgarien</td><td>Gyurov tillfällig PM. Yotova pres (efter Radev jan 2026). VAL 19 APR 2026.</td><td>Äldre info: Zhelyazkov/Radev.</td></tr>
      <tr><td>Syrien</td><td>Ahmad al-Sharaa är president (övergång). PM-posten ÄR AVSKAFFAD sedan mars 2025.</td><td>Att fråga efter "PM" i Syrien.</td></tr>
      <tr><td>Portugal</td><td>Montenegro (PSD) fortfarande PM. Ny pres António José Seguro (PS) sedan 9 mars 2026.</td><td>Att tro Rebelo de Sousa fortfarande pres.</td></tr>
      <tr><td>UK</td><td>Keir Starmer är premiärminister, ej president. Monark: Charles III.</td><td>Att skriva "president Starmer".</td></tr>
    </table>
  </div>

  <div class="section-title">3 · Daglig drill & mnemonic</div>
  <div class="drill">
    <div class="drill-box daily">
      <h3>5-minuters daglig drill</h3>
      <ol>
        <li>Säg ALLA nordiska stats-/regeringschefer utan att titta <span class="check"></span></li>
        <li>Säg tre triader: USA, Kina, Finland <span class="check"></span></li>
        <li>Peka ut fem presidentstyrda länder i Latinamerika <span class="check"></span></li>
        <li>Peka ut fem PM-ledda länder i Europa <span class="check"></span></li>
        <li>Säg nyckelnamnen i Mellanöstern utan att missa Iran + Saudi <span class="check"></span></li>
        <li>Säg EU-toppen (Costa, VdL, Kallas, Lagarde, Metsola) <span class="check"></span></li>
        <li>Säg fyra länder med pågående maktskifte apr–maj 2026 <span class="check"></span></li>
      </ol>
      <div class="tip"><b>Svar på #7:</b> Ungern (Magyar tillträder), Nederländerna (Jetten feb), Bulgarien (val idag), Tjeckien (Babiš ny).</div>
    </div>
    <div class="drill-box memory">
      <h3>Mnemonic & associationsknippen</h3>
      <ul style="padding-left: 0; list-style: none;">
        <li><b>Norden-serien:</b> "Kristersson, Orpo, Støre, Frederiksen, Frostadóttir" — 5 PM.</li>
        <li style="margin-top: 1.3mm;"><b>Baltikum E-M-L:</b> <b>E</b>stland Michal, <b>L</b>ettland Siliņa, <b>L</b>itauen Ruginienė.</li>
        <li style="margin-top: 1.3mm;"><b>Trumps team:</b> "TVR" = Trump, Vance, Rubio.</li>
        <li style="margin-top: 1.3mm;"><b>EU-toppen:</b> "Costa, Kallas, Ursula, Lagarde, Metsola" = CKULM.</li>
        <li style="margin-top: 1.3mm;"><b>Iran-regeln:</b> "Rahbar över allt" — Khamenei > Pezeshkian.</li>
        <li style="margin-top: 1.3mm;"><b>Saudi-regeln:</b> "Kungen sitter, prinsen regerar."</li>
        <li style="margin-top: 1.3mm;"><b>Ungern-klockan:</b> "12 april 2026, Magyar vann, tillträder maj." Om prov är 18 maj → Magyar är PM.</li>
      </ul>
    </div>
  </div>

  <footer>
    <span>DIPS 2026 · Skriftliga provet 18 maj 2026</span>
    <span>Källor: regeringen.se, officiella regeringssajter, Wikipedia, Reuters, Al Jazeera, Bloomberg · verifierat 19 apr 2026</span>
  </footer>
</div>

</body>
</html>
'''
    return html


if __name__ == "__main__":
    html = build()
    with open(OUTPUT_HTML, 'w') as f:
        f.write(html)
    weasyprint.HTML(filename=OUTPUT_HTML).write_pdf(OUTPUT_PDF)
    size = os.path.getsize(OUTPUT_PDF)
    print(f"✓ Built {OUTPUT_PDF} ({size/1024:.0f} KB)")
