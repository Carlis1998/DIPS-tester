#!/bin/bash
# Serve the DIPS Tester app locally for development.
# Serve from the repo root so both /app and /data are available.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "Serving DIPS-Tester from repo root: $ROOT"
echo "Open: http://localhost:8080/app/"
python3 -m http.server 8080
