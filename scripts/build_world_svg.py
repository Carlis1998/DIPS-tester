"""Convert world-atlas 110m TopoJSON to a pre-projected SVG world map.

Output: app/data/world-map.svg with one <path> per country, carrying:
  - id: "c<ISO-numeric>"
  - data-iso: numeric ISO 3166
  - data-name: country English name

Projection: Natural Earth I (gives pleasing, mobile-friendly shapes — less
polar distortion than Mercator, Europe still prominent enough to work with).

Viewport: 1000 x 520 (2:1-ish aspect) — the SPA scales it responsively.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPO_PATH = ROOT / "app" / "data" / "world-110m.json"
SVG_PATH = ROOT / "app" / "data" / "world-map.svg"

VIEW_W = 1000
VIEW_H = 520


def natural_earth(lon_deg: float, lat_deg: float) -> tuple[float, float]:
    """Natural Earth I projection, (lon,lat in degrees) -> (x,y) in unit space.

    Formulas from Flex Projector / de Wallis (publicly documented).
    """
    lam = math.radians(lon_deg)
    phi = math.radians(lat_deg)
    phi2 = phi * phi
    phi4 = phi2 * phi2
    x = lam * (0.8707 - 0.131979 * phi2 + phi4 * (-0.013791 + phi4 * (0.003971 * phi2 - 0.001529 * phi4)))
    y = phi * (1.007226 + phi2 * (0.015085 + phi4 * (-0.044475 + 0.028874 * phi2 - 0.005916 * phi4)))
    return x, y


def build_projection_bounds() -> tuple[float, float, float, float]:
    xs: list[float] = []
    ys: list[float] = []
    for lon in range(-180, 181, 5):
        for lat in range(-90, 91, 5):
            x, y = natural_earth(lon, lat)
            xs.append(x)
            ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def decode_topojson(topo: dict) -> tuple[list[list[tuple[float, float]]], dict]:
    transform = topo.get("transform") or {}
    scale = transform.get("scale", [1, 1])
    translate = transform.get("translate", [0, 0])
    raw_arcs = topo["arcs"]
    decoded: list[list[tuple[float, float]]] = []
    for arc in raw_arcs:
        x = 0
        y = 0
        pts: list[tuple[float, float]] = []
        for dx, dy in arc:
            x += dx
            y += dy
            lon = x * scale[0] + translate[0]
            lat = y * scale[1] + translate[1]
            pts.append((lon, lat))
        decoded.append(pts)
    return decoded, topo["objects"]["countries"]["geometries"]


def arc_pts(decoded_arcs: list[list[tuple[float, float]]], index: int) -> list[tuple[float, float]]:
    if index < 0:
        return list(reversed(decoded_arcs[~index]))
    return list(decoded_arcs[index])


def ring_to_coords(decoded_arcs, ring: list[int]) -> list[tuple[float, float]]:
    coords: list[tuple[float, float]] = []
    for idx in ring:
        pts = arc_pts(decoded_arcs, idx)
        if coords and pts and coords[-1] == pts[0]:
            coords.extend(pts[1:])
        else:
            coords.extend(pts)
    return coords


def geom_to_rings(decoded_arcs, geom: dict) -> list[list[tuple[float, float]]]:
    t = geom["type"]
    arcs = geom["arcs"]
    rings: list[list[tuple[float, float]]] = []
    if t == "Polygon":
        for ring in arcs:
            rings.append(ring_to_coords(decoded_arcs, ring))
    elif t == "MultiPolygon":
        for poly in arcs:
            for ring in poly:
                rings.append(ring_to_coords(decoded_arcs, ring))
    return rings


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def main() -> None:
    topo = json.loads(TOPO_PATH.read_text())
    decoded_arcs, geometries = decode_topojson(topo)

    min_x, min_y, max_x, max_y = build_projection_bounds()
    scale_x = VIEW_W / (max_x - min_x)
    scale_y = VIEW_H / (max_y - min_y)
    scale = min(scale_x, scale_y)
    # Center
    off_x = (VIEW_W - (max_x - min_x) * scale) / 2 - min_x * scale
    off_y = (VIEW_H - (max_y - min_y) * scale) / 2 + max_y * scale

    def project(lon: float, lat: float) -> tuple[float, float]:
        x, y = natural_earth(lon, lat)
        return x * scale + off_x, -y * scale + off_y

    paths: list[str] = []
    for geom in geometries:
        iso = geom.get("id") or ""
        props = geom.get("properties") or {}
        name = props.get("name") or ""
        rings = geom_to_rings(decoded_arcs, geom)
        d_parts: list[str] = []
        for ring in rings:
            if len(ring) < 3:
                continue
            pts = [project(lon, lat) for lon, lat in ring]
            d_parts.append("M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z")
        if not d_parts:
            continue
        d_attr = "".join(d_parts)
        slug = slugify(name)
        paths.append(
            f'<path id="c{iso}" data-iso="{iso}" data-slug="{slug}" '
            f'data-name="{name}" d="{d_attr}"/>'
        )

    # Graticule (optional faint gridlines)
    graticule: list[str] = []
    for lon in range(-180, 181, 30):
        pts = [project(lon, lat) for lat in range(-80, 81, 5)]
        graticule.append("M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts))
    for lat in range(-60, 91, 30):
        pts = [project(lon, lat) for lon in range(-180, 181, 5)]
        graticule.append("M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts))

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {VIEW_W} {VIEW_H}" preserveAspectRatio="xMidYMid meet">'
        f'<g class="graticule" fill="none" stroke="rgba(148,163,184,0.15)" '
        f'stroke-width="0.4">'
        + "".join(f'<path d="{d}"/>' for d in graticule)
        + '</g>'
        f'<g class="countries" fill="#1f2a44" stroke="#0f172a" '
        f'stroke-width="0.5" stroke-linejoin="round">'
        + "".join(paths)
        + '</g></svg>'
    )
    SVG_PATH.write_text(svg)
    print(f"Wrote {SVG_PATH} ({SVG_PATH.stat().st_size:,} bytes, {len(paths)} countries)")


if __name__ == "__main__":
    main()
