#!/usr/bin/env bash
# הדגמת פתיחה למפגש 5 — צוות של 3 subagents ב-Claude Code.
# דרישה: Claude Code מותקן ומחובר (הריצו `claude` פעם אחת אינטראקטיבית לפני ההקלטה).
#
# הפלט מוזרם בזמן אמת: כל קריאה ל-subagent, כל כתיבת קובץ, וההודעה הסופית.
# (במצב --output-format text אין שום פלט עד הסוף — כ-60–90 שניות — וזה נראה "תקוע".)
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out
rm -f out/*.md

echo ">>> starting crew: researcher -> writer -> reviewer   (expect ~60-90s)"
echo

# --setting-sources project,local: מתעלמים מ-~/.claude/settings.json האישי (כללי הרשאה/hooks של פרויקטים אחרים),
# כדי שהפלט בהקלטה יהיה נקי מאזהרות שלא קשורות להדגמה. ההתחברות (OAuth) לא מושפעת.
claude -p "$(cat prompt.md)" \
  --setting-sources project,local \
  --allowedTools "Read,Write,Glob,Grep,Task" \
  --max-turns 40 \
  --output-format stream-json --verbose \
| tee out/stream.jsonl \
| python3 -u stream_filter.py

echo
echo "---- out/ ----"
ls -la out/
echo "---- out/review.md ----"
cat out/review.md 2>/dev/null || echo "(no review.md)"
