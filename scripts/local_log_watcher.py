#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import urllib.request


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOG = PROJECT_ROOT / "outputs" / "challenger_runner.log"
DEFAULT_OUTPUT = PROJECT_ROOT / "AA_Research" / "ollama_log_summary.txt"
DEFAULT_OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
DEFAULT_MODEL = "llama3.2:latest"
TAIL_BYTES = 64_000
MAX_FILTERED_LINES = 220
NOISE_PATTERNS = (
    re.compile(r"NotOpenSSLWarning"),
    re.compile(r"urllib3 v2 only supports OpenSSL"),
    re.compile(r"warnings\.warn"),
    re.compile(r"^\s*$"),
)
IMPORTANT_PATTERNS = (
    re.compile(r"\b(ERROR|Error|Exception|Traceback|FAILED|failed|sqlite|OperationalError|HTTPError|Unauthorized|ConnectionError)\b"),
    re.compile(r"\bheartbeat|last_cycle_status|started|stopped|STOPPED|OK\b", re.IGNORECASE),
)


def main() -> int:
    args = parse_args()
    timestamp = datetime.now(timezone.utc).isoformat()
    try:
        raw_tail = read_byte_tail(args.log_path, args.tail_bytes)
        filtered = prefilter_log(raw_tail)
        if not filtered:
            line = strict_line(timestamp, "LOCAL_SUMMARY_FAILED", "no filtered log lines", "inspect raw log")
        else:
            summary = summarize_with_ollama(
                filtered,
                url=args.ollama_url,
                model=args.model,
                timeout=args.timeout,
            )
            line = normalize_summary(timestamp, summary)
    except Exception as exc:
        line = strict_line(timestamp, "LOCAL_SUMMARY_FAILED", f"{type(exc).__name__}: {exc}", "inspect raw log")

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    print(line)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize Ari runner logs with local Ollama.")
    parser.add_argument("--log-path", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--tail-bytes", type=int, default=TAIL_BYTES)
    return parser.parse_args()


def read_byte_tail(path: Path, byte_count: int) -> str:
    if byte_count <= 0:
        raise ValueError("byte_count must be positive")
    with path.open("rb") as handle:
        handle.seek(0, 2)
        size = handle.tell()
        handle.seek(max(0, size - byte_count))
        data = handle.read(byte_count)
    return data.decode("utf-8", errors="replace")


def prefilter_log(text: str) -> str:
    unique_lines: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        stripped = line.strip()
        if any(pattern.search(stripped) for pattern in NOISE_PATTERNS):
            continue
        if stripped in seen:
            continue
        seen.add(stripped)
        unique_lines.append(stripped)

    important = [line for line in unique_lines if any(pattern.search(line) for pattern in IMPORTANT_PATTERNS)]
    selected = important if important else unique_lines
    return "\n".join(selected[-MAX_FILTERED_LINES:])


def summarize_with_ollama(log_text: str, *, url: str, model: str, timeout: float) -> str:
    prompt = (
        "You are Theo Park, Ari systems reliability analyst. "
        "Summarize the following runner log into exactly one pipe-delimited line.\n"
        "Schema: status | issue | next_action\n"
        "Allowed status values: GREEN, AMBER, RED\n"
        "No markdown. No extra text.\n\n"
        f"LOG:\n{log_text}"
    )
    request = urllib.request.Request(
        url,
        data=json.dumps(
            {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0,
            }
        ).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer ollama"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read())
    return str(payload["choices"][0]["message"]["content"]).strip()


def normalize_summary(timestamp: str, summary: str) -> str:
    parts = [part.strip() for part in summary.replace("\n", " ").split("|")]
    if len(parts) != 3:
        return strict_line(timestamp, "LOCAL_SUMMARY_FAILED", "invalid summary schema", "inspect raw log")
    status, issue, next_action = parts
    if status not in {"GREEN", "AMBER", "RED"}:
        return strict_line(timestamp, "LOCAL_SUMMARY_FAILED", f"invalid status: {status}", "inspect raw log")
    return strict_line(timestamp, status, issue or "none", next_action or "none")


def strict_line(timestamp: str, status: str, issue: str, next_action: str) -> str:
    return " | ".join(
        [
            timestamp,
            sanitize_field(status),
            sanitize_field(issue),
            sanitize_field(next_action),
        ]
    )


def sanitize_field(value: str) -> str:
    return re.sub(r"\s+", " ", str(value).replace("|", "/")).strip()[:500]


if __name__ == "__main__":
    raise SystemExit(main())
