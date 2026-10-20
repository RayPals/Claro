#!/usr/bin/env python3
"""Check OBJECT CLASS/FIELDS release evaluated values under sanitizers."""
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
    with tempfile.TemporaryDirectory(prefix="object-expression-cleanup-") as tmp:
        binary = Path(tmp) / "claro-asan"
        build = subprocess.run(
            ["gcc", "-std=c89", "-pedantic-errors", "-Werror=implicit-function-declaration", "-O0", "-g", "-fsanitize=address,undefined",
             "src/claro.c", "-o", str(binary), "-lm"],
            cwd=ROOT, text=True, capture_output=True,
        )
        if build.returncode:
            print(build.stdout, end="")
            print(build.stderr, end="", file=sys.stderr)
            return build.returncode
        script = Path(tmp) / "object-expressions.claro"
        script.write_text(
            "CLASS Person\nHAS name TEXT\nEND\nNEW Person person\n"
            "DO 2000 TIMES\nOBJECT CLASS person AS kind\nOBJECT FIELDS person AS fields\nEND\n"
            "SAY kind\nCOUNT fields AS count\nGET fields AT 1 AS first\nSAY count\nSAY first\n", encoding="utf-8"
        )
        run = subprocess.run(
            [str(binary), str(script)], cwd=ROOT, text=True, capture_output=True,
            env={**os.environ, "ASAN_OPTIONS": "detect_leaks=1"},
        )
        if run.returncode or "LeakSanitizer" in run.stderr or "SUMMARY:" in run.stderr:
            print("FAIL: repeated OBJECT CLASS/FIELDS retains expression allocations")
            print(run.stdout, end="")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        if run.stdout != "Person\n1\nname\n":
            print(f"FAIL: unexpected output: {run.stdout!r}")
            return 1
        print("PASS: repeated OBJECT CLASS/FIELDS is leak-free and preserves results")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
