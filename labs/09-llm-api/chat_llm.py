#!/usr/bin/env python3
"""Minimal OpenAI-compatible chat — Ollama (local) or OpenRouter (cloud)."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parent


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def client_for(backend: str) -> tuple[OpenAI, str]:
    if backend == "ollama":
        base = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        model = os.environ.get("OLLAMA_MODEL", "qwen3.5:4b")
        key = os.environ.get("OLLAMA_API_KEY", "ollama")
        return OpenAI(base_url=base, api_key=key), model
    if backend == "openrouter":
        key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        if not key:
            raise SystemExit("OPENROUTER_API_KEY missing — set in .env or export")
        base = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        model = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4.1-nano")
        return OpenAI(base_url=base, api_key=key), model
    raise SystemExit("backend must be ollama|openrouter")


def main() -> None:
    load_dotenv(ROOT / ".env")
    p = argparse.ArgumentParser()
    p.add_argument("--backend", choices=("ollama", "openrouter"), required=True)
    p.add_argument("--message", default="Hi — who are you? Answer in one short sentence.")
    p.add_argument("--system", default=None, help="optional system role")
    args = p.parse_args()

    client, model = client_for(args.backend)
    messages = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": args.message})

    print(f"backend={args.backend} model={model}")
    resp = client.chat.completions.create(model=model, messages=messages)
    print(resp.choices[0].message.content)


if __name__ == "__main__":
    main()
