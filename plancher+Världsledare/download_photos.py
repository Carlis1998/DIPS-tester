"""
download_photos.py — Laddar ner riktiga foton från Wikipedia för DIPS-planschen

Instruktioner:
  1. Ha build_plansch_v3.py + denna fil i samma mapp
  2. pip install requests pillow
  3. python3 download_photos.py
  4. python3 build_plansch_v3.py
  5. Öppna DIPS_2026_Varldsledare_v3.pdf

Skriptet hämtar Wikipedia-porträttet för varje ledare, beskär till fyrkant
och sparar som JPG i photos/. build_plansch_v3.py läser sedan dessa automatiskt.
"""
import os
import time
import requests
from io import BytesIO

try:
    from PIL import Image
except ImportError:
    print("Installera Pillow: pip install pillow")
    exit(1)

os.makedirs('photos', exist_ok=True)

SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'DIPS-Plansch/1.1 (personal educational script; requests sequential thumbnails)',
    'Accept': 'application/json,image/*;q=0.9,*/*;q=0.8',
})

# Wikimedia tillåter bara original eller standard-thumbnail-storlekar.
THUMB_STEPS = (120, 250, 330, 500, 960)
REQUEST_DELAY_S = 0.75
MAX_RETRIES = 5

# Samma nycklar som i build_plansch_v3.py
LEADERS = {
    # Norden & Baltikum
    "kristersson": "Ulf Kristersson",
    "orpo": "Petteri Orpo",
    "stubb": "Alexander Stubb",
    "store": "Jonas Gahr Støre",
    "frederiksen": "Mette Frederiksen",
    "frostadottir": "Kristrún Frostadóttir",
    "michal": "Kristen Michal",
    "silina": "Evika Siliņa",
    "ruginiene": "Inga Ruginienė",
    # Nordamerika
    "trump": "Donald Trump",
    "carney": "Mark Carney",
    "sheinbaum": "Claudia Sheinbaum",
    # Stora EU + UK
    "merz": "Friedrich Merz",
    "macron": "Emmanuel Macron",
    "starmer": "Keir Starmer",
    "meloni": "Giorgia Meloni",
    "sanchez": "Pedro Sánchez",
    "jetten": "Rob Jetten",
    "tusk": "Donald Tusk",
    "dewever": "Bart De Wever",
    # Övriga EU + Ukraina
    "zelensky": "Volodymyr Zelenskyy",
    "babis": "Andrej Babiš",
    "orban": "Viktor Orbán",
    "bolojan": "Ilie Bolojan",
    "stocker": "Christian Stocker",
    "montenegro": "Luís Montenegro",
    "mitsotakis": "Kyriakos Mitsotakis",
    "martin": "Micheál Martin",
    "gyurov": "Andrey Gyurov",
    # Ryssland & Balkan
    "putin": "Vladimir Putin",
    "lukashenko": "Alexander Lukashenko",
    "sandu": "Maia Sandu",
    "erdogan": "Recep Tayyip Erdoğan",
    "vucic": "Aleksandar Vučić",
    "plenkovic": "Andrej Plenković",
    # Asien
    "xi": "Xi Jinping",
    "takaichi": "Sanae Takaichi",
    "lee": "Lee Jae-myung",
    "kim": "Kim Jong Un",
    "modi": "Narendra Modi",
    "sharif": "Shehbaz Sharif",
    "prabowo": "Prabowo Subianto",
    "albanese": "Anthony Albanese",
    # MENA
    "netanyahu": "Benjamin Netanyahu",
    "abbas": "Mahmoud Abbas",
    "pezeshkian": "Masoud Pezeshkian",
    "khamenei": "Ali Khamenei",
    "mbs": "Mohammed bin Salman",
    "sisi": "Abdel Fattah el-Sisi",
    "sharaa": "Ahmed al-Sharaa",
    "aoun": "Joseph Aoun",
    "abdullah": "Abdullah II of Jordan",
    "akhannouch": "Aziz Akhannouch",
    # Afrika
    "ramaphosa": "Cyril Ramaphosa",
    "tinubu": "Bola Tinubu",
    "ruto": "William Ruto",
    "abiy": "Abiy Ahmed",
    "kagame": "Paul Kagame",
    "tshisekedi": "Félix Tshisekedi",
    "burhan": "Abdel Fattah al-Burhan",
    # Latam
    "lula": "Luiz Inácio Lula da Silva",
    "milei": "Javier Milei",
    "boric": "Gabriel Boric",
    "petro": "Gustavo Petro",
    "maduro": "Nicolás Maduro",
    "diazcanel": "Miguel Díaz-Canel",
    # Org chefer
    "guterres": "António Guterres",
    "rutte": "Mark Rutte",
    "vdl": "Ursula von der Leyen",
    "costa": "António Costa",
    "kallas": "Kaja Kallas",
    "metsola": "Roberta Metsola",
    "lagarde": "Christine Lagarde",
    "okonjo": "Ngozi Okonjo-Iweala",
    "georgieva": "Kristalina Georgieva",
    "banga": "Ajay Banga",
}


