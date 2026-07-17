# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Semantic post-validation for failure-matching verdicts.

Enforces invariants that JSON Schema cannot express:
- If ticket_id is not null, it must look like a Jira ticket ID

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

    ticket_id = data.get("ticket_id")
    if ticket_id is not None and not re.match(r"^[A-Z][A-Z0-9]+-\d+$", ticket_id):
        print(
            f"Semantic error: ticket_id '{ticket_id}' does not match "
            "Jira ticket pattern (e.g. AIPCC-123)",
            file=sys.stderr,
        )
        return 1

    print("Verdict semantics valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
