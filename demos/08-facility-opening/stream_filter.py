#!/usr/bin/env python3
"""Turn `claude -p --output-format stream-json --verbose` into a readable live log.

Prints one line per orchestrator action (Task -> subagent, Write, Read, text),
then the final result and run stats. Used by run-claude.sh.
"""
import json
import sys
import time

t0 = time.time()


def ts() -> str:
    return f"[{time.time() - t0:5.1f}s]"


for raw in sys.stdin:
    raw = raw.strip()
    if not raw:
        continue
    try:
        ev = json.loads(raw)
    except Exception:
        continue
    typ = ev.get("type")

    if typ == "system" and ev.get("subtype") == "init":
        agents = ev.get("agents") or []
        print(f"{ts()} INIT  model={ev.get('model')} agents={agents}", flush=True)

    elif typ == "assistant":
        for c in ev.get("message", {}).get("content", []):
            ctype = c.get("type")
            if ctype == "tool_use":
                name, inp = c.get("name"), c.get("input", {}) or {}
                if name in ("Task", "Agent"):  # subagent call (tool name differs between Claude Code versions)
                    who = inp.get("subagent_type") or inp.get("agent") or inp.get("name") or "?"
                    print(f"{ts()} TASK  -> subagent {who!r}: {inp.get('description', '')}", flush=True)
                elif name in ("Write", "Edit"):
                    print(f"{ts()} WRITE -> {inp.get('file_path', '')}", flush=True)
                elif name == "Read":
                    print(f"{ts()} READ  -> {inp.get('file_path', '')}", flush=True)
                else:
                    print(f"{ts()} TOOL  -> {name}", flush=True)
            elif ctype == "text" and c.get("text", "").strip():
                print(f"{ts()} ORCHESTRATOR: {c['text'].strip()[:300]}", flush=True)

    elif typ == "user":
        # tool results coming back to the orchestrator (e.g. a subagent's final message)
        for c in ev.get("message", {}).get("content", []) or []:
            if isinstance(c, dict) and c.get("type") == "tool_result":
                content = c.get("content")
                if isinstance(content, list):
                    content = " ".join(x.get("text", "") for x in content if isinstance(x, dict))
                snippet = (content or "").strip().replace("\n", " ")[:160]
                if snippet:
                    print(f"{ts()} RESULT<- {snippet}", flush=True)

    elif typ == "result":
        dur = ev.get("duration_ms") or 0
        print()
        print("=" * 70)
        print(ev.get("result", ""))
        print("=" * 70)
        print(f"turns={ev.get('num_turns')} duration={dur / 1000:.0f}s cost_usd={ev.get('total_cost_usd')}", flush=True)
