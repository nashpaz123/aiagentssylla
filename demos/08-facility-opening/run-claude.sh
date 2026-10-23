#!/usr/bin/env bash
# הדגמת פתיחה מפגש 8B — Claude Code → Facility HTML + Telegram text.
# אחרי הריצה: ./send-telegram.sh שולח את out/telegram.txt לצ׳אט שלכם.
# שימוש:
#   ./run-claude.sh reset
#   ./run-claude.sh hvac      # WO-HVAC → open (כחול)
#   ./run-claude.sh elev      # WO-ELEV → sla_breach (אדום)
#   ./send-telegram.sh
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out

cmd="${1:-hvac}"
case "$cmd" in
  reset)
    rm -f out/work_order.html out/telegram.txt out/stream.jsonl
    echo "Facility surfaces cleared."; exit 0 ;;
  hvac) prompt=prompt-hvac.md; label="WO-HVAC → HTML+Telegram (expect open/blue)" ;;
  elev) prompt=prompt-elev.md; label="WO-ELEV → HTML+Telegram (expect sla_breach/red)" ;;
  *) echo "usage: $0 hvac|elev|reset"; exit 1 ;;
esac

echo ">>> $label   (Claude Code, expect ~20-90s)"
echo

claude -p "$(cat "$prompt")" \
  --setting-sources project,local \
  --allowedTools "Read,Write,Edit,Glob,Grep,Task" \
  --max-turns 25 \
  --output-format stream-json --verbose \
| tee out/stream.jsonl \
|| python3 -u stream_filter.py

echo
echo "---- out/telegram.txt ----"
cat out/telegram.txt 2>/dev/null || echo "(no telegram.txt yet)"
echo
echo "---- out/work_order.html (exists?) ----"
ls -la out/work_order.html 2>/dev/null || echo "(no html yet)"
echo "Open: file://$(pwd)/out/work_order.html"
echo
echo "Next: ./send-telegram.sh   # sends out/telegram.txt to your Telegram"
