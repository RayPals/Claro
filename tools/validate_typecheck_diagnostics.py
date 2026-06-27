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
    "tests/typecheck_function_bad.claro": [
        "tests/typecheck_function_bad.claro:5: Type mismatch for function square: parameter amount needs NUMBER, but this argument looks like TEXT.",
    ],
    "tests/typecheck_function_multi_bad.claro": [
        "tests/typecheck_function_multi_bad.claro:8: Type mismatch for function label: parameter name needs TEXT, but this argument looks like NUMBER.",
        "tests/typecheck_function_multi_bad.claro:8: Type mismatch for function label: parameter age needs NUMBER, but this argument looks like TEXT.",
    ],
    "tests/typecheck_method_bad.claro": [
        "tests/typecheck_method_bad.claro:11: Type mismatch for method Player.add: parameter points needs NUMBER, but this argument looks like TEXT.",
    ],
    "tests/typecheck_object_field_bad.claro": [
        "tests/typecheck_object_field_bad.claro:6: Type mismatch for field player.score: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_object_field_text_bad.claro": [
        "tests/typecheck_object_field_text_bad.claro:6: Type mismatch for field player.name: expected TEXT, but this value looks like NUMBER.",
    ],
    "tests/typecheck_object_field_yesno_bad.claro": [
        "tests/typecheck_object_field_yesno_bad.claro:6: Type mismatch for field player.ready: expected YESNO, but this value looks like TEXT.",
    ],
    "tests/typecheck_object_field_unknown_bad.claro": [
        "tests/typecheck_object_field_unknown_bad.claro:6: Object Player has no field level. Check the field name or add HAS level NUMBER to the class.",
    ],
    "tests/typecheck_object_field_unknown_text_bad.claro": [
        "tests/typecheck_object_field_unknown_text_bad.claro:6: Object Player has no field nickname. Check the field name or add HAS nickname TEXT to the class.",
    ],
    "tests/typecheck_object_field_unknown_yesno_bad.claro": [
        "tests/typecheck_object_field_unknown_yesno_bad.claro:6: Object Player has no field ready. Check the field name or add HAS ready YESNO to the class.",
    ],
    "tests/typecheck_object_field_check_type_text_bad.claro": [
        "tests/typecheck_object_field_check_type_text_bad.claro:7: Type check failed: expected NUMBER, but player.name looks like TEXT.",
    ],
}

EXPECTED_OK = [
    "tests/typecheck_function_good.claro",
    "tests/typecheck_function_multi_good.claro",
    "tests/typecheck_method_good.claro",
    "tests/typecheck_object_field_good.claro",
    "tests/typecheck_object_field_text_good.claro",
    "tests/typecheck_object_field_yesno_good.claro",
    "tests/typecheck_object_field_check_type_text_yesno_good.claro",
    "tests/37_object_field_types.claro",
]

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


def run_typecheck_ok(path):
    result = subprocess.run(
        [str(EXE), "typecheck", path],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print("$", EXE.name, "typecheck", path)
    print(result.stdout, end="")
    if result.returncode != 0:
        raise SystemExit(f"Expected {path} to pass typecheck")
    lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if lines != ["Type check OK"]:
        raise SystemExit("Unexpected success output for " + path + "\nGot:\n" + "\n".join(lines))


def main():
    if not EXE.exists():
        raise SystemExit(f"Missing Claro executable: {EXE}")

    for path in EXPECTED:
        run_typecheck(path)

    for path in EXPECTED_OK:
        run_typecheck_ok(path)

    print("Typecheck diagnostics validation complete")


if __name__ == "__main__":
    main()
