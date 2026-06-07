#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / ("claro.exe" if os.name == "nt" else "claro")


def fail(message):
    raise SystemExit(message)


def main():
    if not EXE.exists():
        fail(f"Missing Claro executable: {EXE}")
    result = subprocess.run([str(EXE), "ide"], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        fail(result.stdout)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        fail(f"claro ide did not print valid JSON: {exc}\n{result.stdout}")

    required_top_level = ["language", "version", "file_extensions", "keywords", "types", "commands", "snippets", "diagnostics"]
    for key in required_top_level:
        if key not in data:
            fail(f"Missing top-level IDE metadata field: {key}")

    if ".claro" not in data["file_extensions"]:
        fail("IDE metadata must advertise the .claro file extension")
    if "LIST OF TEXT" not in data["types"]:
        fail("IDE metadata must include typed container types")
    if not any(cmd.get("name") == "typecheck" for cmd in data["commands"]):
        fail("IDE metadata must include the typecheck command")
    if not any(snip.get("name") == "typed_list" for snip in data["snippets"]):
        fail("IDE metadata must include a typed_list snippet")
    if not any(diag.get("source") == "claro typecheck" for diag in data["diagnostics"]):
        fail("IDE metadata must describe claro typecheck diagnostics")

    print("IDE metadata validation OK")


if __name__ == "__main__":
    main()
