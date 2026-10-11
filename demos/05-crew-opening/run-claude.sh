#!/usr/bin/env bash
# הדגמת פתיחה למפגש 5 — צוות של 3 subagents ב-Claude Code.
# דרישה: Claude Code מותקן ומחובר (הריצו `claude` פעם אחת אינטראקטיבית לפני ההקלטה).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out
rm -f out/*.md

claude -p "$(cat prompt.md)" \
  --allowedTools "Read,Write,Glob,Grep,Task" \
  --max-turns 40 \
  --output-format text

echo
echo "---- out/ ----"
ls -la out/
echo "---- out/review.md ----"
cat out/review.md 2>/dev/null || echo "(no review.md)"
