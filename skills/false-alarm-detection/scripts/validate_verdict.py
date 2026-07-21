# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Semantic post-validation for false-alarm-detection verdicts.

Enforces invariants that JSON Schema cannot express:
- If matched_pattern is not null, a corresponding .md file must exist
  in the patterns directory

Usage:
    uv run --script validate_verdict.py <verdict-path> <patterns-dir>

Exit codes:
    0  All invariants hold
    1  Semantic validation failed
    2  Usage error (bad arguments, missing file, bad JSON)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "Usage: validate_verdict.py <verdict-path> <patterns-dir>",
            file=sys.stderr,
        )
        return 2

    verdict_path = Path(sys.argv[1])
    patterns_dir = Path(sys.argv[2])

    if not verdict_path.exists():
        print(f"File not found: {verdict_path}", file=sys.stderr)
        return 2

    if not patterns_dir.is_dir():
        print(f"Patterns directory not found: {patterns_dir}", file=sys.stderr)
        return 2

    try:
        data = json.loads(verdict_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"Cannot read verdict: {e}", file=sys.stderr)
        return 2

    if not isinstance(data, dict):
        print("Semantic error: verdict must be a JSON object", file=sys.stderr)
        return 1

    pattern = data.get("matched_pattern")
    if pattern is not None:
        if not isinstance(pattern, str):
            print(
                f"Semantic error: matched_pattern must be a string, got {type(pattern).__name__}",
                file=sys.stderr,
            )
            return 1

        pattern_file = patterns_dir / f"{pattern}.md"
        if not pattern_file.exists():
            available = sorted(p.stem for p in patterns_dir.glob("*.md"))
            print(
                f"Semantic error: matched_pattern '{pattern}' does not correspond "
                f"to a pattern file in {patterns_dir}. "
                f"Available patterns: {', '.join(available) or 'none'}",
                file=sys.stderr,
            )
            return 1

    print("Verdict semantics valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
