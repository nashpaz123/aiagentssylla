"""Tool schemas + handlers for session 3 lab (read-only where AWS)."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Callable

try:
    import boto3
except ImportError:  # pragma: no cover
    boto3 = None  # type: ignore

REGION = (
    os.environ.get("AWS_REGION")
    or os.environ.get("AWS_DEFAULT_REGION")
    or "eu-north-1"
)
os.environ.setdefault("AWS_PROFILE", "nashpazformatan")
os.environ.setdefault("AWS_DEFAULT_PROFILE", "nashpazformatan")


TOOLS: list[dict[str, Any]] = [
    {
        "name": "echo_status",
        "description": "Local demo tool. Echo a status label. Not for AWS.",
        "parameters": {
            "type": "object",
            "properties": {
                "label": {
                    "type": "string",
                    "enum": ["ok", "degraded", "down"],
                    "description": "Status label to echo",
                }
            },
            "required": ["label"],
        },
        "side_effect": "none",
        "parallel_safe": True,
        "idempotent": True,
    },
    {
        "name": "sts_whoami",
        "description": "Return AWS caller identity (read-only). Use to confirm credentials.",
        "parameters": {"type": "object", "properties": {}, "required": []},
        "side_effect": "read",
        "parallel_safe": True,
        "idempotent": True,
    },
    {
        "name": "list_ec2_running",
        "description": "List running EC2 instances in the region (read-only DescribeInstances).",
        "parameters": {
            "type": "object",
            "properties": {
                "max_items": {
                    "type": "integer",
                    "description": "Max instances to return (1..20)",
                }
            },
            "required": [],
        },
        "side_effect": "read",
        "parallel_safe": True,
        "idempotent": True,
    },
]


def _validate(schema: dict[str, Any], args: dict[str, Any]) -> str | None:
    props = schema.get("properties") or {}
    required = schema.get("required") or []
    if not isinstance(args, dict):
        return "arguments must be an object"
    for key in required:
        if key not in args:
            return f"missing required: {key}"
    for key, val in args.items():
        if key not in props:
            return f"unknown property: {key}"
        spec = props[key]
        t = spec.get("type")
        if t == "string" and not isinstance(val, str):
            return f"{key} must be string"
        if t == "integer" and not isinstance(val, int):
            return f"{key} must be integer"
        enum = spec.get("enum")
        if enum is not None and val not in enum:
            return f"{key} not in enum {enum}"
    if "max_items" in args:
        n = args["max_items"]
        if n < 1 or n > 20:
            return "max_items must be 1..20"
    return None


def handle_echo_status(args: dict[str, Any]) -> dict[str, Any]:
    return {
        "label": args["label"],
        "echoed_at": datetime.now(timezone.utc).isoformat(),
    }


def handle_sts_whoami(_args: dict[str, Any]) -> dict[str, Any]:
    if boto3 is None:
        raise RuntimeError("boto3 not installed")
    client = boto3.client("sts", region_name=REGION)
    ident = client.get_caller_identity()
    return {
        "Account": ident.get("Account"),
        "Arn": ident.get("Arn"),
        "UserId": ident.get("UserId"),
    }


def handle_list_ec2_running(args: dict[str, Any]) -> dict[str, Any]:
    if boto3 is None:
        raise RuntimeError("boto3 not installed")
    max_items = int(args.get("max_items") or 10)
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
                    "name": name,
                }
            )
            if len(instances) >= max_items:
                break
        if len(instances) >= max_items:
            break
    return {"region": REGION, "running_count": len(instances), "instances": instances}


HANDLERS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "echo_status": handle_echo_status,
    "sts_whoami": handle_sts_whoami,
    "list_ec2_running": handle_list_ec2_running,
}


def get_tool(name: str) -> dict[str, Any] | None:
    for t in TOOLS:
        if t["name"] == name:
            return t
    return None


def execute_tool_call(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    tool = get_tool(name)
    if tool is None:
        return {"ok": False, "tool": name, "error": {"code": "UNKNOWN_TOOL", "message": name}}
    err = _validate(tool["parameters"], arguments or {})
    if err:
        return {"ok": False, "tool": name, "error": {"code": "SCHEMA", "message": err}}
    try:
        data = HANDLERS[name](arguments or {})
        return {"ok": True, "tool": name, "data": data}
    except Exception as exc:  # noqa: BLE001 — surface any handler/AWS error as Observation
        return {
            "ok": False,
            "tool": name,
            "error": {"code": "EXEC", "message": str(exc)[:300]},
        }
