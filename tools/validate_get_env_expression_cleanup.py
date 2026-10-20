#!/usr/bin/env python3
"""Regression check for GET ENV expression temporary cleanup."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if os.name == "nt":
        print("SKIP: LeakSanitizer check is POSIX-only")
        return 0
    with tempfile.TemporaryDirectory(prefix="claro-get-env-cleanup-") as tmp:
        tmp_path = Path(tmp)
        binary = tmp_path / "claro-lsan"
        script = tmp_path / "get_env_expressions.claro"
        script.write_text(
            'GET ENV "PATH" AS path\n' * 2000 + "SAY path\n",
            encoding="utf-8",
        )
        build = subprocess.run(
            ["gcc", "-std=c89", "-pedantic-errors", "-Werror=implicit-function-declaration", "-O0", "-g", "-fsanitize=address,undefined",
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
            print("FAIL: GET ENV expression values still leak")
            print(run.stdout, end="")
            print(run.stderr, end="")
            return 1
        if not run.stdout.endswith("\n") or len(run.stdout.splitlines()) != 1:
            print("FAIL: GET ENV probe did not produce one output line")
            return 1
        print("PASS: GET ENV expression values are released")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
