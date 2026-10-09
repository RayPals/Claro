#!/usr/bin/env python3
"""Check that GET ... AT ... releases its evaluated index value."""
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
    with tempfile.TemporaryDirectory(prefix="get-at-cleanup-") as tmp:
        binary = Path(tmp) / "claro-asan"
        build = subprocess.run(
            ["gcc", "-std=c99", "-O0", "-g", "-fsanitize=address,undefined",
             "src/claro.c", "-o", str(binary), "-lm"],
            cwd=ROOT, text=True, capture_output=True,
        )
        if build.returncode:
            print(build.stdout, end="")
            print(build.stderr, end="", file=sys.stderr)
            return build.returncode
        script = Path(tmp) / "get-at.claro"
        script.write_text(
            'SET items TO LIST\n'
            'ADD "hello" TO items\n'
            'DO 2000 TIMES\n'
            'GET items AT "1" AS item\n'
            'END\n'
            'SAY item\n', encoding="utf-8"
        )
        run = subprocess.run(
            [str(binary), str(script)], cwd=ROOT, text=True, capture_output=True,
            env={**os.environ, "ASAN_OPTIONS": "detect_leaks=1"},
        )
        if run.returncode or "LeakSanitizer" in run.stderr or "SUMMARY:" in run.stderr:
            print("FAIL: GET ... AT ... retains expression allocations")
            print(run.stdout, end="")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        if run.stdout != "hello\n":
            print(f"FAIL: unexpected output: {run.stdout!r}")
            return 1
        print("PASS: repeated GET ... AT ... is leak-free and preserves the selected value")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
