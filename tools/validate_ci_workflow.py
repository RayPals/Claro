#!/usr/bin/env python3
"""Validate that CI runs Claro's current release gates, not only legacy smoke tests."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".forgejo" / "workflows" / "ci.yml"

REQUIRED_COMMANDS = [
    "./claro validate",
    "python3 tools/validate_typecheck_diagnostics.py",
    "python3 tools/validate_version_convention.py",
    "python3 tools/validate_package_security.py",
]


def main() -> int:
    if not WORKFLOW.exists():
        print(f"Missing CI workflow: {WORKFLOW.relative_to(ROOT)}")
        return 1

    text = WORKFLOW.read_text(encoding="utf-8")
    missing = [command for command in REQUIRED_COMMANDS if command not in text]
    if missing:
        print("CI workflow is missing current release validation commands:")
        for command in missing:
            print(f"  - {command}")
        print("Add them to .forgejo/workflows/ci.yml so regressions are caught before release.")
        return 1

    print("CI workflow validation complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
