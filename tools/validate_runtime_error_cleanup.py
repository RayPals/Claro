#!/usr/bin/env python3
"""Check that caught runtime diagnostics release their owned message values."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
CASES = {
    "tests/38_builtin_arity.claro": "math.abs needs 1 argument",
    "tests/39_random_inverted_range.claro": "random.int needs the lower bound",
}


def main() -> int:
    if os.name == "nt":
        print("SKIP: LeakSanitizer check is POSIX-only")
        return 0
    with tempfile.TemporaryDirectory(prefix="runtime-error-cleanup-") as tmp:
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
        for script, expected in CASES.items():
            run = subprocess.run(
                [str(binary), script], cwd=ROOT, text=True, capture_output=True,
                env={**os.environ, "ASAN_OPTIONS": "detect_leaks=1"},
            )
            if run.returncode or "LeakSanitizer" in run.stderr or "SUMMARY:" in run.stderr:
                print(f"FAIL: caught diagnostics in {script} retain allocations")
                print(run.stdout, end="")
                print(run.stderr, end="", file=sys.stderr)
                return 1
            if expected not in run.stdout:
                print(f"FAIL: expected diagnostic was not printed for {script}")
                print(run.stdout, end="")
                return 1
        print("PASS: caught builtin-arity and inverted-range diagnostics are leak-free")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
