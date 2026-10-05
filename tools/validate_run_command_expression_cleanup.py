#!/usr/bin/env python3
"""Regression check for RUN COMMAND expression temporary ownership."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if os.name == "nt":
        print("SKIP: LeakSanitizer check is POSIX-only")
        return 0
    with tempfile.TemporaryDirectory(prefix="claro-run-command-cleanup-") as tmp:
        tmp_path = Path(tmp)
        binary = tmp_path / "claro-lsan"
        script = tmp_path / "run_command_expressions.claro"
        script.write_text('RUN COMMAND "true" AS output\n' * 2000, encoding="utf-8")
        build = subprocess.run(
            ["gcc", "-std=c99", "-O0", "-g", "-fsanitize=address,undefined",
             "src/claro.c", "-o", str(binary), "-lm"],
            cwd=ROOT, text=True, capture_output=True,
        )
        if build.returncode:
            print(build.stdout, end="")
            print(build.stderr, end="")
            return build.returncode
        run = subprocess.run(
            [str(binary), str(script)], cwd=ROOT, text=True, capture_output=True,
            env={**os.environ, "ASAN_OPTIONS": "detect_leaks=1"},
        )
        if run.returncode or "LeakSanitizer" in run.stderr or "SUMMARY:" in run.stderr:
            print("FAIL: RUN COMMAND expression values still leak")
            print(run.stdout, end="")
            print(run.stderr, end="")
            return 1
        print("PASS: RUN COMMAND expression values are released")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())