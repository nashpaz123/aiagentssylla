#!/usr/bin/env bash
# הדגמת פתיחה מפגש 8 — Claude Code → HTML card + Telegram text.
# אחרי הריצה: ./send-telegram.sh שולח את out/telegram.txt לצ׳אט שלכם.
# שימוש:
#   ./run-claude.sh reset
#   ./run-claude.sh smb           # L-SMB → out/briefing.html + telegram.txt
#   ./run-claude.sh enterprise    # L-ENT → hitl styling
#   ./send-telegram.sh            # שליחה אמיתית (דורש .env)
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out

cmd="${1:-smb}"
case "$cmd" in
  reset)
    rm -f out/briefing.html out/telegram.txt out/stream.jsonl
    echo "Surfaces cleared."; exit 0 ;;
  smb)         prompt=prompt-smb.md; label="L-SMB → HTML+Telegram (expect auto)" ;;
  enterprise)  prompt=prompt-enterprise.md; label="L-ENT → HTML+Telegram (expect hitl)" ;;
  *) echo "usage: $0 smb|enterprise|reset"; exit 1 ;;
esac

echo ">>> $label   (Claude Code, expect ~20-90s)"
echo

claude -p "$(cat "$prompt")" \
  --setting-sources project,local \
  --allowedTools "Read,Write,Edit,Glob,Grep,Task" \
  --max-turns 25 \
  --output-format stream-json --verbose \
| tee out/stream.jsonl \
| python3 -u stream_filter.py

echo
echo "---- out/telegram.txt ----"
cat out/telegram.txt 2>/dev/null || echo "(no telegram.txt yet)"
echo
echo "---- out/briefing.html (exists?) ----"
ls -la out/briefing.html 2>/dev/null || echo "(no html yet)"
echo "Open: file://$(pwd)/out/briefing.html"
echo
echo "Next: ./send-telegram.sh   # sends out/telegram.txt to your Telegram"
