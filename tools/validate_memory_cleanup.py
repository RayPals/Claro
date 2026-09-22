#!/usr/bin/env python3
"""Focused regression check for expression-token cleanup under LeakSanitizer."""
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
    with tempfile.TemporaryDirectory(prefix="claro-memory-") as tmp:
        tmp_path = Path(tmp)
        binary = tmp_path / "claro-lsan"
        script = tmp_path / "overwrite.claro"
        script.write_text(
            'TEACH consume first, second, third, fourth\n'
            '    RETURN first\n'
            'END\n'
            'SET value TO "first"\n'
            'SET value TO "second"\n'
            'SET items TO LIST\n'
            'ADD "one" TO items\n'
            'SET items TO LIST\n'
            'SET profile TO MAP\n'
            'PUT profile KEY "name" VALUE "Ada"\n'
            'PUT profile KEY "name" VALUE "Grace"\n'
            + ''.join('DO consume "a", "b", "c", "d"\n' for _ in range(2000))
            + 'SAY profile\n',
            encoding="utf-8",
        )
        build = subprocess.run(
            [
                "gcc", "-std=c99", "-O0", "-g",
                "-fsanitize=address,undefined",
                "src/claro.c", "-o", str(binary), "-lm",
            ], cwd=ROOT, text=True, capture_output=True,
        )
        if build.returncode:
            print(build.stdout, end="")
            print(build.stderr, end="", file=sys.stderr)
            return build.returncode
        run = subprocess.run(
            [str(binary), str(script)], cwd=ROOT, text=True,
            capture_output=True,
            env={**os.environ, "ASAN_OPTIONS": "detect_leaks=1"},
        )
        if "toks_add" in run.stderr or "tokenize" in run.stderr:
            print("FAIL: expression token allocations still leak")
            print(run.stderr, end="", file=sys.stderr)
            return 1
        source = (ROOT / "src" / "claro.c").read_text(encoding="utf-8")
        if "static void split_args_free(char **parts, int count)" not in source:
            print("FAIL: split argument storage has no cleanup boundary")
            return 1
        if "static void value_free(Value v)" not in source or "value_free(v->val);" not in source:
            print("FAIL: overwritten runtime values are not released")
            return 1
        functional = subprocess.run(
            [str(binary), str(script)], cwd=ROOT, text=True,
            capture_output=True,
            env={**os.environ, "ASAN_OPTIONS": "detect_leaks=0"},
        )
        if functional.returncode or "[map]\n" not in functional.stdout:
            print("FAIL: overwrite cleanup probe produced the wrong output")
            print(functional.stdout, end="", file=sys.stderr)
            return 1
        print("PASS: expression token allocations are released")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
