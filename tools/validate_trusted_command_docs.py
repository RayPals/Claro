#!/usr/bin/env python3
"""Ensure the learner-facing RUN COMMAND docs describe its trust boundary."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "PRACTICAL_SCRIPTING.md"


def main() -> int:
    text = DOC.read_text(encoding="utf-8").lower()
    required = (
        "trusted code",
        "not a sandbox",
        "runs commands on the user's computer",
    )
    missing = [phrase for phrase in required if phrase not in text]
    if missing:
        raise SystemExit("RUN COMMAND documentation is missing: " + ", ".join(missing))
    print("Trusted command documentation validation complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
