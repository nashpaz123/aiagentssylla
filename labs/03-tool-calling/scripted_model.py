"""Deterministic 'model' that emits tool_calls — does NOT execute tools."""

from __future__ import annotations

from typing import Any


def next_assistant_message(turn: int, observations: list[dict[str, Any]]) -> dict[str, Any]:
    """Return either tool_calls or a final text answer.

    Turn plan (for teaching):
      0: bad call (schema fail) — intentional
      1: fix + parallel sts + list_ec2
      2: final answer from observations
    """
    if turn == 0:
        return {
            "role": "assistant",
            "content": "Checking status label first.",
            "tool_calls": [
                {
                    "id": "call_bad_1",
                    "name": "echo_status",
                    "arguments": {"label": "healthy"},  # not in enum → SCHEMA error
                }
            ],
        }
    if turn == 1:
        return {
            "role": "assistant",
            "content": "Retrying with valid args, then parallel AWS reads.",
            "tool_calls": [
                {
                    "id": "call_echo_ok",
                    "name": "echo_status",
                    "arguments": {"label": "ok"},
                },
                {
                    "id": "call_sts",
                    "name": "sts_whoami",
                    "arguments": {},
                },
                {
                    "id": "call_ec2",
                    "name": "list_ec2_running",
                    "arguments": {"max_items": 5},
                },
            ],
        }
    # Final
    bits = []
    for obs in observations:
        if obs.get("ok"):
            bits.append(f"{obs.get('tool')}: ok")
        else:
            bits.append(f"{obs.get('tool')}: {obs.get('error')}")
    return {
        "role": "assistant",
        "content": "Summary from tool observations: " + "; ".join(bits[-5:]),
        "tool_calls": [],
    }
