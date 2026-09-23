#!/usr/bin/env python3
"""Regression check for control-flow expression Value cleanup under LeakSanitizer."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if os.name == "nt":
        print("SKIP: LeakSanitizer check is POSIX-only")
        return 0
    with tempfile.TemporaryDirectory(prefix="claro-control-flow-cleanup-") as tmp:
        tmp_path = Path(tmp)
        binary = tmp_path / "claro-lsan"
        script = tmp_path / "control_flow.claro"
        script.write_text(
            'SET items TO LIST\n'
            'FOR EACH item IN items\n'
            '    SAY item\n'
            'DONE\n',
            encoding="utf-8",
        )
        build = subprocess.run(
            [
                "gcc", "-std=c99", "-O0", "-g",
                "-fsanitize=address,undefined",
                "src/claro.c", "-o", str(binary), "-lm",
            ], cwd=ROOT, text=True, capture_output=True,
        )
        if build.returncode:
            print(build.stdout, end="")
            print(build.stderr, end="", file=sys.stderr)
            return build.returncode
        run = subprocess.run(
            [str(binary), str(script)], cwd=ROOT, text=True,
            capture_output=True,
            env={**os.environ, "ASAN_OPTIONS": "detect_leaks=1"},
        )
        if run.returncode:
            print("FAIL: control-flow cleanup probe failed")
            print(run.stdout, end="")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        if "LeakSanitizer" in run.stderr or "SUMMARY:" in run.stderr:
            print("FAIL: control-flow expression values still leak")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        if run.stdout != "":
            print("FAIL: control-flow cleanup probe produced the wrong output")
            print(run.stdout, end="", file=sys.stderr)
            return 1
        print("PASS: control-flow expression values are released")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
