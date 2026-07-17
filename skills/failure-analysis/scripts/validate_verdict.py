# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Semantic post-validation for failure-analysis verdicts.

Enforces invariants that JSON Schema cannot express:
- root_cause_snippet should contain line-number citations (L<num>:)
- summary should not be identical to likely_cause

Usage:
    uv run --script validate_verdict.py <verdict-path>

Exit codes:
    0  All invariants hold
    1  Semantic validation failed
    2  Usage error (bad arguments, missing file, bad JSON)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_verdict.py <verdict-path>", file=sys.stderr)
        return 2

    verdict_path = Path(sys.argv[1])
    if not verdict_path.exists():
        print(f"File not found: {verdict_path}", file=sys.stderr)
        return 2

    try:
        data = json.loads(verdict_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"Cannot read verdict: {e}", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print("Validation failed: verdict must be a JSON object", file=sys.stderr)
        return 1

    errors = []

    snippet = data.get("root_cause_snippet", "")
    if isinstance(snippet, str) and snippet:
        lines = [line.strip() for line in snippet.splitlines() if line.strip()]
        if not all(re.match(r"L\d+:", line) for line in lines):
            errors.append(
                "every non-empty line in root_cause_snippet should start "
                "with a line-number citation in 'L<num>:' format"
            )

    summary = data.get("summary", "")
    cause = data.get("likely_cause", "")
    if (
        isinstance(summary, str)
        and isinstance(cause, str)
        and summary
        and cause
        and summary.strip() == cause.strip()
    ):
        errors.append("summary should not be identical to likely_cause")

    if errors:
        for err in errors:
            print(f"Validation failed: {err}", file=sys.stderr)
        return 1

    print("Verdict semantics valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
