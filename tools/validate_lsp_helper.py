#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "support" / "lsp" / "claro_lsp_stub.py"
EXE = ROOT / ("claro.exe" if os.name == "nt" else "claro")


def fail(message):
    raise SystemExit(message)


def run_helper(*args):
    result = subprocess.run([sys.executable, str(HELPER), *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        fail(result.stdout)
    return result.stdout


def main():
    if not HELPER.exists():
        fail(f"Missing LSP helper: {HELPER}")
    if not EXE.exists():
        fail(f"Missing Claro executable: {EXE}")

    metadata = json.loads(run_helper("metadata"))
    if metadata.get("language") != "Claro":
        fail("metadata must describe Claro")
    if ".claro" not in metadata.get("file_extensions", []):
        fail("metadata must include .claro")
    if not any(cmd.get("name") == "typecheck" for cmd in metadata.get("commands", [])):
        fail("metadata must include typecheck command")

    completions = json.loads(run_helper("completions"))
    if "SAY" not in completions.get("keywords", []):
        fail("completions must include SAY")
    if "LIST OF TEXT" not in completions.get("types", []):
        fail("completions must include typed containers")

    with tempfile.TemporaryDirectory() as td:
        bad = Path(td) / "bad_lsp.claro"
        bad.write_text("SET score AS NUMBER TO 1\nSET score TO \"oops\"\n", encoding="utf-8")
        diagnostics = json.loads(run_helper("diagnostics", str(bad)))
    if not diagnostics:
        fail("diagnostics must report type errors")
    first = diagnostics[0]
    for key in ["source", "file", "line", "severity", "message"]:
        if key not in first:
            fail(f"diagnostic is missing {key}")
    if first["source"] != "claro typecheck":
        fail("type mismatch should come from claro typecheck")
    if first["line"] != 2:
        fail(f"expected type diagnostic on line 2, got {first['line']}")
    if "NUMBER" not in first["message"] or "TEXT" not in first["message"]:
        fail(f"diagnostic should preserve type mismatch message: {first['message']}")

    print("LSP helper validation OK")


if __name__ == "__main__":
    main()
