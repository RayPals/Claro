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
    "python3 tools/validate_compiler_warnings.py",
    "python3 tools/validate_ci_workflow.py",
]


def _run_step_text(workflow_text: str) -> str:
    """Return commands from YAML-like ``run`` steps, excluding comments/names."""
    commands = []
    in_run = False
    run_indent = -1
    for raw_line in workflow_text.splitlines():
        stripped = raw_line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(stripped)
        if stripped.startswith("run:"):
            in_run = True
            run_indent = indent
            commands.append(stripped[4:].strip())
            continue
        if in_run:
            if indent <= run_indent and stripped.startswith("-"):
                in_run = False
            elif indent <= run_indent and ":" in stripped:
                in_run = False
            else:
                commands.append(stripped)
    return "\n".join(commands)


def missing_release_gates(workflow_text: str):
    run_text = _run_step_text(workflow_text)
    return [command for command in REQUIRED_COMMANDS if command not in run_text]


def main() -> int:
    if not WORKFLOW.exists():
        print(f"Missing CI workflow: {WORKFLOW.relative_to(ROOT)}")
        return 1

    text = WORKFLOW.read_text(encoding="utf-8")
    missing = missing_release_gates(text)
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
