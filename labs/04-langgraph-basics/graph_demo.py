#!/usr/bin/env python3
"""Session 4 lab: tiny LangGraph with shared State + conditional edge.

No LLM API key required — deterministic demo for teaching graph structure.
"""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class DemoState(TypedDict):
    text: str
    path: str
    step_log: list[str]


def normalize(state: DemoState) -> dict:
    cleaned = " ".join(state["text"].split()).strip()
    log = list(state.get("step_log") or [])
    log.append(f"normalize: {cleaned!r}")
    print(f"[node:normalize] text -> {cleaned!r}")
    return {"text": cleaned, "step_log": log}


def route_by_length(state: DemoState) -> str:
    """Conditional edge: short vs long text paths."""
    choice = "short" if len(state["text"]) < 20 else "long"
    print(f"[edge:route_by_length] len={len(state['text'])} -> {choice}")
    return choice


def handle_short(state: DemoState) -> dict:
    log = list(state.get("step_log") or [])
    log.append("handle_short")
    print("[node:handle_short] taking short path")
    return {"path": "short", "step_log": log, "text": state["text"].upper()}


def handle_long(state: DemoState) -> dict:
    log = list(state.get("step_log") or [])
    log.append("handle_long")
    preview = state["text"][:40] + ("…" if len(state["text"]) > 40 else "")
    print(f"[node:handle_long] taking long path; preview={preview!r}")
    return {
        "path": "long",
        "step_log": log,
        "text": f"[summary] {state['text'][:60]}",
    }


def summarize(state: DemoState) -> dict:
    log = list(state.get("step_log") or [])
    log.append("summarize")
    print(f"[node:summarize] path={state['path']} final={state['text']!r}")
    return {"step_log": log}


def build_app():
    g = StateGraph(DemoState)
    g.add_node("normalize", normalize)
    g.add_node("handle_short", handle_short)
    g.add_node("handle_long", handle_long)
    g.add_node("summarize", summarize)

    g.add_edge(START, "normalize")
    g.add_conditional_edges(
        "normalize",
        route_by_length,
        {"short": "handle_short", "long": "handle_long"},
    )
    g.add_edge("handle_short", "summarize")
    g.add_edge("handle_long", "summarize")
    g.add_edge("summarize", END)
    return g.compile()


def run_case(app, label: str, text: str) -> None:
    print("\n" + "=" * 60)
    print(f"CASE: {label}")
    print(f"INPUT: {text!r}")
    print("-" * 60)
    result = app.invoke({"text": text, "path": "", "step_log": []})
    print("-" * 60)
    print("FINAL STATE:")
    print(f"  path     = {result['path']}")
    print(f"  text     = {result['text']!r}")
    print(f"  step_log = {result['step_log']}")
    print("GOAL_COMPLETE: True")


def main() -> int:
    print("Lab 04 — LangGraph basics (deterministic, no LLM key)")
    print("Graph: START → normalize → (short|long) → summarize → END")
    app = build_app()
    run_case(app, "short branch", "hi there")
    run_case(
        app,
        "long branch",
        "please review this longer customer message about a delayed order",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
