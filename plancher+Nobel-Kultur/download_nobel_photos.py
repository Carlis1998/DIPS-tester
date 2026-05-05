"""
download_nobel_photos.py — Hämtar Wikipedia-porträtt för Nobel/Kulturpris-planschen.

Steg:
  1. pip install requests pillow
  2. python3 download_nobel_photos.py
  3. python3 build_nobel_plansch.py

Hämtar ~40 porträtt (Nobel Fred + Litt 2015-2025 + 10 historiska + några kulturpris).
För organisationer (WFP, ICAN, EU, Memorial, Nihon Hidankyo) finns inget porträtt:
build-skriptet använder då gradient-initial-avatar (egen visuell ankare).
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
    'User-Agent': 'DIPS-Plansch-Nobel/1.0 (educational; sequential thumbnail requests)',
    'Accept': 'application/json,image/*;q=0.9,*/*;q=0.8',
})

THUMB_STEPS = (120, 250, 330, 500, 960)
REQUEST_DELAY_S = 0.8
MAX_RETRIES = 5

# Wikipedia-titlar (engelska Wiki som primär — bredast täckning)
LAUREATES = {
    # ============ NOBELS FREDSPRIS 2015-2025 ============
    "machado": "María Corina Machado",
    "mohammadi": "Narges Mohammadi",
    "ressa": "Maria Ressa",
    "abiy": "Abiy Ahmed",
    "mukwege": "Denis Mukwege",
    "santos": "Juan Manuel Santos",
    # 2015 = Tunisian National Dialogue Quartet (organisation)
    # 2017 ICAN (org)
    # 2020 WFP (org)
    # 2022 inkluderar Bialiatski (person) + Memorial + CCL — ta Bialiatski
    "bialiatski": "Ales Bialiatski",
    # 2024 Nihon Hidankyo (organisation)

    # ============ NOBELS LITTERATURPRIS 2015-2025 ============
    "krasznahorkai": "László Krasznahorkai",
    "hankang": "Han Kang (author)",
    "fosse": "Jon Fosse",
    "ernaux": "Annie Ernaux",
    "gurnah": "Abdulrazak Gurnah",
    "gluck": "Louise Glück",
    "handke": "Peter Handke",
    "tokarczuk": "Olga Tokarczuk",
    "ishiguro": "Kazuo Ishiguro",
    "dylan": "Bob Dylan",
    "alexievich": "Svetlana Alexievich",

    # ============ HISTORISKA KLASSIKER (10 must-know) ============
    "dunant": "Henry Dunant",
    "lagerlof": "Selma Lagerlöf",
    "hemingway": "Ernest Hemingway",
    "mlk": "Martin Luther King Jr.",
    "teresa": "Mother Teresa",
    "marquez": "Gabriel García Márquez",
    "morrison": "Toni Morrison",
    "mandela": "Nelson Mandela",
    "tranströmer": "Tomas Tranströmer",
    # EU = organisation, ingen person

    # ============ KULTURPRIS-VINNARE (utvalda — där det är 1 tydlig person) ============
    "queen_may": "Brian May",   # Queen-medlem, mest igenkännlig
    "hancock": "Herbie Hancock",
    "hannigan": "Barbara Hannigan",
    "klassen": "Jon Klassen",
    "saleh": "Tarik Saleh",
    "vang": "Vónbjørt Vang",
    "wolff": "Lina Wolff",
    "uusma": "Bea Uusma",
    "szalay": "David Szalay",
    "mauvignier": "Laurent Mauvignier",
    "celorio": "Gonzalo Celorio",
    "bajani": "Andrea Bajani",
    "panahi": "Jafar Panahi",
    "catak": "İlker Çatak",
    "pta": "Paul Thomas Anderson",
    "everett": "Percival Everett",
    "badbunny": "Bad Bunny",
    "jiakun": "Liu Jiakun",
    "jarmusch": "Jim Jarmusch",
}


def choose_thumb_width(size_px):
    wanted = max(size_px, size_px + 10)
    for step in THUMB_STEPS:
        if step >= wanted:
            return step
    return THUMB_STEPS[-1]


def get_with_backoff(url, *, params=None, timeout=15):
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


def fetch_page_image(title, thumb_width, lang="en"):
    api_url = f"https://{lang}.wikipedia.org/w/api.php"
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
    """Försök engelska Wiki först, fall tillbaka till svenska."""
    last_err = None
    for lang in ("en", "sv"):
        try:
            thumb_width = choose_thumb_width(size_px)
            raw = fetch_page_image(title, thumb_width, lang=lang)
            img = Image.open(BytesIO(raw)).convert('RGB')
            w, h = img.size
            if w != h:
                s = min(w, h)
                left = (w - s) // 2
                top = max(0, (h - s) // 3)
                img = img.crop((left, top, left + s, top + s))
            img = img.resize((size_px, size_px), Image.LANCZOS)
            img.save(target_path, 'JPEG', quality=85)
            return True, f"ok ({lang}.wiki)"
        except Exception as e:
            last_err = str(e)
            continue
    return False, last_err or "unknown"


ok = 0
fail = []
for key, name in LAUREATES.items():
    path = f"photos/{key}.jpg"
    if os.path.exists(path):
        print(f"  - {key}: redan nedladdad")
        ok += 1
        continue
    success, msg = get_wiki_photo(name, path)
    if success:
        print(f"  ✓ {key} ({name}) — {msg}")
        ok += 1
    else:
        print(f"  ✗ {key} ({name}): {msg}")
        fail.append((key, name))

print(f"\n{ok}/{len(LAUREATES)} nedladdade")
if fail:
    print(f"\nFailade ({len(fail)}): lägg in manuellt som photos/<key>.jpg")
    for k, n in fail:
        print(f"  - {k}.jpg  ({n})")
print("\nNästa steg: python3 build_nobel_plansch.py")
