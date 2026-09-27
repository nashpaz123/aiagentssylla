#!/usr/bin/env python3
"""Minimal read-only Planning → Execute → Observe → Re-plan demo for session 2.

Uses cheap AWS APIs only. Safe defaults: no create/update/delete.

Goal is fully met when:
  1) STS identity is confirmed, and
  2) We answered whether EC2 CPU metrics exist — either by sampling
     CPUUtilization for a running instance (with InstanceId dimension),
     or by observing that there are no running instances to sample.
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


MAX_ITERATIONS = 8
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
    # Working memory for later tools / success check
    identity_ok: bool = False
    instance_ids: list[str] = field(default_factory=list)
    metrics_sampled: bool = False
    metrics_points: int = 0
    cw_retries: int = 0


def tool_sts_whoami() -> dict[str, Any]:
    client = boto3.client("sts", region_name=REGION)
    return client.get_caller_identity()


def tool_list_ec2_running() -> dict[str, Any]:
    """List running EC2 instances (read-only). Needed to query CPU by InstanceId."""
    client = boto3.client("ec2", region_name=REGION)
    resp = client.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )
    instances: list[dict[str, Any]] = []
    for reservation in resp.get("Reservations", []):
        for inst in reservation.get("Instances", []):
            name = next(
                (t["Value"] for t in inst.get("Tags", []) if t.get("Key") == "Name"),
                None,
            )
            instances.append(
                {
                    "instance_id": inst["InstanceId"],
                    "instance_type": inst.get("InstanceType"),
                    "az": (inst.get("Placement") or {}).get("AvailabilityZone"),
                    "name": name,
                }
            )
    return {
        "region": REGION,
        "running_count": len(instances),
        "instances": instances,
    }


def tool_cloudwatch_sample(instance_ids: list[str]) -> dict[str, Any]:
    """Fetch EC2 CPUUtilization for specific instance IDs (required dimension)."""
    if not instance_ids:
        return {
            "region": REGION,
            "points": 0,
            "sample": [],
            "status": "skipped_no_instances",
            "instance_ids": [],
        }

    client = boto3.client("cloudwatch", region_name=REGION)
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=1)

    queries = []
    for idx, instance_id in enumerate(instance_ids[:5]):  # cap queries
        queries.append(
            {
                "Id": f"cpu{idx}",
                "MetricStat": {
                    "Metric": {
                        "Namespace": "AWS/EC2",
                        "MetricName": "CPUUtilization",
                        "Dimensions": [
                            {"Name": "InstanceId", "Value": instance_id},
                        ],
                    },
                    "Period": 300,
                    "Stat": "Average",
                },
                "ReturnData": True,
            }
        )

    resp = client.get_metric_data(
        MetricDataQueries=queries,
        StartTime=start,
        EndTime=end,
    )
    results = resp.get("MetricDataResults", [])
    per_instance: list[dict[str, Any]] = []
    total_points = 0
    sample_vals: list[float] = []
    for idx, result in enumerate(results):
        values = result.get("Values") or []
        total_points += len(values)
        sample_vals.extend(values[:2])
        per_instance.append(
            {
                "instance_id": instance_ids[idx] if idx < len(instance_ids) else "?",
                "points": len(values),
                "sample": values[:3],
                "status": result.get("StatusCode"),
            }
        )

    return {
        "region": REGION,
        "points": total_points,
        "sample": sample_vals[:5],
        "status": "Complete",
        "per_instance": per_instance,
        "instance_ids": instance_ids[:5],
    }


def initial_plan() -> list[str]:
    return [
        "sts_whoami",
        "list_ec2_running",
        "cloudwatch_sample",
        "summarize",
    ]


def goal_complete(state: State) -> bool:
    """Goal: AWS access confirmed AND we know whether EC2 CPU metrics exist."""
    if not state.identity_ok:
        return False
    if not state.instance_ids:
        # Answered: no running EC2 → no instance CPU metrics to sample.
        return True
    return state.metrics_sampled and state.metrics_points > 0


def replan_local(state: State, last_tool: str, observation: dict[str, Any]) -> None:
    if last_tool == "sts_whoami":
        state.identity_ok = True
        return

    if last_tool == "list_ec2_running":
        ids = [i["instance_id"] for i in observation.get("instances", [])]
        state.instance_ids = ids
        if not ids:
            state.findings.append(
                "No running EC2 instances — cannot sample instance CPU; goal answer = metrics do not exist for running fleet."
            )
            state.plan = state.plan[: state.current_step + 1] + ["summarize"]
            state.findings.append("Local re-plan: skip CloudWatch → summarize.")
        return

    if last_tool == "cloudwatch_sample":
        state.metrics_sampled = True
        state.metrics_points = int(observation.get("points") or 0)
        if state.metrics_points > 0:
            state.findings.append(
                f"EC2 CPU metrics exist: {state.metrics_points} datapoint(s) for {observation.get('instance_ids')}."
            )
            return

        # Metrics lag after launch — retry a couple of times (still read-only).
        if state.cw_retries < 2 and state.instance_ids:
            state.cw_retries += 1
            wait_s = 20
            state.findings.append(
                f"CloudWatch empty for {state.instance_ids}; wait {wait_s}s and retry ({state.cw_retries}/2)."
            )
            print(f"WAITING {wait_s}s for CloudWatch (retry {state.cw_retries}/2)...")
            time.sleep(wait_s)
            # Re-queue cloudwatch_sample then summarize.
            state.plan = (
                state.plan[: state.current_step + 1]
                + ["cloudwatch_sample", "summarize"]
            )
            state.findings.append("Local re-plan: retry cloudwatch_sample.")
            return

        state.findings.append(
            "CloudWatch still empty after retries — instances exist but no CPU datapoints yet."
        )
        state.plan = state.plan[: state.current_step + 1] + ["summarize"]
        state.findings.append("Local re-plan: stop retrying → summarize with Evidence.")


def summarize(state: State) -> str:
    return json.dumps(
        {
            "goal": state.goal,
            "goal_complete": goal_complete(state),
            "identity_ok": state.identity_ok,
            "running_instances": state.instance_ids,
            "metrics_sampled": state.metrics_sampled,
            "metrics_points": state.metrics_points,
            "findings": state.findings,
            "iterations": state.iterations,
            "stop": state.stop_reason or "goal_check",
        },
        ensure_ascii=False,
        indent=2,
    )


def run_tool(step: str, state: State) -> dict[str, Any]:
    if step == "sts_whoami":
        return tool_sts_whoami()
    if step == "list_ec2_running":
        return tool_list_ec2_running()
    if step == "cloudwatch_sample":
        return tool_cloudwatch_sample(state.instance_ids)
    raise KeyError(step)


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
            complete = goal_complete(state)
            state.stop_reason = (
                "success_criteria_met" if complete else "incomplete_goal"
            )
            print(summarize(state))
            state.done = True
            break

        try:
            observation = run_tool(step, state)
            print("OBSERVE:", json.dumps(observation, default=str)[:800])
            state.findings.append(f"{step} ok: {str(observation)[:200]}")
            replan_local(state, step, observation)
            print("PLAN NOW:", state.plan)
        except (BotoCoreError, ClientError, KeyError) as err:
            print("OBSERVE ERROR:", err)
            state.findings.append(f"{step} failed: {err}")
            state.plan = state.plan[: state.current_step + 1] + ["summarize"]
            print("PLAN NOW (after error):", state.plan)

        state.current_step += 1
        time.sleep(0.3)

    if not state.done:
        state.stop_reason = "max_iterations"
        print(summarize(state))

    print("\nSTOP:", state.stop_reason)
    print("GOAL_COMPLETE:", goal_complete(state))
    print("FINDINGS:")
    for item in state.findings:
        print("-", item)

    if not goal_complete(state):
        raise SystemExit(2)


if __name__ == "__main__":
    run()
