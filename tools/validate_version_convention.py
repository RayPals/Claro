#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "claro.exe"
EXPECTED = "Claro v1.18.26"


def fail(message):
    raise SystemExit(message)


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def main():
    if not EXE.exists():
        fail(f"Missing executable: {EXE}")
    out = run([str(EXE), "--version"]).stdout.strip()
    if out != EXPECTED:
        fail(f"Expected version {EXPECTED!r}, got {out!r}")
    ide = run([str(EXE), "ide"])
    if ide.returncode != 0:
        fail(ide.stdout)
    metadata = json.loads(ide.stdout)
    if metadata.get("version") != "v1.18.26":
        fail(f"Expected IDE metadata version 'v1.18.26', got {metadata.get('version')!r}")
    validator = ROOT / "tools" / "validate_v1_17.py"
    text = validator.read_text(encoding="utf-8")
    if "Claro v1.18.26" not in text:
        fail("tools/validate_v1_17.py must validate Claro v1.18.26")
    print("Version convention validation OK")


if __name__ == "__main__":
    main()
