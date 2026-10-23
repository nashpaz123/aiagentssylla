#!/usr/bin/env bash
# Send out/telegram.txt to your Telegram via Bot API.
# Requires TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID (env or .env in this folder).
set -euo pipefail
cd "$(dirname "$0")"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if [[ -z "${TELEGRAM_BOT_TOKEN:-}" || -z "${TELEGRAM_CHAT_ID:-}" ]]; then
  echo "Missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID"
  echo "Copy .env.example → .env and fill your bot + personal chat id."
  exit 1
fi

if [[ ! -f out/telegram.txt ]]; then
  echo "out/telegram.txt missing — run ./run-claude.sh smb first"
  exit 1
fi

python3 - <<'PY'
import json, os, pathlib, urllib.request
text = pathlib.Path("out/telegram.txt").read_text(encoding="utf-8")
token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]
url = f"https://api.telegram.org/bot{token}/sendMessage"
req = urllib.request.Request(
    url,
    data=json.dumps({"chat_id": chat_id, "text": text}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=30) as resp:
    body = json.loads(resp.read().decode())
print(json.dumps(body, ensure_ascii=False, indent=2))
if not body.get("ok"):
    raise SystemExit("Telegram API returned ok=false")
print("SENT to chat", chat_id)
PY
