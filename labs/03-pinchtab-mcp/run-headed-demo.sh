#!/usr/bin/env bash
# PinchTab headed demo for Session 3 MCP section.
# Mirrors what an MCP client would call (navigate → snapshot → text → screenshot),
# but via CLI so you can watch the browser and run it without wiring MCP mid-recording.
#
# Requires: pinchtab on PATH, Chrome/Chromium installed.
# You run this on your laptop (headed). Safe demo URL: https://example.com

set -euo pipefail

DEMO_URL="${PINCHTAB_DEMO_URL:-https://example.com}"
OUT_DIR="${PINCHTAB_DEMO_OUT:-$(pwd)/out}"
AGENT_ID="${PINCHTAB_AGENT_ID:-aiagentssylla-s3-mcp}"

mkdir -p "$OUT_DIR"

echo "== PinchTab headed MCP-style demo =="
echo "Local paths worth showing on camera:"
echo "  ~/.pinchtab/                 (state + config.json + profiles/)"
echo "  ~/.claude/skills/pinchtab/   (skill + references/mcp.md)"
echo "  $(pwd)                       (this lab)"
echo
echo "URL:  $DEMO_URL"
echo "Out:  $OUT_DIR"
echo

if ! command -v pinchtab >/dev/null 2>&1; then
  echo "ERROR: pinchtab not found. Install: npm i -g pinchtab  OR  brew install pinchtab/tap/pinchtab" >&2
  exit 1
fi

echo "-- health / server (headed) --"
if ! pinchtab health >/dev/null 2>&1; then
  echo "Starting PinchTab server in HEADED mode (-H) in background..."
  pinchtab server -H -b
  sleep 2
else
  echo "Server already up. If the window is headless, restart headed:"
  echo "  pinchtab server stop && pinchtab server -H -b"
fi

pinchtab health || true

echo
echo "-- session (dedicated tab for this agent) --"
export PINCHTAB_SESSION
PINCHTAB_SESSION="$(pinchtab session create --agent-id "$AGENT_ID")"
echo "PINCHTAB_SESSION=$PINCHTAB_SESSION"

echo
echo "-- MCP-equivalent: pinchtab_navigate + snapshot --"
pinchtab nav "$DEMO_URL" --snap | tee "$OUT_DIR/01-snap.txt"

echo
echo "-- MCP-equivalent: pinchtab_get_text --"
pinchtab text | tee "$OUT_DIR/02-text.txt"

echo
echo "-- MCP-equivalent: pinchtab_screenshot --"
pinchtab screenshot -o "$OUT_DIR/03-screenshot.png"
echo "Wrote $OUT_DIR/03-screenshot.png"

echo
echo "-- optional: list tabs --"
pinchtab tab || true

echo
echo "DONE."
echo "What you just saw is the same contract MCP exposes:"
echo "  Host (you/agent) → MCP Client → PinchTab MCP Server → browser tools"
echo "Wire MCP into Cursor with: mcp.cursor.example.json"
echo "Keep the headed Chrome window open while you inspect refs in 01-snap.txt"
