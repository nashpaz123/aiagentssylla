#!/usr/bin/env python3
"""Host loop: model proposes tool_calls → validate/execute → observations.

Teaching demo for session 3. Read-only AWS tools. No resource creation.
"""

from __future__ import annotations

import json
from typing import Any

from scripted_model import next_assistant_message
from tools_registry import TOOLS, execute_tool_call


MAX_TURNS = 4


def main() -> int:
    print("GOAL: Demonstrate function-calling host (validate, parallel, observe).")
    print("CATALOG:", [t["name"] for t in TOOLS])
    print("---")

    all_observations: list[dict[str, Any]] = []
    turn = 0
    while turn < MAX_TURNS:
        msg = next_assistant_message(turn, all_observations)
        print(f"\n[turn {turn}] assistant content: {msg.get('content')}")
        calls = msg.get("tool_calls") or []
        if not calls:
            print("FINAL:", msg.get("content"))
            print("STOP: model_finished")
            print("GOAL_COMPLETE: True")
            return 0

        print(f"tool_calls ({len(calls)}):")
        for c in calls:
            print(" ", json.dumps(c, ensure_ascii=False))

        # Execute (parallel-safe tools run one after another here for clarity;
        # teaching point: host owns execution order / concurrency.)
        batch_obs: list[dict[str, Any]] = []
        for c in calls:
            result = execute_tool_call(c["name"], c.get("arguments") or {})
            obs = {
                "tool_call_id": c["id"],
                **result,
            }
            batch_obs.append(obs)
            all_observations.append(obs)
            print("OBSERVE:", json.dumps(obs, ensure_ascii=False)[:500])

        turn += 1

    print("STOP: max_turns")
    print("GOAL_COMPLETE: False")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
