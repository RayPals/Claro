#!/usr/bin/env python3
"""Check that READ FILE releases its evaluated path expression."""
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
    with tempfile.TemporaryDirectory(prefix="read-expression-cleanup-", dir=os.environ.get("TMPDIR")) as tmp:
        tmp_path = Path(tmp)
        source = tmp_path / "input.txt"
        source.write_text("hello\n", encoding="utf-8")
        script = tmp_path / "repeated_read.claro"
        quoted = str(source).replace('\\', '\\\\').replace('"', '\\"')
        script.write_text((f'READ FILE "{quoted}" AS contents\n' * 2000) + 'SAY contents\n', encoding="utf-8")
        binary = tmp_path / "claro-asan"
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
            [str(binary), str(script)], cwd=ROOT, text=True, capture_output=True,
            env={**os.environ, "ASAN_OPTIONS": "detect_leaks=1"},
        )
        if run.returncode or "LeakSanitizer" in run.stderr or "SUMMARY:" in run.stderr:
            print("FAIL: repeated READ FILE expressions retain allocations")
            print(run.stdout, end="")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        if run.stdout != "hello\n\n":
            print(f"FAIL: unexpected READ FILE output: {run.stdout!r}")
            return 1
        print("PASS: repeated READ FILE expressions release temporary values")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
