#!/usr/bin/env python3
"""Claro checker/linter (gentle)."""
import sys, pathlib

OPEN = {"IF":"ENDIF", "DO":"DONE", "REPEAT":"UNTIL", "TEACH":"LEARNED", "TRY":"ENDTRY"}
KNOWN = set(list(OPEN.keys()) + list(OPEN.values()) + ["ELSE","CATCH",
    "SAY","ASK","SET","CALL","RETURN","WAIT","HELP",
    "IMPORT","EXPORT",
    "ADD","GET","PUT","COUNT","HAS","KEYS",
    "READ","WRITE","APPEND","EXISTS","DELETE","FILE",
    "PARSE","MAKE","JSON",
    "WITH","TO","AS","INTO","AT","KEY","TIMES","STOP"
])

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/check.py <file.claro>")
        return 2
    p = pathlib.Path(sys.argv[1])
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    stack = []
    bad = 0
    for i, line in enumerate(lines, start=1):
        if "\t" in line:
            print(f"Line {i}: contains a TAB. Use spaces.")
            bad += 1
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        head = stripped.split()[0].upper()
        if head not in KNOWN:
            print(f"Line {i}: warning: unknown keyword '{head}'.")
        if head in OPEN:
            stack.append((head, i))
        elif head in OPEN.values():
            if not stack:
                print(f"Line {i}: '{head}' without opener.")
                bad += 1
            else:
                op, oi = stack.pop()
                exp = OPEN[op]
                if head != exp:
                    print(f"Line {i}: '{head}' closes '{op}' from line {oi}, expected '{exp}'.")
                    bad += 1
    if stack:
        for op, oi in stack:
            print(f"Line {oi}: '{op}' not closed (expected {OPEN[op]}).")
        bad += len(stack)
    if bad:
        print(f"\nFound {bad} issue(s).")
        return 1
    print("No problems found.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
