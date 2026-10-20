#!/usr/bin/env python3
"""Verify recursive Claro calls stop with the documented runtime diagnostic."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = (
    "Claro function call depth exceeded the safe limit of 256. "
    "Simplify the recursion or add a stopping condition."
)
SCRIPT = """TEACH loop
    CALL loop
ENDTEACH
TRY
    CALL loop
CATCH
    SAY LASTERROR
ENDTRY
"""


def main() -> int:
    binary = ROOT / ("claro.exe" if sys.platform == "win32" else "claro")
    if not binary.exists():
        print(f"FAIL: build Claro first; missing {binary}")
        return 1
    with tempfile.TemporaryDirectory(prefix="claro-call-depth-") as tmp:
        program = Path(tmp) / "recursive.claro"
        program.write_text(SCRIPT, encoding="utf-8")
        run = subprocess.run([str(binary), str(program)], cwd=ROOT, text=True,
                             capture_output=True, timeout=30)
    output = run.stdout + run.stderr
    if EXPECTED not in output:
        print("FAIL: recursion did not produce the documented call-depth error")
        print(output, end="")
        return 1
    if run.returncode == 0:
        print("FAIL: runtime error unexpectedly exited successfully")
        return 1
    print("PASS: unbounded recursion stops with the documented call-depth error")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
