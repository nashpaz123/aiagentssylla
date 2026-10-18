#!/usr/bin/env bash
# הדגמת פתיחה מפגש 7 — Claude Code + Sales Ops (CRM → Quote → HITL).
# שימוש:
#   ./run-claude.sh reset
#   ./run-claude.sh smb           # L-SMB / 5% → auto
#   ./run-claude.sh enterprise    # L-ENT / 18% → hitl
#   ./run-claude.sh nomail        # L-NOMAIL → blocked
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out

SEED_CRM='crm/leads.seed.json'
if [[ ! -f "$SEED_CRM" ]]; then
  cp crm/leads.json "$SEED_CRM"
fi

cmd="${1:-smb}"
case "$cmd" in
  reset)
    cp "$SEED_CRM" crm/leads.json
    rm -f out/quotes.json out/email_draft.md out/stream.jsonl
    echo "CRM restored from seed; quotes cleared."; exit 0 ;;
  smb)         prompt=prompt-smb.md; label="L-SMB discount=5% → expect auto" ;;
  enterprise)  prompt=prompt-enterprise.md; label="L-ENT discount=18% → expect hitl" ;;
  nomail)      prompt=prompt-nomail.md; label="L-NOMAIL → expect blocked/need_email" ;;
  *) echo "usage: $0 smb|enterprise|nomail|reset"; exit 1 ;;
esac

echo ">>> $label   (Claude Code, expect ~20-90s)"
echo

claude -p "$(cat "$prompt")" \
  --setting-sources project,local \
  --allowedTools "Read,Write,Glob,Grep,Task" \
  --max-turns 30 \
  --output-format stream-json --verbose \
| tee out/stream.jsonl \
| python3 -u stream_filter.py

echo
echo "---- out/quotes.json ----"
cat out/quotes.json 2>/dev/null || echo "(no quotes yet)"
echo
echo "---- crm stages ----"
python3 - <<'PY'
import json
from pathlib import Path
leads=json.loads(Path("crm/leads.json").read_text())
for k,v in leads.items():
    print(f"  {k}: stage={v.get('stage')} email={v.get('email')!r} discount={v.get('requested_discount_pct')}%")
PY
