#!/usr/bin/env python3
"""Claro formatter (simple, deterministic)."""
import sys, pathlib

OPEN = {"IF", "DO", "REPEAT", "TEACH", "TRY"}
MID  = {"ELSE", "CATCH"}
CLOSE= {"ENDIF", "DONE", "UNTIL", "LEARNED", "ENDTRY"}

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/fmt.py <file.claro>")
        return 2
    p = pathlib.Path(sys.argv[1])
    lines = p.read_text(encoding="utf-8").splitlines()
    out = []
    indent = 0
    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            out.append("")
            continue
        head = stripped.split()[0].upper()
        if head in CLOSE:
            indent = max(0, indent-1)
        if head in MID:
            indent = max(0, indent-1)
        out.append(("    "*indent) + stripped)
        if head in OPEN:
            indent += 1
        if head in MID:
            indent += 1
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
