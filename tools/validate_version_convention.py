#!/usr/bin/env python3
import json
import re
from datetime import datetime
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "claro.exe"
EXPECTED = "Claro v2026.10.20.160950"


def fail(message):
    raise SystemExit(message)


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def main():
    if not EXE.exists():
        fail(f"Missing executable: {EXE}")
    out = run([str(EXE), "--version"]).stdout.strip()
    if not re.fullmatch(r"Claro v\d{4}\.\d{2}\.\d{2}\.\d{6}", out):
        fail(f"Expected UTC run timestamp Claro vYYYY.MM.DD.HHMMSS, got {out!r}")
    datetime.strptime(out.removeprefix("Claro v"), "%Y.%m.%d.%H%M%S")
    if out != EXPECTED:
        fail(f"Expected version {EXPECTED!r}, got {out!r}")
    ide = run([str(EXE), "ide"])
    if ide.returncode != 0:
        fail(ide.stdout)
    metadata = json.loads(ide.stdout)
    if metadata.get("version") != "v2026.10.20.160950":
        fail(f"Expected IDE metadata version 'v2026.10.20.160950', got {metadata.get('version')!r}")
    validator = ROOT / "tools" / "validate_v1_17.py"
    text = validator.read_text(encoding="utf-8")
    if "Claro v2026.10.20.160950" not in text:
        fail("tools/validate_v1_17.py must validate Claro v2026.10.20.160950")
    print("Version convention validation OK")


if __name__ == "__main__":
    main()
