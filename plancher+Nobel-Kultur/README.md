# DIPS 2026 Nobel & Kulturpriser-plansch

Studieplansch för diplomatprovet 18 maj 2026 — täcker Nobels fredspris, litteraturpris och världens kulturpriser.

## Innehåll

- `DIPS_2026_Nobel_Kultur.pdf` — **Färdig 2-sidig A3-plansch** (skriv ut direkt)
- `build_nobel_plansch.py` — Python-skript som bygger HTML→PDF
- `download_nobel_photos.py` — Hämtar Wikipedia-porträtt automatiskt
- `plansch_nobel.html` — Källkoden (HTML) som skriptet producerar
- `photos/` — 44 nedladdade Wikipedia-porträtt (240×240 JPG)

## Snabbstart

Öppna `DIPS_2026_Nobel_Kultur.pdf`. Skriv ut i A3-färg. Klart.

## Vad planschen täcker

### Sida 1
- **Nobels fredspris 2016-2025** (10 år) — namn, land, vad/varför de kämpar för
- **Nobels litteraturpris 2016-2025** (10 år) — namn, land, två mest kända verk
- **Bonus 2015** för båda priserna (Nat. dialogkvartetten / Aleksijevitj)

### Sida 2
- **10 historiska klassiker** (mix fred + litteratur) — Dunant, Lagerlöf, MLK, Mor Teresa, Hemingway, García Márquez, Mandela & de Klerk, Morrison, Tranströmer, EU
- **Specialpanel:** Sveriges 7 Nobel-laureater i litteratur genom tiderna
- **Sveriges 5 + 1 kulturpriser:** Augustpriset, Polar Music, ALMA, Guldbaggen, Nordiska rådets, Stora Journalistpriset
- **Europas 5 + 1 kulturpriser:** Booker, Goncourt, Cervantes, Strega, Cannes Palme d'Or, Berlin Golden Bear
- **Världens 5 + 1 kulturpriser:** Oscars, Pulitzer, Grammy, Pritzker, Venice Lion, Tony

## Regenerera planschen

Om du vill uppdatera data eller lägga till foton:

```bash
pip install requests pillow weasyprint
python3 download_nobel_photos.py    # hämtar ~44 Wikipedia-porträtt
python3 build_nobel_plansch.py      # bygger PDF
```

## Saknade foton (använder initial-avatar)

- `vang.jpg` (Vónbjørt Vang, Färöarna — obskyrare)
- `jiakun.jpg` (Liu Jiakun, kinesisk arkitekt — Wikipedia saknar thumbnail)

Kan läggas in manuellt i `photos/<key>.jpg` (240×240px).

## Källor

Verifierad mot:
- nobelprize.org, nobelpeaceprize.org
- Augustpriset.se, polarmusicprize.org, alma.se, guldbaggen.se, norden.org
- thebookerprizes.com, academiegoncourt.com, premiostrega.it
- pulitzer.org, oscars.org, grammy.com, pritzkerprize.com, labiennale.org

## Provdatum: 18 maj 2026 🇸🇪

Lycka till, Moa!
