#!/usr/bin/env python3
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import urllib.request


DEFAULT_OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
DEFAULT_MODEL = "llama3.2:latest"
PERSONAS = {
    "systems_engineer": (
        "You are a ruthless HFT systems engineer. Review only latency, I/O, "
        "race conditions, fail-closed behavior, process safety, and operational complexity."
    ),
    "ml_architect": (
        "You are a ruthless ML architect. Review only overfitting, leakage, "
        "bad validation, hallucination risk, weak sample size, and feature brittleness."
    ),
}


def main() -> int:
    args = parse_args()
    proposal = read_proposal(args.proposal)
    result = run_tier0_review(
        proposal,
        personas=PERSONAS,
        url=args.ollama_url,
        model=args.model,
        timeout=args.timeout,
    )
    output = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a Tier 0 local Ollama red-team precheck.")
    parser.add_argument("proposal", nargs="?", type=Path, help="Proposal markdown/text file. Reads stdin if omitted.")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--timeout", type=float, default=30.0)
    return parser.parse_args()


def read_proposal(path: Path | None) -> str:
    if path is None:
        text = sys.stdin.read()
    else:
        text = path.read_text(encoding="utf-8")
    text = text.strip()
    if not text:
        raise ValueError("proposal is empty")
    return text


def run_tier0_review(
    proposal: str,
    *,
    personas: dict[str, str],
    url: str,
    model: str,
    timeout: float,
) -> dict:
    started_at = datetime.now(timezone.utc).isoformat()
    reviews: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=len(personas)) as executor:
        futures = {
            executor.submit(
                review_with_persona,
                name,
                instructions,
                proposal,
                url=url,
                model=model,
                timeout=timeout,
            ): name
            for name, instructions in personas.items()
        }
        for future in as_completed(futures):
            name = futures[future]
            try:
                reviews[name] = future.result()
            except Exception as exc:
                reviews[name] = failure_review(name, f"{type(exc).__name__}: {exc}")

    escalation_required = any(review.get("escalation_required", True) for review in reviews.values())
    verdict = "ESCALATE" if escalation_required else aggregate_verdict(reviews)
    return {
        "mode": "Tier 0 Advisory Pre-Check",
        "started_at": started_at,
        "model": model,
        "verdict": verdict,
        "escalation_required": escalation_required,
        "reviews": reviews,
    }


def review_with_persona(
    name: str,
    instructions: str,
    proposal: str,
    *,
    url: str,
    model: str,
    timeout: float,
) -> dict:
    prompt = (
        f"{instructions}\n\n"
        "Return strict JSON only with this schema:\n"
        "{\n"
        '  "persona": "<name>",\n'
        '  "verdict": "PASS" or "REJECT",\n'
        '  "blockers": ["short blocker strings"],\n'
        '  "risks": ["short risk strings"],\n'
        '  "escalation_required": true or false\n'
        "}\n"
        "Rules: If any uncertainty could affect live trading, set escalation_required=true.\n\n"
        f"PERSONA_NAME: {name}\n"
        f"PROPOSAL:\n{proposal}"
    )
    request = urllib.request.Request(
        url,
        data=json.dumps(
            {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0,
                "response_format": {"type": "json_object"},
            }
        ).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer ollama"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read())
    content = str(payload["choices"][0]["message"]["content"]).strip()
    return validate_review(name, json.loads(content))


def validate_review(name: str, review: dict) -> dict:
    verdict = str(review.get("verdict", "")).upper()
    if verdict not in {"PASS", "REJECT"}:
        return failure_review(name, f"invalid verdict: {verdict}")
    blockers = normalize_list(review.get("blockers"))
    risks = normalize_list(review.get("risks"))
    escalation_required = bool(review.get("escalation_required", verdict == "REJECT"))
    return {
        "persona": name,
        "verdict": verdict,
        "blockers": blockers,
        "risks": risks,
        "escalation_required": escalation_required,
    }


def normalize_list(value: object) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        return [str(value)[:500]]
    return [str(item)[:500] for item in value]


def failure_review(name: str, reason: str) -> dict:
    return {
        "persona": name,
        "verdict": "REJECT",
        "blockers": [reason],
        "risks": ["local red-team output invalid or unavailable"],
        "escalation_required": True,
    }


def aggregate_verdict(reviews: dict[str, dict]) -> str:
    if any(review.get("verdict") == "REJECT" for review in reviews.values()):
        return "REJECT"
    return "PASS"


if __name__ == "__main__":
    raise SystemExit(main())
