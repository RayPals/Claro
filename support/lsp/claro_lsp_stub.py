#!/usr/bin/env python3
"""Small Claro editor/LSP helper.

This is not a full JSON-RPC Language Server yet. It is a stable helper that
editor plugins can call to get metadata, completions, and diagnostics without
re-implementing Claro parsing.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXE = ROOT / ("claro.exe" if os.name == "nt" else "claro")

KEYWORDS = [
    "SAY", "ASK", "SET", "IF", "ELSE", "ENDIF", "END", "REPEAT", "UNTIL",
    "TEACH", "LEARNED", "DO", "RETURN", "CLASS", "HAS", "NEW", "IMPORT",
    "TRY", "CATCH", "ENDTRY", "START TASK", "WAIT TASK", "HTTP CHECK",
    "HTTP GET", "HTTP SAVE", "OPEN WINDOW", "CLEAR SCREEN", "DRAW TEXT",
    "UPDATE SCREEN", "CLOSE WINDOW", "TYPE OF", "CHECK TYPE",
]
TYPES = [
    "NUMBER", "TEXT", "YESNO", "LIST", "LIST OF TEXT", "LIST OF NUMBER",
    "LIST OF YESNO", "MAP", "MAP OF TEXT", "MAP OF NUMBER", "MAP OF YESNO",
    "OBJECT", "ANY",
]
COMMANDS = [
    {"name": "check", "usage": "claro check file.claro"},
    {"name": "typecheck", "usage": "claro typecheck file.claro"},
    {"name": "fmt", "usage": "claro fmt file.claro"},
]

DIAG_RE = re.compile(r"^(?P<file>.*?):(?P<line>\d+):\s*(?P<message>.*)$")


def print_json(value: object) -> int:
    print(json.dumps(value, indent=2))
    return 0


def metadata() -> dict:
    return {
        "language": "Claro",
        "version": "v1.18.26",
        "file_extensions": [".claro"],
        "keywords": KEYWORDS,
        "types": TYPES,
        "commands": COMMANDS,
    }


def completions() -> dict:
    return {"keywords": KEYWORDS, "types": TYPES}


def parse_diagnostics(output: str, source: str) -> list[dict]:
    diagnostics = []
    for raw in output.splitlines():
        line = raw.strip()
        if not line or line == "OK" or line == "Type check OK":
            continue
        match = DIAG_RE.match(line)
        if not match:
            continue
        diagnostics.append(
            {
                "source": source,
                "file": match.group("file").replace("\\", "/"),
                "line": int(match.group("line")),
                "severity": "error",
                "message": match.group("message"),
            }
        )
    return diagnostics


def run_claro_command(command: str, path: str) -> list[dict]:
    result = subprocess.run(
        [str(EXE), command, path],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return parse_diagnostics(result.stdout, f"claro {command}")


def diagnostics(path: str) -> list[dict]:
    found = []
    found.extend(run_claro_command("check", path))
    found.extend(run_claro_command("typecheck", path))
    return found


def usage() -> int:
    print("Usage:")
    print("  claro_lsp_stub.py metadata")
    print("  claro_lsp_stub.py completions")
    print("  claro_lsp_stub.py diagnostics file.claro")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return usage()
    cmd = argv[1]
    if cmd == "metadata":
        return print_json(metadata())
    if cmd == "completions":
        return print_json(completions())
    if cmd == "diagnostics" and len(argv) >= 3:
        return print_json(diagnostics(argv[2]))
    return usage()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
