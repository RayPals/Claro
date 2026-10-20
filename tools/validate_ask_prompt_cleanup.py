#!/usr/bin/env python3
"""Check ASK prompt expression values are released under LeakSanitizer."""
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
    with tempfile.TemporaryDirectory(prefix="claro-ask-prompt-cleanup-") as tmp:
        tmp_path = Path(tmp)
        binary = tmp_path / "claro-lsan"
        script = tmp_path / "ask_prompts.claro"
        script.write_text(
            ''.join('ASK "question" + " value" AS answer\n' for _ in range(2000)),
            encoding="utf-8",
        )
        build = subprocess.run(
            ["gcc", "-std=c89", "-pedantic-errors", "-Werror=implicit-function-declaration", "-O0", "-g", "-fsanitize=address,undefined",
             "src/claro.c", "-o", str(binary), "-lm"],
            cwd=ROOT, text=True, capture_output=True,
        )
        if build.returncode:
            print(build.stdout, end="")
            print(build.stderr, end="", file=sys.stderr)
            return build.returncode
        run = subprocess.run(
            [str(binary), str(script)], cwd=ROOT, input="\n" * 2000,
            text=True, capture_output=True,
            env={**os.environ, "ASAN_OPTIONS": "detect_leaks=1"},
        )
        if run.returncode:
            print("FAIL: ASK prompt cleanup probe failed")
            print(run.stdout, end="")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        if "LeakSanitizer" in run.stderr or "SUMMARY:" in run.stderr:
            print("FAIL: ASK prompt expression values still leak")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        if run.stdout.count("question value\n") != 2000:
            print("FAIL: ASK prompt cleanup probe produced the wrong output")
            return 1
        print("PASS: ASK prompt expression values are released")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
