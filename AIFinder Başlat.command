#!/bin/bash
# AIFinder'i baslatir ve tarayiciyi acar. Bu dosyaya cift tiklamak yeterlidir.
cd "$(dirname "$0")" || exit 1

if [ ! -x ".venv/bin/python" ]; then
  echo "Kurulum eksik: .venv bulunamadi."
  echo "Terminalde su komutu calistirin:"
  echo "  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  read -r -p "Kapatmak icin Enter'a basin..."
  exit 1
fi

PORT=9317
# Port doluysa bir sonrakini dene
while lsof -nP -iTCP:$PORT -sTCP:LISTEN >/dev/null 2>&1; do
  PORT=$((PORT + 1))
done

echo "AIFinder baslatiliyor — http://127.0.0.1:$PORT"
echo "Modeller ilk aciliista yuklenir (~15 sn)."
echo "Kapatmak icin bu pencerede Ctrl+C."
echo

( sleep 3; open "http://127.0.0.1:$PORT" ) &
PORT=$PORT .venv/bin/python app.py
