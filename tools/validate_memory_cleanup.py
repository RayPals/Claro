#!/usr/bin/env python3
"""Focused regression check for expression-token cleanup under LeakSanitizer."""
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
    with tempfile.TemporaryDirectory(prefix="claro-memory-") as tmp:
        tmp_path = Path(tmp)
        binary = tmp_path / "claro-lsan"
        script = tmp_path / "overwrite.claro"
        script.write_text(
            'SET value TO "first"\n'
            'SET value TO "second"\n'
            'SAY value\n',
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
        if "toks_add" in run.stderr or "tokenize" in run.stderr:
            print("FAIL: expression token allocations still leak")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        functional = subprocess.run(
            [str(binary), str(script)], cwd=ROOT, text=True,
            capture_output=True,
            env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0"},
        )
        if functional.returncode or "second\n" not in functional.stdout:
            print("FAIL: overwrite cleanup probe produced the wrong output")
            print(functional.stdout, end="", file=sys.stderr)
            return 1
        print("PASS: expression token allocations are released")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
