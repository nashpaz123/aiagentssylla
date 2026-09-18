#!/usr/bin/env python3
"""Minimal read-only Planning → Execute → Observe → Re-plan demo for session 2.

Uses cheap AWS APIs only. Safe defaults: no create/update/delete.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError as exc:  # pragma: no cover
    raise SystemExit("pip install boto3") from exc


MAX_ITERATIONS = 5
REGION = (
    os.environ.get("AWS_REGION")
    or os.environ.get("AWS_DEFAULT_REGION")
    or "eu-north-1"
)
# Prefer the course demo profile unless the caller already set AWS_PROFILE.
os.environ.setdefault("AWS_PROFILE", "nashpazformatan")
os.environ.setdefault("AWS_DEFAULT_PROFILE", "nashpazformatan")


@dataclass
class State:
    goal: str
    plan: list[str]
    current_step: int = 0
    findings: list[str] = field(default_factory=list)
    iterations: int = 0
    done: bool = False
    stop_reason: str = ""


def tool_sts_whoami() -> dict[str, Any]:
    client = boto3.client("sts", region_name=REGION)
    return client.get_caller_identity()


def tool_cloudwatch_sample() -> dict[str, Any]:
    """Fetch a tiny CloudWatch sample for EC2 CPU (may be empty — that's OK for demo)."""
    client = boto3.client("cloudwatch", region_name=REGION)
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=1)
    resp = client.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "cpu",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",
                        "MetricName": "CPUUtilization",
                    },
                    "Period": 300,
                    "Stat": "Average",
                },
                "ReturnData": True,
            }
        ],
        StartTime=start,
        EndTime=end,
    )
    results = resp.get("MetricDataResults", [])
    values = results[0].get("Values", []) if results else []
    return {
        "region": REGION,
        "points": len(values),
        "sample": values[:3],
        "status": results[0].get("StatusCode") if results else "Empty",
    }


TOOLS: dict[str, Callable[[], dict[str, Any]]] = {
    "sts_whoami": tool_sts_whoami,
    "cloudwatch_sample": tool_cloudwatch_sample,
}


def initial_plan() -> list[str]:
    return [
        "sts_whoami",
        "cloudwatch_sample",
        "summarize",
    ]


def replan_local(state: State, last_tool: str, observation: dict[str, Any]) -> None:
    """Cheap local re-plan: if CloudWatch empty, skip chasing metrics and summarize early."""
    if last_tool == "cloudwatch_sample" and observation.get("points", 0) == 0:
        state.findings.append(
            "CloudWatch returned 0 points — likely no EC2 metrics in this account/region."
        )
        # Drop remaining metric hunting; jump to summarize.
        state.plan = state.plan[: state.current_step + 1] + ["summarize"]
        state.findings.append("Local re-plan: skip further metrics → summarize with Evidence.")


def summarize(state: State) -> str:
    return json.dumps(
        {
            "goal": state.goal,
            "findings": state.findings,
            "iterations": state.iterations,
            "stop": state.stop_reason or "goal_check",
        },
        ensure_ascii=False,
        indent=2,
    )


def run() -> None:
    state = State(
        goal="Confirm AWS access and sample whether EC2 CPU metrics exist (read-only).",
        plan=initial_plan(),
    )
    print("GOAL:", state.goal)
    print("INITIAL PLAN:", state.plan)
    print("---")

    while not state.done and state.iterations < MAX_ITERATIONS:
        state.iterations += 1
        if state.current_step >= len(state.plan):
            state.done = True
            state.stop_reason = "plan_exhausted"
            break

        step = state.plan[state.current_step]
        print(f"\n[iter {state.iterations}] step={step}")

        if step == "summarize":
            state.findings.append("Reached summarize step.")
            print(summarize(state))
            state.done = True
            state.stop_reason = "success_criteria_met"
            break

        fn = TOOLS.get(step)
        if not fn:
            state.findings.append(f"Unknown step {step}")
            state.done = True
            state.stop_reason = "failure_unknown_step"
            break

        try:
            observation = fn()
            print("OBSERVE:", json.dumps(observation, default=str)[:500])
            state.findings.append(f"{step} ok: {str(observation)[:160]}")
            replan_local(state, step, observation)
            print("PLAN NOW:", state.plan)
        except (BotoCoreError, ClientError) as err:
            print("OBSERVE ERROR:", err)
            state.findings.append(f"{step} failed: {err}")
            # Local re-plan: try summarize with what we have.
            state.plan = state.plan[: state.current_step + 1] + ["summarize"]
            print("PLAN NOW (after error):", state.plan)

        state.current_step += 1
        time.sleep(0.3)

    if not state.done:
        state.stop_reason = "max_iterations"
    print("\nSTOP:", state.stop_reason)
    print("FINDINGS:")
    for item in state.findings:
        print("-", item)


if __name__ == "__main__":
    run()
