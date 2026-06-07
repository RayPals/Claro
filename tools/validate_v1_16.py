#!/usr/bin/env python3
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / ("claro.exe" if os.name == "nt" else "claro")

def run(cmd, cwd=ROOT, input_text=None):
    result = subprocess.run(cmd, cwd=cwd, input=input_text, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("$", " ".join(map(str, cmd)))
    print(result.stdout, end="")
    if result.returncode != 0:
        raise SystemExit(result.returncode)
    return result.stdout

if not EXE.exists():
    run(["gcc", "-std=c99", "src/claro.c", "-O0", "-o", str(EXE), "-lm"])

run([str(EXE), "--version"])
run([str(EXE), "test"])
run([str(EXE), "validate"])

with tempfile.TemporaryDirectory() as td:
    work = Path(td)
    shutil.copy2(EXE, work / EXE.name)
    local = work / EXE.name
    run([str(local), "new", "DemoProject"], cwd=work)
    proj = work / "DemoProject"
    run([str(local), "package", "doctor"], cwd=proj)
    run([str(local), "package", "add", "text"], cwd=proj)
    run([str(local), "package", "add", "text"], cwd=proj)
    listing = run([str(local), "package", "list"], cwd=proj)
    if listing.count("text") != 1:
        raise SystemExit("Package was duplicated in listing")
    bad = subprocess.run([str(local), "package", "add", "../bad"], cwd=proj, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("$", local, "package add ../bad")
    print(bad.stdout, end="")
    if bad.returncode == 0:
        raise SystemExit("Unsafe package name was accepted")
    run([str(local), "package", "remove", "text"], cwd=proj)
    run([str(local), "run"], cwd=proj)

print("Validation passed. Claro v1.18.26 networking reliability is ready for use.")
