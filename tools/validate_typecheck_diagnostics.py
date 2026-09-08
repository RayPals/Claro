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
    "tests/typecheck_function_missing_arg_bad.claro": [
        "tests/typecheck_function_missing_arg_bad.claro:6: Function square needs argument amount as NUMBER, but this call does not provide it.",
    ],
    "tests/typecheck_function_missing_unchecked_arg_bad.claro": [
        "tests/typecheck_function_missing_unchecked_arg_bad.claro:5: Function greet needs 1 argument, but this call gives 0. Add the missing argument.",
    ],
    "tests/typecheck_function_call_missing_unchecked_arg_bad.claro": [
        "tests/typecheck_function_call_missing_unchecked_arg_bad.claro:5: Function greet needs 1 argument, but this call gives 0. Add the missing argument.",
    ],
    "tests/typecheck_function_extra_arg_bad.claro": [
        "tests/typecheck_function_extra_arg_bad.claro:6: Function square only accepts 1 argument, but this call gives 2. Remove the extra argument.",
    ],
    "tests/typecheck_function_unknown_bad.claro": [
        "tests/typecheck_function_unknown_bad.claro:6: Function squre is not known yet. Check the function name or add TEACH squre before calling it.",
    ],
    "tests/typecheck_function_call_unknown_bad.claro": [
        "tests/typecheck_function_call_unknown_bad.claro:6: Function squre is not known yet. Check the function name or add TEACH squre before calling it.",
    ],
    "tests/typecheck_method_bad.claro": [
        "tests/typecheck_method_bad.claro:11: Type mismatch for method Player.add: parameter points needs NUMBER, but this argument looks like TEXT.",
    ],
    "tests/typecheck_method_call_bad.claro": [
        "tests/typecheck_method_call_bad.claro:11: Type mismatch for method Player.add: parameter points needs NUMBER, but this argument looks like TEXT.",
    ],
    "tests/typecheck_method_second_method_bad.claro": [
        "tests/typecheck_method_second_method_bad.claro:15: Type mismatch for method Player.add: parameter points needs NUMBER, but this argument looks like TEXT.",
    ],
    "tests/typecheck_method_second_method_extra_arg_bad.claro": [
        "tests/typecheck_method_second_method_extra_arg_bad.claro:15: Method Player.add only accepts 1 argument, but this call gives 2. Remove the extra argument.",
    ],
    "tests/typecheck_method_missing_arg_bad.claro": [
        "tests/typecheck_method_missing_arg_bad.claro:11: Method Player.add needs argument points as NUMBER, but this call does not provide it.",
    ],
    "tests/typecheck_method_missing_unchecked_arg_bad.claro": [
        "tests/typecheck_method_missing_unchecked_arg_bad.claro:10: Method Player.rename needs 1 argument, but this call gives 0. Add the missing argument.",
    ],
    "tests/typecheck_method_extra_arg_bad.claro": [
        "tests/typecheck_method_extra_arg_bad.claro:11: Method Player.add only accepts 1 argument, but this call gives 2. Remove the extra argument.",
    ],
    "tests/typecheck_method_unknown_object_bad.claro": [
        "tests/typecheck_method_unknown_object_bad.claro:10: Object player is not known yet. Create it with NEW ClassName player before calling player.add.",
    ],
    "tests/typecheck_method_call_unknown_object_bad.claro": [
        "tests/typecheck_method_call_unknown_object_bad.claro:10: Object player is not known yet. Create it with NEW ClassName player before calling player.add.",
    ],
    "tests/typecheck_method_call_unknown_object_unknown_method_bad.claro": [
        "tests/typecheck_method_call_unknown_object_unknown_method_bad.claro:10: Object player is not known yet. Create it with NEW ClassName player before calling player.fly.",
    ],
    "tests/typecheck_method_unknown_method_bad.claro": [
        "tests/typecheck_method_unknown_method_bad.claro:11: Object Player has no method fly. Check the method name or add TEACH fly inside CLASS Player.",
    ],
    "tests/typecheck_method_call_unknown_method_bad.claro": [
        "tests/typecheck_method_call_unknown_method_bad.claro:11: Object Player has no method fly. Check the method name or add TEACH fly inside CLASS Player.",
    ],
    "tests/typecheck_object_field_bad.claro": [
        "tests/typecheck_object_field_bad.claro:6: Type mismatch for field player.score: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_object_field_typed_bad.claro": [
        "tests/typecheck_object_field_typed_bad.claro:6: Type mismatch for field player.score: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_object_field_after_method_bad.claro": [
        "tests/typecheck_object_field_after_method_bad.claro:10: Type mismatch for field player.score: expected NUMBER, but this value looks like TEXT.",
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
    "tests/typecheck_object_field_unknown_expression_bad.claro": [
        "tests/typecheck_object_field_unknown_expression_bad.claro:7: Object Player has no field level. Check the field name or add the field to the class with the right type.",
    ],
    "tests/typecheck_object_field_expression_bad.claro": [
        "tests/typecheck_object_field_expression_bad.claro:8: Type mismatch for field player.score: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_object_field_compound_bad.claro": [
        "tests/typecheck_object_field_compound_bad.claro:8: Type mismatch for field player.score: addition needs NUMBER values, but player.name looks like TEXT.",
    ],
    "tests/typecheck_object_field_addition_bad.claro": [
        "tests/typecheck_object_field_addition_bad.claro:8: Type mismatch for field player.score: addition needs NUMBER values, but player.name looks like TEXT.",
    ],
    "tests/typecheck_object_field_subtraction_bad.claro": [
        "tests/typecheck_object_field_subtraction_bad.claro:8: Type mismatch for field player.score: subtraction needs NUMBER values, but player.name looks like TEXT.",
    ],
    "tests/typecheck_object_field_multiplication_bad.claro": [
        "tests/typecheck_object_field_multiplication_bad.claro:8: Type mismatch for field player.score: multiplication needs NUMBER values, but player.name looks like TEXT.",
    ],
    "tests/typecheck_object_field_division_bad.claro": [
        "tests/typecheck_object_field_division_bad.claro:8: Type mismatch for field player.score: division needs NUMBER values, but player.name looks like TEXT.",
    ],
    "tests/typecheck_object_field_text_expression_bad.claro": [
        "tests/typecheck_object_field_text_expression_bad.claro:8: Type mismatch for field player.name: expected TEXT, but this value looks like NUMBER.",
    ],
    "tests/typecheck_object_field_check_type_text_bad.claro": [
        "tests/typecheck_object_field_check_type_text_bad.claro:7: Type check failed: expected NUMBER, but player.name looks like TEXT.",
    ],
    "tests/typecheck_object_field_check_type_yesno_bad.claro": [
        "tests/typecheck_object_field_check_type_yesno_bad.claro:7: Type check failed: expected TEXT, but player.ready looks like YESNO.",
    ],
    "tests/typecheck_object_field_check_type_number_bad.claro": [
        "tests/typecheck_object_field_check_type_number_bad.claro:7: Type check failed: expected TEXT, but player.score looks like NUMBER.",
    ],
    "tests/typecheck_object_field_check_type_unknown_number_bad.claro": [
        "tests/typecheck_object_field_check_type_unknown_number_bad.claro:6: Object Player has no field level. Check the field name or add HAS level NUMBER to the class.",
    ],
    "tests/typecheck_object_field_check_type_unknown_text_bad.claro": [
        "tests/typecheck_object_field_check_type_unknown_text_bad.claro:6: Object Player has no field nickname. Check the field name or add HAS nickname TEXT to the class.",
    ],
    "tests/typecheck_object_field_check_type_unknown_yesno_bad.claro": [
        "tests/typecheck_object_field_check_type_unknown_yesno_bad.claro:6: Object Player has no field enabled. Check the field name or add HAS enabled YESNO to the class.",
    ],
    "tests/typecheck_object_field_check_type_unknown_object_bad.claro": [
        "tests/typecheck_object_field_check_type_unknown_object_bad.claro:5: Object player is not known yet. Create it with NEW ClassName player before checking player.score.",
    ],
    "tests/typecheck_object_field_unknown_object_bad.claro": [
        "tests/typecheck_object_field_unknown_object_bad.claro:5: Object player is not known yet. Create it with NEW ClassName player before setting player.score.",
    ],
    "tests/typecheck_object_field_alias_bad.claro": [
        "tests/typecheck_object_field_alias_bad.claro:7: Type mismatch for field alias.score: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_object_field_check_type_alias_bad.claro": [
        "tests/typecheck_object_field_check_type_alias_bad.claro:8: Type check failed: expected TEXT, but alias.score looks like NUMBER.",
    ],
    "tests/typecheck_object_field_check_type_chained_alias_bad.claro": [
        "tests/typecheck_object_field_check_type_chained_alias_bad.claro:8: Type check failed: expected TEXT, but backup.score looks like NUMBER.",
    ],
    "tests/typecheck_object_field_chained_alias_bad.claro": [
        "tests/typecheck_object_field_chained_alias_bad.claro:8: Type mismatch for field backup.score: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_object_alias_method_bad.claro": [
        "tests/typecheck_object_alias_method_bad.claro:12: Type mismatch for method Player.add: parameter points needs NUMBER, but this argument looks like TEXT.",
    ],
    "tests/typecheck_object_alias_method_call_bad.claro": [
        "tests/typecheck_object_alias_method_call_bad.claro:12: Type mismatch for method Player.add: parameter points needs NUMBER, but this argument looks like TEXT.",
    ],
}

EXPECTED_OK = [
    "tests/typecheck_function_good.claro",
    "tests/typecheck_function_multi_good.claro",
    "tests/typecheck_method_good.claro",
    "tests/typecheck_method_call_good.claro",
    "tests/typecheck_object_field_good.claro",
    "tests/typecheck_object_field_expression_good.claro",
    "tests/typecheck_object_field_compound_good.claro",
    "tests/typecheck_object_field_subtraction_good.claro",
    "tests/typecheck_object_field_division_good.claro",
    "tests/typecheck_object_field_multiplication_good.claro",
    "tests/typecheck_object_field_text_good.claro",
    "tests/typecheck_object_field_yesno_good.claro",
    "tests/typecheck_object_field_check_type_number_good.claro",
    "tests/typecheck_object_field_check_type_text_good.claro",
    "tests/typecheck_object_field_check_type_yesno_good.claro",
    "tests/typecheck_object_field_check_type_text_yesno_good.claro",
    "tests/typecheck_object_field_alias_good.claro",
    "tests/typecheck_object_field_check_type_chained_alias_good.claro",
    "tests/typecheck_object_field_check_type_chained_alias_text_good.claro",
    "tests/typecheck_object_alias_method_call_good.claro",
    "tests/typecheck_object_alias_method_do_good.claro",
    "tests/typecheck_nested_container_good.claro",
    "tests/typecheck_good.claro",
    "tests/typecheck_container_good.claro",
    "tests/37_object_field_types.claro",
]

STALE_PHRASES = [
    "was first set as NUMBER, but this looks like TEXT",
    "name needs TEXT, but this looks like NUMBER",
    "Type check says this should be TEXT",
    "ADD to names needs TEXT items",
    "PUT into scores needs NUMBER values",
]


def validate_fixture_coverage():
    discovered = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").glob("typecheck_*.claro")
    }
    listed = set(EXPECTED) | set(EXPECTED_OK)
    missing = sorted(discovered - listed)
    extra = sorted(listed - discovered - {"tests/37_object_field_types.claro"})
    if missing or extra:
        details = []
        if missing:
            details.append("unlisted fixtures: " + ", ".join(missing))
        if extra:
            details.append("missing fixture files: " + ", ".join(extra))
        raise SystemExit("Typecheck fixture coverage mismatch: " + "; ".join(details))


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

    validate_fixture_coverage()
    for path in EXPECTED:
        run_typecheck(path)

    for path in EXPECTED_OK:
        run_typecheck_ok(path)

    print("Typecheck diagnostics validation complete")


if __name__ == "__main__":
    main()
