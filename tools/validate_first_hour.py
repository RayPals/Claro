#!/usr/bin/env python3
"""Execute every Claro code block in docs/FIRST_HOUR.md and check its output."""
from pathlib import Path
import os
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / ("claro.exe" if os.name == "nt" else "claro")
INPUTS = {2: "Ada\n", 5: "4\n"}
EXPECTED = {
    1: "Hello!\n",
    2: "What is your name?\nHello Ada\n",
    3: "0\n",
    4: "1\n",
    5: "What is 2 + 2?\nCorrect!\n",
    6: "Practice helps\nPractice helps\nPractice helps\n",
    7: "milk\nbread\n",
    8: "5\n",
    9: "Hello\n",
}


def main() -> int:
    text = (ROOT / "docs/FIRST_HOUR.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```claro\s*\n(.*?)\n```", text, flags=re.DOTALL)
    if len(blocks) != len(EXPECTED):
        print(f"FAIL: expected {len(EXPECTED)} Claro blocks, found {len(blocks)}")
        return 1
    with tempfile.TemporaryDirectory(prefix="claro-first-hour-") as tmp:
        for number, block in enumerate(blocks, 1):
            script = Path(tmp) / f"block-{number}.claro"
            script.write_text(block + "\n", encoding="utf-8")
            run = subprocess.run([str(EXE), str(script)], cwd=tmp,
                                 input=INPUTS.get(number, ""), text=True,
                                 capture_output=True)
            if run.returncode or run.stdout != EXPECTED[number]:
                print(f"FAIL: First Hour block {number}: exit={run.returncode}")
                print(f"expected stdout: {EXPECTED[number]!r}")
                print(f"actual stdout:   {run.stdout!r}")
                print(run.stderr, end="", file=sys.stderr)
                return 1
            print(f"PASS: First Hour block {number}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
