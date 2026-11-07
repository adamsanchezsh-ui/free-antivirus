#!/bin/sh
cd "$(dirname "$0")"
command -v python3 >/dev/null || { echo "Nainstaluj Python 3."; exit 1; }
command -v clamscan >/dev/null || { echo "Nainstaluj ClamAV (apt install clamav / brew install clamav)."; exit 1; }
echo "Aktualizuji databazi virus..."
freshclam 2>/dev/null || echo "(freshclam selhal, zkus: sudo freshclam)"
( sleep 1; xdg-open http://127.0.0.1:8765 2>/dev/null || open http://127.0.0.1:8765 2>/dev/null ) &
python3 app.py
