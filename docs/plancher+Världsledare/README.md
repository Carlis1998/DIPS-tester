# DIPS 2026 Världsledare-plansch v3

Paket för att skapa en studieplansch inför DIPS skriftliga prov 18 maj 2026.

## Innehåll

- `DIPS_2026_Varldsledare_v3.pdf` — Färdig plansch med initial-avatar-ankare (använd denna direkt)
- `build_plansch_v3.py` — Python-skript som genererar PDF:en (kör själv för att lägga in foton)
- `download_photos.py` — Hämtar Wikipedia-porträtt automatiskt
- `plansch_v3.html` — Källkoden (HTML) som skriptet producerar

## Snabbstart — använd planschen direkt

Öppna `DIPS_2026_Varldsledare_v3.pdf`. Skriv ut i A3 färg. Klart.

## Steg-för-steg: lägga in riktiga foton på ledarna

Planschen använder färgkodade initial-cirklar (UK för Kristersson i Norden-blå,
VP för Putin i lila, osv.) som visuella ankare. Om du vill ha riktiga
Wikipedia-porträtt istället:

### 1. Installera beroenden

```bash
pip install requests pillow weasyprint
```

På Linux/Mac behöver weasyprint även systembibliotek:
```bash
# Ubuntu/Debian:
sudo apt install libpango-1.0-0 libpangoft2-1.0-0

# Mac:
brew install pango
```

### 2. Ladda ner porträtt

```bash
python3 download_photos.py
```

Skriptet skapar mappen `photos/` och laddar ner ~70 porträtt från Wikipedia.
Det använder Wikimedia-godkända thumbnail-storlekar, kör sekventiellt för att
undvika 429-blockeringar, beskär automatiskt till fyrkant och skalar till 240px.

### 3. Regenerera planschen

```bash
python3 build_plansch_v3.py
```

`build_plansch_v3.py` plockar automatiskt upp fotona från `photos/`-mappen
och bäddar in dem i PDF:en istället för initial-avatarerna.

Om ett enskilt foto inte gick att ladda ned: lägg in det manuellt i
`photos/<key>.jpg` (t.ex. `photos/kristersson.jpg`). Kör sedan
`build_plansch_v3.py` igen.

## Filstruktur efter körning

```
dips-plansch/
├── DIPS_2026_Varldsledare_v3.pdf     ← DIN PLANSCH
├── build_plansch_v3.py
├── download_photos.py
├── plansch_v3.html
├── README.md
└── photos/
    ├── kristersson.jpg
    ├── macron.jpg
    ├── ... (70 stycken)
```

## Anpassa

### Byta ett specifikt foto
Ersätt `photos/<key>.jpg` med egen bild (kvadratisk, ca 240×240px,
ansiktet tydligt). Kör `python3 build_plansch_v3.py` igen.

### Lägg till/ta bort en ledare
Redigera `LEADERS`-dictet i `build_plansch_v3.py` och `download_photos.py`.
Varje post är en tuple:
```python
("key", "II", "region", "🇺🇸", "LAND", "Förnamn Efternamn", "PM",
 "Sub-line med info", None)
```
- `key` — filnamn utan .jpg, bara bokstäver/siffror/understreck
- `II` — initialer (används om foto saknas)
- `region` — en av: norden, nordam, storm, ovriga, russ, asien, mena, afrika, latam, org
- Sista fältet: `None`, `"note:text"` (orange callout) eller `"alert:text"` (röd callout)

### Uppdatera inför provet
Planschen är verifierad 19 april 2026. Innan provet 18 maj, kör en ny runda:
- Kontrollera Ungern (Magyar väntas tillträda maj 2026)
- Kontrollera Bulgarien (val hölls 19 april)
- Kontrollera alla "NY"/"⚠" markerade rader

## Om provfällorna

Planschens sida 2 listar 13 klassiska provfällor med exakt rätt svar.
Kör den som förhörsmall — täck över den högra kolumnen och förhör dig själv.

## Kontakt och teknisk info

Planschen är byggd 19 april 2026 av Claude (Anthropic) för kandidat Moa.
Data verifierad mot regeringen.se, officiella regeringssajter, Wikipedia,
Reuters, Al Jazeera och Bloomberg.

PDF genereras med WeasyPrint (HTML→PDF) och flagg-emojis via Noto Color Emoji.
Layout optimerad för A3-utskrift.

Lycka till på provet! 🇸🇪
