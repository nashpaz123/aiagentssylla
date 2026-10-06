#!/usr/bin/env python3
"""Session 4 lab (part 2): Checkpoint + thread_id + interrupt → resume.

Deterministic, no LLM key. Shows why HITL (Human In The Loop) needs a
checkpointer: the graph pauses at a sensitive node, a "human" answers,
and the run resumes from the same thread_id.
"""

from __future__ import annotations

import sys
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

MAX_STEPS = 5


class RefundState(TypedDict):
    customer_id: str
    amount: int
    order_status: str
    needs_hitl: bool
    decision: str
    step_count: int
    step_log: list[str]


def _log(state: RefundState, msg: str) -> list[str]:
    log = list(state.get("step_log") or [])
    log.append(msg)
    print(f"[node] {msg}")
    return log


def lookup_order(state: RefundState) -> dict:
    status = "shipped"  # pretend tool call
    return {
        "order_status": status,
        "step_count": state["step_count"] + 1,
        "step_log": _log(state, f"lookup_order -> order_status={status}"),
    }


def policy(state: RefundState) -> dict:
    # Policy Gate: refunds above 100 need a human.
    needs = state["amount"] > 100
    return {
        "needs_hitl": needs,
        "step_count": state["step_count"] + 1,
        "step_log": _log(state, f"policy -> needs_hitl={needs} (amount={state['amount']})"),
    }


def route_after_policy(state: RefundState) -> str:
    if state["step_count"] >= MAX_STEPS:
        return "end"
    return "hitl" if state["needs_hitl"] else "auto"


def hitl_approve(state: RefundState) -> dict:
    # Graph PAUSES here. interrupt() returns the human's value on resume.
    answer = interrupt(
        {
            "action": "issue_refund",
            "amount": state["amount"],
            "customer_id": state["customer_id"],
            "risk": "irreversible money move",
            "options": ["approve", "reject"],
        }
    )
    return {
        "decision": f"human:{answer}",
        "step_count": state["step_count"] + 1,
        "step_log": _log(state, f"hitl_approve -> resumed with {answer!r}"),
    }


def auto_approve(state: RefundState) -> dict:
    return {
        "decision": "auto:approve",
        "step_count": state["step_count"] + 1,
        "step_log": _log(state, "auto_approve -> small amount, no human"),
    }


def build_app():
    g = StateGraph(RefundState)
    g.add_node("lookup_order", lookup_order)
    g.add_node("policy", policy)
    g.add_node("hitl_approve", hitl_approve)
    g.add_node("auto_approve", auto_approve)

    g.add_edge(START, "lookup_order")
    g.add_edge("lookup_order", "policy")
    g.add_conditional_edges(
        "policy",
        route_after_policy,
        {"hitl": "hitl_approve", "auto": "auto_approve", "end": END},
    )
    g.add_edge("hitl_approve", END)
    g.add_edge("auto_approve", END)

    # Without a checkpointer there is nowhere to pause/resume.
    return g.compile(checkpointer=InMemorySaver())


def initial(customer_id: str, amount: int) -> RefundState:
    return {
        "customer_id": customer_id,
        "amount": amount,
        "order_status": "",
        "needs_hitl": False,
        "decision": "",
        "step_count": 0,
        "step_log": [],
    }


def run_small(app) -> None:
    print("\n" + "=" * 60)
    print("CASE A: amount=40 -> policy says no human needed")
    config = {"configurable": {"thread_id": "ticket-0040"}}
    result = app.invoke(initial("C-1", 40), config=config)
    print(f"decision = {result['decision']}")
    print(f"step_log = {result['step_log']}")
    print("GOAL_COMPLETE: True")


def run_hitl(app, human_answer: str) -> None:
    print("\n" + "=" * 60)
    print("CASE B: amount=249 -> interrupt, then resume on SAME thread_id")
    config = {"configurable": {"thread_id": "ticket-0249"}}

    result = app.invoke(initial("C-2", 249), config=config)
    pending = result.get("__interrupt__")
    if not pending:
        print("unexpected: graph did not pause")
        return
    payload = pending[0].value
    print("\n--- PAUSED. Payload shown to the human: ---")
    for k, v in payload.items():
        print(f"  {k}: {v}")

    snap = app.get_state(config)
    print(f"--- checkpoint exists · next node = {snap.next} ---")

    print(f"\n--- human answers: {human_answer!r} -> Command(resume=...) ---")
    result = app.invoke(Command(resume=human_answer), config=config)
    print(f"decision = {result['decision']}")
    print(f"step_log = {result['step_log']}")
    print("GOAL_COMPLETE: True")


def run_wrong_thread(app) -> None:
    print("\n" + "=" * 60)
    print("CASE C: resume with a DIFFERENT thread_id -> nothing to resume")
    config = {"configurable": {"thread_id": "ticket-9999"}}
    snap = app.get_state(config)
    print(f"get_state(ticket-9999).values = {snap.values}")
    print("Lesson: wrong/new thread_id = empty memory. Keep the id stable.")


def main() -> int:
    answer = sys.argv[1] if len(sys.argv) > 1 else "approve"
    if answer not in {"approve", "reject"}:
        print("usage: python3 hitl_demo.py [approve|reject]")
        return 2
    print("Lab 04 (part 2) — Checkpoint · thread_id · interrupt · resume")
    print("Graph: START -> lookup_order -> policy -> (hitl_approve | auto_approve) -> END")
    app = build_app()
    run_small(app)
    run_hitl(app, answer)
    run_wrong_thread(app)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
