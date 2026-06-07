#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / ("claro.exe" if os.name == "nt" else "claro")

EXPECTED = {
    "tests/typecheck_bad.claro": [
        "tests/typecheck_bad.claro:2: Type mismatch for score: it was first set as NUMBER, but this value looks like TEXT.",
        "tests/typecheck_bad.claro:3: Type mismatch for name: expected TEXT, but this value looks like NUMBER.",
        "tests/typecheck_bad.claro:4: Type check failed: expected TEXT, but score looks like NUMBER.",
    ],
    "tests/typecheck_container_bad.claro": [
        "tests/typecheck_container_bad.claro:3: Type mismatch for list names: expected TEXT item, but this value looks like NUMBER.",
        "tests/typecheck_container_bad.claro:6: Type mismatch for map scores: expected NUMBER value, but this value looks like TEXT.",
    ],
}

STALE_PHRASES = [
    "was first set as NUMBER, but this looks like TEXT",
    "name needs TEXT, but this looks like NUMBER",
    "Type check says this should be TEXT",
    "ADD to names needs TEXT items",
    "PUT into scores needs NUMBER values",
]


def run_typecheck(path):
    result = subprocess.run(
        [str(EXE), "typecheck", path],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print("$", EXE.name, "typecheck", path)
    print(result.stdout, end="")
    if result.returncode == 0:
        raise SystemExit(f"Expected {path} to fail typecheck")
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    expected = EXPECTED[path]
    if lines != expected:
        raise SystemExit(
            "Unexpected diagnostics for " + path + "\nExpected:\n"
            + "\n".join(expected) + "\nGot:\n" + "\n".join(lines)
        )
    for stale in STALE_PHRASES:
        if stale in result.stdout:
            raise SystemExit(f"Found stale diagnostic wording: {stale}")
    return result.stdout


def main():
    if not EXE.exists():
        raise SystemExit(f"Missing Claro executable: {EXE}")

    for path in EXPECTED:
        run_typecheck(path)

    print("Typecheck diagnostics validation complete")


if __name__ == "__main__":
    main()
