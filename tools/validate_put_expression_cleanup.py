#!/usr/bin/env python3
"""Check that PUT releases evaluated map/key/value copies under LeakSanitizer."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if os.name == "nt":
        print("SKIP: LeakSanitizer check is POSIX-only")
        return 0
    with tempfile.TemporaryDirectory(prefix="claro-put-cleanup-") as tmp:
        tmp_path = Path(tmp)
        binary = tmp_path / "claro-lsan"
        script = tmp_path / "put_expressions.claro"
        script.write_text(
            'SET items TO MAP\n'
            + 'PUT items KEY "key" VALUE "transient" + " value"\n' * 2000,
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
            print("FAIL: PUT expression values still leak")
            print(run.stdout, end="")
            print(run.stderr, end="")
            return 1
        print("PASS: PUT expression values are released")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
