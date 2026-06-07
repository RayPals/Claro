#!/usr/bin/env python3
"""Validate Claro v1.10.26 from the package root."""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / ("claro.exe" if os.name == "nt" else "claro")


def run(cmd):
    print("+", " ".join(str(c) for c in cmd))
    return subprocess.run(cmd, cwd=ROOT).returncode


def main():
    if run(["gcc", "-std=c99", "src/claro.c", "-O0", "-o", str(EXE), "-lm"]):
        return 1
    checks = [
        [str(EXE), "--version"],
        [str(EXE), "test"],
        [str(EXE), "doctor"],
        [str(EXE), "validate"],
        [str(EXE), "examples/simple_functions.claro"],
        [str(EXE), "examples/text_polish.claro"],
        [str(EXE), "examples/types_and_objects.claro"],
        [str(EXE), "examples/tasks_and_graphics.claro"],
    ]
    for cmd in checks:
        if run(cmd):
            return 1
    print("Claro v1.10.26 validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
