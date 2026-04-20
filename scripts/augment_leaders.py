"""Add iso_num + capital lat/lon to each leader row in app/data/leaders.json.

Also stamps the map projection pixel position so the SPA can render pins without
re-running the Natural Earth math on every tick.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEADERS_PATH = ROOT / "app" / "data" / "leaders.json"

# key -> (ISO-numeric, capital lat, capital lon)
# Capitals, not geographic centroids. For Israel we use Jerusalem (gov seat).
COUNTRY_META: dict[str, tuple[str, float, float]] = {
    # Norden & Baltikum
    "kristersson":  ("752", 59.33, 18.07),   # Stockholm
    "orpo":         ("246", 60.17, 24.94),   # Helsinki
    "store":        ("578", 59.91, 10.75),   # Oslo
    "frederiksen":  ("208", 55.68, 12.57),   # Copenhagen
    "frostadottir": ("352", 64.15, -21.94),  # Reykjavik
    "michal":       ("233", 59.44, 24.75),   # Tallinn
    "silina":       ("428", 56.95, 24.11),   # Riga
    "ruginiene":    ("440", 54.69, 25.28),   # Vilnius
    # Nordamerika
    "trump":        ("840", 38.90, -77.04),  # Washington DC
    "carney":       ("124", 45.42, -75.70),  # Ottawa
    "sheinbaum":    ("484", 19.43, -99.13),  # Mexico City
    # Stora EU + UK
    "merz":         ("276", 52.52, 13.40),   # Berlin
    "macron":       ("250", 48.85, 2.35),    # Paris
    "starmer":      ("826", 51.51, -0.13),   # London
    "meloni":       ("380", 41.90, 12.50),   # Rome
    "sanchez":      ("724", 40.42, -3.70),   # Madrid
    "jetten":       ("528", 52.37, 4.89),    # Amsterdam
    "tusk":         ("616", 52.23, 21.01),   # Warsaw
    "dewever":      ("056", 50.85, 4.35),    # Brussels
    # Övriga EU + Ukr
    "zelensky":     ("804", 50.45, 30.52),   # Kyiv
    "babis":        ("203", 50.08, 14.43),   # Prague
    "orban":        ("348", 47.50, 19.04),   # Budapest
    "bolojan":      ("642", 44.43, 26.10),   # Bucharest
    "stocker":      ("040", 48.21, 16.37),   # Vienna
    "montenegro":   ("620", 38.72, -9.14),   # Lisbon
    "mitsotakis":   ("300", 37.98, 23.72),   # Athens
    "martin":       ("372", 53.35, -6.26),   # Dublin
    "gyurov":       ("100", 42.70, 23.32),   # Sofia
    # Ryssland + Balkan + Turkiet
    "putin":        ("643", 55.75, 37.62),   # Moscow
    "lukashenko":   ("112", 53.90, 27.57),   # Minsk
    "sandu":        ("498", 47.01, 28.86),   # Chisinau
    "erdogan":      ("792", 39.93, 32.87),   # Ankara
    "vucic":        ("688", 44.79, 20.45),   # Belgrade
    "plenkovic":    ("191", 45.81, 15.98),   # Zagreb
    # Asien & Pacific
    "xi":           ("156", 39.90, 116.41),  # Beijing
    "takaichi":     ("392", 35.68, 139.69),  # Tokyo
    "lee":          ("410", 37.57, 126.98),  # Seoul
    "kim":          ("408", 39.02, 125.75),  # Pyongyang
    "modi":         ("356", 28.61, 77.23),   # New Delhi
    "sharif":       ("586", 33.69, 73.05),   # Islamabad
    "prabowo":      ("360", -6.21, 106.85),  # Jakarta
    "albanese":     ("036", -35.28, 149.13), # Canberra
    # MENA
    "netanyahu":    ("376", 31.77, 35.21),   # Jerusalem
    "abbas":        ("275", 31.90, 35.20),   # Ramallah
    "pezeshkian":   ("364", 35.69, 51.39),   # Tehran
    "mbs":          ("682", 24.71, 46.68),   # Riyadh
    "sisi":         ("818", 30.04, 31.24),   # Cairo
    "sharaa":       ("760", 33.51, 36.28),   # Damascus
    "aoun":         ("422", 33.89, 35.50),   # Beirut
    "abdullah":     ("400", 31.95, 35.93),   # Amman
    "akhannouch":   ("504", 34.02, -6.83),   # Rabat
    # Afrika
    "ramaphosa":    ("710", -25.75, 28.19),  # Pretoria
    "tinubu":       ("566", 9.08, 7.54),     # Abuja
    "ruto":         ("404", -1.29, 36.82),   # Nairobi
    "abiy":         ("231", 9.03, 38.74),    # Addis Ababa
    "kagame":       ("646", -1.94, 30.06),   # Kigali
    "tshisekedi":   ("180", -4.44, 15.27),   # Kinshasa
    "burhan":       ("729", 15.50, 32.56),   # Khartoum
    # LatAm
    "lula":         ("076", -15.79, -47.88), # Brasilia
    "milei":        ("032", -34.60, -58.38), # Buenos Aires
    "boric":        ("152", -33.45, -70.67), # Santiago
    "petro":        ("170", 4.71, -74.07),   # Bogota
    "maduro":       ("862", 10.49, -66.87),  # Caracas
    "diazcanel":    ("192", 23.13, -82.38),  # Havana
}

# Org chiefs — seat city
ORG_META: dict[str, tuple[str, float, float]] = {
    "guterres":  ("FN",  40.75, -73.97),  # New York
    "rutte":     ("NATO", 50.87, 4.42),    # Brussels
    "vdl":       ("EU",  50.85, 4.35),
    "costa":     ("EU",  50.85, 4.35),
    "kallas":    ("EU",  50.85, 4.35),
    "metsola":   ("EU",  49.61, 6.12),     # Strasbourg/Luxembourg split — pick LUX
    "lagarde":   ("EU",  50.11, 8.68),     # Frankfurt ECB
    "okonjo":    ("WTO", 46.22, 6.14),     # Geneva
    "georgieva": ("IMF", 38.90, -77.04),   # DC
    "banga":     ("VB",  38.90, -77.04),   # DC
}


VIEW_W = 1000
VIEW_H = 520


def natural_earth(lon_deg: float, lat_deg: float):
    lam = math.radians(lon_deg)
    phi = math.radians(lat_deg)
    phi2 = phi * phi
    phi4 = phi2 * phi2
    x = lam * (0.8707 - 0.131979 * phi2 + phi4 * (-0.013791 + phi4 * (0.003971 * phi2 - 0.001529 * phi4)))
    y = phi * (1.007226 + phi2 * (0.015085 + phi4 * (-0.044475 + 0.028874 * phi2 - 0.005916 * phi4)))
    return x, y


def projection_params():
    xs, ys = [], []
    for lon in range(-180, 181, 5):
        for lat in range(-90, 91, 5):
            x, y = natural_earth(lon, lat)
            xs.append(x); ys.append(y)
    mnx, mxx = min(xs), max(xs)
    mny, mxy = min(ys), max(ys)
    scale = min(VIEW_W / (mxx - mnx), VIEW_H / (mxy - mny))
    off_x = (VIEW_W - (mxx - mnx) * scale) / 2 - mnx * scale
    off_y = (VIEW_H - (mxy - mny) * scale) / 2 + mxy * scale
    return scale, off_x, off_y


SCALE, OFF_X, OFF_Y = projection_params()


def project(lat, lon):
    x, y = natural_earth(lon, lat)
    return round(x * SCALE + OFF_X, 2), round(-y * SCALE + OFF_Y, 2)


def main():
    data = json.loads(LEADERS_PATH.read_text())

    missing = []
    for region in data["regions"]:
        for leader in region["leaders"]:
            meta = COUNTRY_META.get(leader["key"])
            if not meta:
                missing.append(leader["key"])
                continue
            iso, lat, lon = meta
            px, py = project(lat, lon)
            leader["iso_num"] = iso
            leader["lat"] = lat
            leader["lon"] = lon
            leader["mx"] = px
            leader["my"] = py

    for chief in data.get("org_chiefs", []):
        meta = ORG_META.get(chief["key"])
        if not meta:
            continue
        _org, lat, lon = meta
        px, py = project(lat, lon)
        chief["lat"] = lat
        chief["lon"] = lon
        chief["mx"] = px
        chief["my"] = py

    if missing:
        print("Missing coordinates for:", missing)
    else:
        print("All leaders enriched with ISO + pixel positions.")

    LEADERS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"Wrote {LEADERS_PATH}")


if __name__ == "__main__":
    main()
