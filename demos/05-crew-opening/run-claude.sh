#!/usr/bin/env bash
# הדגמת פתיחה למפגש 5 — צוות של 3 subagents ב-Claude Code.
# דרישה: Claude Code מותקן ומחובר (הריצו `claude` פעם אחת אינטראקטיבית לפני ההקלטה).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out
rm -f out/*.md

# --setting-sources project,local: מתעלמים מ-~/.claude/settings.json האישי (כללי הרשאה/hooks של פרויקטים אחרים),
# כדי שהפלט בהקלטה יהיה נקי מאזהרות שלא קשורות להדגמה. ההתחברות (OAuth) לא מושפעת.
claude -p "$(cat prompt.md)" \
  --setting-sources project,local \
  --allowedTools "Read,Write,Glob,Grep,Task" \
  --max-turns 40 \
  --output-format text

echo
echo "---- out/ ----"
ls -la out/
echo "---- out/review.md ----"
cat out/review.md 2>/dev/null || echo "(no review.md)"
