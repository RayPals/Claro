#!/usr/bin/env python3
"""Regression check for EXISTS FILE expression temporary ownership."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if os.name == "nt":
        print("SKIP: LeakSanitizer check is POSIX-only")
        return 0
    with tempfile.TemporaryDirectory(prefix="claro-exists-cleanup-") as tmp:
        tmp_path = Path(tmp)
        binary = tmp_path / "claro-lsan"
        script = tmp_path / "exists_expressions.claro"
        script.write_text(
            'SET path TO "missing-file-for-cleanup-probe"\n'
            + 'EXISTS FILE path AS present\n' * 2000
            + "SAY present\n",
            encoding="utf-8",
        )
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
            print("FAIL: EXISTS FILE expression values still leak")
            print(run.stdout, end="")
            print(run.stderr, end="")
            return 1
        if run.stdout != "NO\n":
            print(f"FAIL: unexpected EXISTS FILE probe output: {run.stdout!r}")
            return 1
        print("PASS: EXISTS FILE expression values are released")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())