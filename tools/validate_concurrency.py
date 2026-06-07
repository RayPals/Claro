#!/usr/bin/env python3
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / "claro.exe"
DOC = ROOT / "docs" / "CONCURRENCY.md"


def fail(message):
    raise SystemExit(message)


def run(cmd):
    result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.returncode, result.stdout


def main():
    if not EXE.exists():
        fail(f"Missing Claro executable: {EXE}")

    if not DOC.exists():
        fail("Missing docs/CONCURRENCY.md")
    text = DOC.read_text(encoding="utf-8")
    required = ["START TASK", "YIELD", "WAIT TASK", "TASK STATUS", "cooperative", "deterministic", "no native threads"]
    for phrase in required:
        if phrase.lower() not in text.lower():
            fail(f"CONCURRENCY.md missing required phrase: {phrase}")

    rc, out = run([str(EXE), "check", "tests/40_tasks_status.claro"])
    if rc != 0:
        fail(out)

    rc, out = run([str(EXE), "tests/40_tasks_status.claro"])
    if rc != 0:
        fail(out)
    if "DONE" not in out:
        fail(f"TASK STATUS should report DONE after a cooperative task runs. Output was:\n{out}")

    with tempfile.TemporaryDirectory() as td:
        bad = Path(td) / "missing_endtask.claro"
        bad.write_text("START TASK sample\n    SAY \"oops\"\n", encoding="utf-8")
        rc, out = run([str(EXE), "check", str(bad)])
    if rc == 0:
        fail("claro check should fail when START TASK is missing ENDTASK/END")
    if "START block opened here needs ENDTASK" not in out:
        fail(f"Missing ENDTASK diagnostic was not clear enough:\n{out}")

    print("Concurrency foundation validation OK")


if __name__ == "__main__":
    main()
