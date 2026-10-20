#!/usr/bin/env python3
"""Regression check for LIST FOLDER expression temporary ownership."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    if os.name == "nt":
        print("SKIP: LeakSanitizer check is POSIX-only")
        return 0
    with tempfile.TemporaryDirectory(prefix="claro-list-folder-cleanup-") as tmp:
        tmp_path = Path(tmp)
        binary = tmp_path / "claro-lsan"
        script = tmp_path / "list_folder_expressions.claro"
        folder = tmp_path / "folder"
        folder.mkdir()
        script.write_text(
            'SET path TO "' + str(folder) + '"\n'
            + "LIST FOLDER path AS entries\n" * 2000,
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
            print("FAIL: LIST FOLDER expression values still leak")
            print(run.stdout, end="")
            print(run.stderr, end="")
            return 1
        print("PASS: LIST FOLDER expression values are released")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
