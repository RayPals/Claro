#!/usr/bin/env python3
"""Check WRITE FILE releases evaluated path and content values."""
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
    with tempfile.TemporaryDirectory(prefix="write-expression-cleanup-", dir=os.environ.get("TMPDIR")) as tmp:
        tmp_path = Path(tmp)
        target = tmp_path / "output.txt"
        script = tmp_path / "repeated_write.claro"
        path = str(target).replace('\\', '\\\\').replace('"', '\\"')
        script.write_text((f'WRITE FILE "{path}" WITH "hello"\n' * 2000), encoding="utf-8")
        binary = tmp_path / "claro-asan"
        build = subprocess.run(
            ["gcc", "-std=c99", "-O0", "-g", "-fsanitize=address,undefined", "src/claro.c", "-o", str(binary), "-lm"],
            cwd=ROOT, text=True, capture_output=True,
        )
        if build.returncode:
            print(build.stdout, end="")
            print(build.stderr, end="", file=sys.stderr)
            return build.returncode
        run = subprocess.run([str(binary), str(script)], cwd=ROOT, text=True, capture_output=True,
                             env={**os.environ, "ASAN_OPTIONS": "detect_leaks=1"})
        if run.returncode or "LeakSanitizer" in run.stderr or "SUMMARY:" in run.stderr:
            print("FAIL: repeated WRITE FILE expressions retain allocations")
            print(run.stdout, end="")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        if target.read_text(encoding="utf-8") != "hello":
            print("FAIL: WRITE FILE output changed")
            return 1
        print("PASS: repeated WRITE FILE expressions release temporary values")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