def choose_thumb_width(size_px):
    """Välj minsta tillåtna Wikimedia-thumbnail som räcker för målstorleken."""
    wanted = max(size_px, size_px + 10)
    for step in THUMB_STEPS:
        if step >= wanted:
            return step
    return THUMB_STEPS[-1]


def get_with_backoff(url, *, params=None, timeout=15):
    """Håll nere tempot och backa vid Wikimedia-rate limiting."""
    backoff = REQUEST_DELAY_S
    last_error = None
    for attempt in range(MAX_RETRIES):
        if attempt:
            time.sleep(backoff)
        response = SESSION.get(url, params=params, timeout=timeout)
        if response.status_code != 429:
            response.raise_for_status()
            time.sleep(REQUEST_DELAY_S)
            return response
        retry_after = response.headers.get("Retry-After")
        if retry_after and retry_after.isdigit():
            backoff = max(float(retry_after), backoff)
        else:
            backoff = min(backoff * 2, 20.0)
        last_error = requests.HTTPError(
            f"429 Too many requests for {response.url} (retry {attempt + 1}/{MAX_RETRIES})"
        )
    raise last_error or RuntimeError("request failed without response")


def fetch_page_image(title, thumb_width):
    """Hämta Wikimedia-thumbnail via MediaWiki API med godkänd storlek."""
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "formatversion": "2",
        "prop": "pageimages",
        "piprop": "thumbnail",
        "pithumbsize": str(thumb_width),
        "pilicense": "any",
        "redirects": "1",
        "titles": title,
    }
    response = get_with_backoff(api_url, params=params, timeout=15)
    data = response.json()
    pages = data.get("query", {}).get("pages", [])
    if not pages:
        raise RuntimeError("no page data")
    page = pages[0]
    thumb = page.get("thumbnail", {})
    source = thumb.get("source")
    if not source:
        raise RuntimeError("no thumbnail")
    img_response = get_with_backoff(source, timeout=20)
    return img_response.content


def get_wiki_photo(title, target_path, size_px=240):
    """Hämta thumbnail från Wikipedia API och anpassa den lokalt."""
    try:
        thumb_width = choose_thumb_width(size_px)
        raw_image = fetch_page_image(title, thumb_width)
        img = Image.open(BytesIO(raw_image)).convert('RGB')
        # Beskär till kvadrat (centrerad, övre delen för porträtt)
        w, h = img.size
        if w != h:
            s = min(w, h)
            # Ta övre delen för porträtt så vi får med ansiktet
            left = (w - s) // 2
            top = max(0, (h - s) // 3)
            img = img.crop((left, top, left + s, top + s))
        img = img.resize((size_px, size_px), Image.LANCZOS)
        img.save(target_path, 'JPEG', quality=85)
        return True, "ok"
    except Exception as e:
        return False, str(e)


ok = 0
fail = []
for key, name in LEADERS.items():
    path = f"photos/{key}.jpg"
    if os.path.exists(path):
        print(f"  - {key}: redan nedladdad")
        ok += 1
        continue
    success, msg = get_wiki_photo(name, path)
    if success:
        print(f"  ✓ {key} ({name})")
        ok += 1
    else:
        print(f"  ✗ {key} ({name}): {msg}")
        fail.append((key, name))

print(f"\n{ok}/{len(LEADERS)} nedladdade")
if fail:
    print(f"\nFailade ({len(fail)}): lägg in manuellt som photos/<key>.jpg")
    for k, n in fail:
        print(f"  - {k}.jpg  ({n})")
print("\nNästa steg: python3 build_plansch_v3.py")
