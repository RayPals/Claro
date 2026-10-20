#!/usr/bin/env python3
"""Check that typecheck releases its temporary type environment."""
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
    with tempfile.TemporaryDirectory(prefix="typecheck-env-cleanup-") as tmp:
        tmp_path = Path(tmp)
        binary = tmp_path / "claro-lsan"
        script = tmp_path / "typecheck.claro"
        script.write_text("SET known TO 1\n" + "SAY known\n" * 2000, encoding="utf-8")
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
            [str(binary), "typecheck", str(script)], cwd=ROOT, text=True,
            capture_output=True, env={**os.environ, "ASAN_OPTIONS": "detect_leaks=1"},
        )
        if run.returncode:
            print("FAIL: typecheck temporary-state cleanup probe failed")
            print(run.stdout, end="")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        if "LeakSanitizer" in run.stderr or "SUMMARY:" in run.stderr:
            print("FAIL: typecheck environment allocations still leak")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        print("PASS: typecheck environment allocations are released")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
