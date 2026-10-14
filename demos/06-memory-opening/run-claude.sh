#!/usr/bin/env bash
# הדגמת פתיחה מפגש 6 — Claude Code + Store בקובץ (Memory בין תורות).
# שימוש:
#   ./run-claude.sh turn1          # C-99 / 99 → auto
#   ./run-claude.sh status         # C-99 שואל סטטוס (חייב לקרוא out/store.json)
#   ./run-claude.sh turn1-101      # C-101 / 101 → hitl
#   ./run-claude.sh reset          # מוחק out/store.json (+ stream)
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out

cmd="${1:-turn1}"
case "$cmd" in
  reset)
    rm -f out/store.json out/stream.jsonl out/*.md
    echo "Store cleared."; exit 0 ;;
  turn1)      prompt=prompt-turn1.md; label="turn1 C-99 amount=99" ;;
  turn1-101)  prompt=prompt-turn1-101.md; label="turn1 C-101 amount=101" ;;
  status)     prompt=prompt-status.md; label="status C-99" ;;
  *) echo "usage: $0 turn1|status|turn1-101|reset"; exit 1 ;;
esac

echo ">>> $label   (Claude Code, expect ~20-60s)"
echo

claude -p "$(cat "$prompt")" \
  --setting-sources project,local \
  --allowedTools "Read,Write,Glob,Grep,Task" \
  --max-turns 25 \
  --output-format stream-json --verbose \
| tee out/stream.jsonl \
| python3 -u stream_filter.py

echo
echo "---- out/store.json ----"
cat out/store.json 2>/dev/null || echo "(no store yet)"
