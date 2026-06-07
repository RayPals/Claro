#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
exe = root / ("claro.exe" if sys.platform.startswith("win") else "claro")

def run(args, expect=0, input_text=None):
    p = subprocess.run(args, cwd=root, input=input_text, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != expect:
        print("FAILED:", " ".join(map(str,args)))
        print(p.stdout)
        print(p.stderr)
        sys.exit(1)
    return p.stdout + p.stderr

run([str(exe), "--version"])
run([str(exe), "test"])
run([str(exe), "check", "lessons/01_hello.claro"])
run([str(exe), "check", "lessons/08_functions.claro"])
run([str(exe), "check", "tests/checker_fixtures/bad_unknown_command.claro"], expect=1)
run([str(exe), "check", "tests/checker_fixtures/bad_typo_command.claro"], expect=1)
print("RC3 validation passed")
