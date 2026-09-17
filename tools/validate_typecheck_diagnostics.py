#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / ("claro.exe" if os.name == "nt" else "claro")

EXPECTED = {
    "tests/typecheck_function_duplicate_param_bad.claro": [
        "tests/typecheck_function_duplicate_param_bad.claro:1: Function greet declares parameter name more than once. Give each parameter a different name.",
    ],
    "tests/typecheck_function_compat_duplicate_param_bad.claro": [
        "tests/typecheck_function_compat_duplicate_param_bad.claro:1: Function greet declares parameter name more than once. Give each parameter a different name.",
    ],
    "tests/typecheck_method_duplicate_param_bad.claro": [
        "tests/typecheck_method_duplicate_param_bad.claro:2: Method Player.greet declares parameter name more than once. Give each parameter a different name.",
    ],
    "tests/typecheck_method_compat_duplicate_param_bad.claro": [
        "tests/typecheck_method_compat_duplicate_param_bad.claro:2: Method Player.greet declares parameter name more than once. Give each parameter a different name.",
    ],
    "tests/typecheck_method_duplicate_name_bad.claro": [
        "tests/typecheck_method_duplicate_name_bad.claro:6: Method Player.show is declared more than once. Give each method a different name.",
    ],
    "tests/typecheck_method_compat_duplicate_name_bad.claro": [
        "tests/typecheck_method_compat_duplicate_name_bad.claro:6: Method Player.show is declared more than once. Give each method a different name.",
    ],
    "tests/typecheck_duplicate_field_bad.claro": [
        "tests/typecheck_duplicate_field_bad.claro:3: Class Player declares field score more than once. Give each field a different name.",
    ],
    "tests/typecheck_duplicate_class_bad.claro": [
        "tests/typecheck_duplicate_class_bad.claro:5: Class Player is declared more than once. Give each class a different name.",
    ],
    "tests/typecheck_duplicate_function_bad.claro": [
        "tests/typecheck_duplicate_function_bad.claro:5: Function greet is declared more than once. Give each function a different name.",
    ],
    "tests/typecheck_missing_function_name_bad.claro": [
        "tests/typecheck_missing_function_name_bad.claro:1: TEACH needs a function name. Add a name after TEACH, such as TEACH greet.",
    ],
    "tests/typecheck_missing_method_name_bad.claro": [
        "tests/typecheck_missing_method_name_bad.claro:2: Method Player needs a method name. Add a name after TEACH, such as TEACH show.",
    ],
    "tests/typecheck_missing_field_name_bad.claro": [
        "tests/typecheck_missing_field_name_bad.claro:2: Class Player needs a field name. Add a name and type after HAS, such as HAS score NUMBER.",
    ],
    "tests/typecheck_missing_class_name_bad.claro": [
        "tests/typecheck_missing_class_name_bad.claro:1: CLASS needs a class name. Add a name after CLASS, such as CLASS Player.",
    ],
    "tests/typecheck_duplicate_object_bad.claro": [
        "tests/typecheck_duplicate_object_bad.claro:6: Object player is created more than once. Give each object a different name.",
    ],
    "tests/typecheck_unknown_class_bad.claro": [
        "tests/typecheck_unknown_class_bad.claro:4: Class Plaeyr is not known yet. Check the class name or declare CLASS Plaeyr before creating player.",
    ],
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
    "tests/typecheck_function_return_bad.claro": [
        "tests/typecheck_function_return_bad.claro:3: Type mismatch for return from square: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_function_lowercase_return_bad.claro": [
        "tests/typecheck_function_lowercase_return_bad.claro:2: Type mismatch for return from square: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_function_compat_return_bad.claro": [
        "tests/typecheck_function_compat_return_bad.claro:3: Type mismatch for return from square: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_function_return_expression_bad.claro": [
        "tests/typecheck_function_return_expression_bad.claro:3: Type mismatch for return from label: expected TEXT, but this value looks like NUMBER.",
    ],
    "tests/typecheck_function_return_arithmetic_bad.claro": [
        "tests/typecheck_function_return_arithmetic_bad.claro:3: Type mismatch for return from total: addition needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_function_return_subtraction_bad.claro": [
        "tests/typecheck_function_return_subtraction_bad.claro:3: Type mismatch for return from total: subtraction needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_function_return_multiplication_bad.claro": [
        "tests/typecheck_function_return_multiplication_bad.claro:3: Type mismatch for return from total: multiplication needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_function_return_division_bad.claro": [
        "tests/typecheck_function_return_division_bad.claro:3: Type mismatch for return from total: division needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_method_return_subtraction_bad.claro": [
        "tests/typecheck_method_return_subtraction_bad.claro:6: Type mismatch for return from Player.total: subtraction needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_method_return_addition_bad.claro": [
        "tests/typecheck_method_return_addition_bad.claro:6: Type mismatch for return from Player.total: addition needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_method_return_division_bad.claro": [
        "tests/typecheck_method_return_division_bad.claro:6: Type mismatch for return from Player.total: division needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_method_return_multiplication_bad.claro": [
        "tests/typecheck_method_return_multiplication_bad.claro:6: Type mismatch for return from Player.total: multiplication needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_method_compat_return_addition_bad.claro": [
        "tests/typecheck_method_compat_return_addition_bad.claro:4: Type mismatch for return from Player.total: addition needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_method_compat_return_subtraction_bad.claro": [
        "tests/typecheck_method_compat_return_subtraction_bad.claro:4: Type mismatch for return from Player.total: subtraction needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_method_compat_return_division_bad.claro": [
        "tests/typecheck_method_compat_return_division_bad.claro:4: Type mismatch for return from Player.total: division needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_method_compat_return_multiplication_bad.claro": [
        "tests/typecheck_method_compat_return_multiplication_bad.claro:4: Type mismatch for return from Player.total: multiplication needs NUMBER values, but \"oops\" looks like TEXT.",
    ],
    "tests/typecheck_function_unknown_return_expression_bad.claro": [
        "tests/typecheck_function_unknown_return_expression_bad.claro:2: Function square's return value could not be understood yet. Use a NUMBER expression after RETURN.",
    ],
    "tests/typecheck_function_missing_return_bad.claro": [
        "tests/typecheck_function_missing_return_bad.claro:3: Function square declares RETURNS NUMBER but has no RETURN statement. Add RETURN with a NUMBER value.",
    ],
    "tests/typecheck_function_branch_missing_return_bad.claro": [
        "tests/typecheck_function_branch_missing_return_bad.claro:5: Function choose declares RETURNS NUMBER but does not return a NUMBER value on every path. Add RETURN to each branch or after the conditional.",
    ],
    "tests/typecheck_function_empty_return_bad.claro": [
        "tests/typecheck_function_empty_return_bad.claro:3: Function square needs a NUMBER value after RETURN. Add a NUMBER expression.",
    ],
    "tests/typecheck_method_return_bad.claro": [
        "tests/typecheck_method_return_bad.claro:3: Type mismatch for return from Player.score: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_method_compat_return_bad.claro": [
        "tests/typecheck_method_compat_return_bad.claro:4: Type mismatch for return from Player.score: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_method_compat_lowercase_return_bad.claro": [
        "tests/typecheck_method_compat_lowercase_return_bad.claro:3: Type mismatch for return from Player.score: expected NUMBER, but this value looks like TEXT.",
    ],
    "tests/typecheck_method_return_expression_bad.claro": [
        "tests/typecheck_method_return_expression_bad.claro:4: Type mismatch for return from Player.label: expected TEXT, but this value looks like NUMBER.",
    ],
    "tests/typecheck_method_unknown_return_expression_bad.claro": [
        "tests/typecheck_method_unknown_return_expression_bad.claro:4: Method Player.square's return value could not be understood yet. Use a NUMBER expression after RETURN.",
    ],
    "tests/typecheck_method_compat_unknown_return_expression_bad.claro": [
        "tests/typecheck_method_compat_unknown_return_expression_bad.claro:4: Method Player.square's return value could not be understood yet. Use a NUMBER expression after RETURN.",
    ],
    "tests/typecheck_method_field_return_bad.claro": [
        "tests/typecheck_method_field_return_bad.claro:5: Type mismatch for return from Player.label: expected TEXT, but this value looks like NUMBER.",
    ],
    "tests/typecheck_method_compat_field_return_bad.claro": [
        "tests/typecheck_method_compat_field_return_bad.claro:5: Type mismatch for return from Player.label: expected TEXT, but this value looks like NUMBER.",
    ],
    "tests/typecheck_method_missing_return_bad.claro": [
        "tests/typecheck_method_missing_return_bad.claro:4: Method Player.score declares RETURNS NUMBER but has no RETURN statement. Add RETURN with a NUMBER value.",
    ],
    "tests/typecheck_method_branch_missing_return_bad.claro": [
        "tests/typecheck_method_branch_missing_return_bad.claro:6: Method Player.choose declares RETURNS NUMBER but does not return a NUMBER value on every path. Add RETURN to each branch or after the conditional.",
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
    "tests/typecheck_method_call_missing_unchecked_arg_bad.claro": [
        "tests/typecheck_method_call_missing_unchecked_arg_bad.claro:10: Method Player.rename needs 1 argument, but this call gives 0. Add the missing argument.",
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
    "tests/typecheck_object_field_unknown_typed_bad.claro": [
        "tests/typecheck_object_field_unknown_typed_bad.claro:6: Object Player has no field level. Check the field name or add HAS level NUMBER to the class.",
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
    "tests/typecheck_invalid_expected_type_bad.claro": [
        "tests/typecheck_invalid_expected_type_bad.claro:2: CHECK TYPE needs a known type such as NUMBER, TEXT, YESNO, LIST, or MAP, but BANANA is not a Claro type.",
    ],
    "tests/typecheck_missing_is_bad.claro": [
        "tests/typecheck_missing_is_bad.claro:2: CHECK TYPE needs IS. Try: CHECK TYPE score IS NUMBER.",
    ],
    "tests/typecheck_missing_expected_type_bad.claro": [
        "tests/typecheck_missing_expected_type_bad.claro:2: CHECK TYPE score needs a type after IS. Try: CHECK TYPE score IS NUMBER.",
    ],
    "tests/typecheck_extra_check_type_tokens_bad.claro": [
        "tests/typecheck_extra_check_type_tokens_bad.claro:2: CHECK TYPE score has extra text after type NUMBER. Keep only the expression, IS, and one type.",
    ],
    "tests/typecheck_invalid_return_type_bad.claro": [
        "tests/typecheck_invalid_return_type_bad.claro:1: Function square declares an unknown return type BANANA. Use a Claro type such as NUMBER, TEXT, YESNO, LIST, or MAP.",
    ],
    "tests/typecheck_method_invalid_return_type_bad.claro": [
        "tests/typecheck_method_invalid_return_type_bad.claro:2: Method Player.score declares an unknown return type BANANA. Use a Claro type such as NUMBER, TEXT, YESNO, LIST, or MAP.",
    ],
    "tests/typecheck_unknown_field_type_bad.claro": [
        "tests/typecheck_unknown_field_type_bad.claro:2: Class Player field score uses an unknown type BANANA. Use a Claro type such as NUMBER, TEXT, YESNO, LIST, or MAP.",
    ],
    "tests/typecheck_missing_field_type_bad.claro": [
        "tests/typecheck_missing_field_type_bad.claro:2: Class Player field score is missing a type. Add a type such as NUMBER, TEXT, YESNO, LIST, or MAP after the field name.",
    ],
    "tests/typecheck_extra_class_tokens_bad.claro": [
        "tests/typecheck_extra_class_tokens_bad.claro:1: Class Player has extra text after its name. Keep only the class name after CLASS.",
    ],
    "tests/typecheck_extra_new_tokens_bad.claro": [
        "tests/typecheck_extra_new_tokens_bad.claro:5: NEW Player has extra text after object name player. Keep only the class and object names.",
    ],
    "tests/typecheck_missing_object_name_bad.claro": [
        "tests/typecheck_missing_object_name_bad.claro:5: NEW Player needs an object name. Add a name after the class, such as NEW Player player.",
    ],
    "tests/typecheck_missing_new_class_name_bad.claro": [
        "tests/typecheck_missing_new_class_name_bad.claro:1: NEW needs a class name. Add a class and object name, such as NEW Player player.",
    ],
    "tests/typecheck_extra_field_tokens_bad.claro": [
        "tests/typecheck_extra_field_tokens_bad.claro:2: Class Player field score has extra text after type NUMBER. Keep only the field name and one type.",
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
    "tests/typecheck_object_alias_method_call_extra_arg_bad.claro": [
        "tests/typecheck_object_alias_method_call_extra_arg_bad.claro:12: Method Player.add only accepts 1 argument, but this call gives 2. Remove the extra argument.",
    ],
    "tests/typecheck_method_field_assignment_bad.claro": [
        "tests/typecheck_method_field_assignment_bad.claro:5: Type mismatch for field score in Player.add: addition needs NUMBER values, but name looks like TEXT.",
    ],
    "tests/typecheck_method_unknown_field_bad.claro": [
        "tests/typecheck_method_unknown_field_bad.claro:5: Object Player has no field level. Check the field name or add HAS level NUMBER to the class.",
    ],
    "tests/typecheck_method_compat_unknown_field_bad.claro": [
        "tests/typecheck_method_compat_unknown_field_bad.claro:5: Object Player has no field level. Check the field name or add HAS level NUMBER to the class.",
    ],
    "tests/typecheck_method_compat_unknown_field_expression_bad.claro": [
        "tests/typecheck_method_compat_unknown_field_expression_bad.claro:5: Object Player has no field level. Check the field name or add the field to the class with the right type.",
    ],
    "tests/typecheck_method_unknown_field_typed_bad.claro": [
        "tests/typecheck_method_unknown_field_typed_bad.claro:4: Object Player has no field level. Check the field name or add HAS level NUMBER to the class.",
    ],
    "tests/typecheck_method_compat_unknown_field_typed_bad.claro": [
        "tests/typecheck_method_compat_unknown_field_typed_bad.claro:4: Object Player has no field level. Check the field name or add HAS level NUMBER to the class.",
    ],
    "tests/typecheck_method_typed_field_assignment_bad.claro": [
        "tests/typecheck_method_typed_field_assignment_bad.claro:5: Type mismatch for field score in Player.set_score: class declares NUMBER, but this assignment says TEXT. Use NUMBER for score.",
    ],
    "tests/typecheck_method_inline_field_annotation_bad.claro": [
        "tests/typecheck_method_inline_field_annotation_bad.claro:5: Type mismatch for field score in Player.set_score: class declares NUMBER, but this assignment says TEXT. Use NUMBER for score.",
    ],
    "tests/typecheck_method_compat_inline_field_annotation_bad.claro": [
        "tests/typecheck_method_compat_inline_field_annotation_bad.claro:5: Type mismatch for field score in Player.set_score: class declares NUMBER, but this assignment says TEXT. Use NUMBER for score.",
    ],
    "tests/typecheck_method_inline_field_annotation_unknown_type_bad.claro": [
        "tests/typecheck_method_inline_field_annotation_unknown_type_bad.claro:5: Field score in Player.set_score needs a known type such as NUMBER, TEXT, or YESNO, but BANANA is not a Claro type. Use NUMBER for score.",
    ],
    "tests/typecheck_method_compat_inline_field_annotation_unknown_type_bad.claro": [
        "tests/typecheck_method_compat_inline_field_annotation_unknown_type_bad.claro:5: Field score in Player.set_score needs a known type such as NUMBER, TEXT, or YESNO, but BANANA is not a Claro type. Use NUMBER for score.",
    ],
    "tests/typecheck_method_unknown_field_expression_bad.claro": [
        "tests/typecheck_method_unknown_field_expression_bad.claro:5: Object Player has no field level. Check the field name or add the field to the class with the right type.",
    ],
    "tests/typecheck_method_unknown_field_check_type_bad.claro": [
        "tests/typecheck_method_unknown_field_check_type_bad.claro:5: Object Player has no field level. Check the field name or add HAS level NUMBER to the class.",
    ],
    "tests/typecheck_method_compat_unknown_field_check_type_bad.claro": [
        "tests/typecheck_method_compat_unknown_field_check_type_bad.claro:5: Object Player has no field level. Check the field name or add HAS level NUMBER to the class.",
    ],
    "tests/typecheck_method_text_field_assignment_bad.claro": [
        "tests/typecheck_method_text_field_assignment_bad.claro:4: Type mismatch for field name in Player.rename: expected TEXT, but this value looks like NUMBER.",
    ],
    "tests/typecheck_method_compat_text_field_assignment_bad.claro": [
        "tests/typecheck_method_compat_text_field_assignment_bad.claro:4: Type mismatch for field name in Player.rename: expected TEXT, but this value looks like NUMBER.",
    ],
    "tests/typecheck_method_yesno_field_assignment_bad.claro": [
        "tests/typecheck_method_yesno_field_assignment_bad.claro:4: Type mismatch for field ready in Player.toggle: expected YESNO, but this value looks like TEXT.",
    ],
    "tests/typecheck_method_compat_yesno_field_assignment_bad.claro": [
        "tests/typecheck_method_compat_yesno_field_assignment_bad.claro:4: Type mismatch for field ready in Player.toggle: expected YESNO, but this value looks like TEXT.",
    ],
    "tests/typecheck_method_field_check_type_bad.claro": [
        "tests/typecheck_method_field_check_type_bad.claro:4: Type check failed in Player.rename: expected NUMBER, but name looks like TEXT.",
    ],
    "tests/typecheck_method_compat_field_check_type_bad.claro": [
        "tests/typecheck_method_compat_field_check_type_bad.claro:4: Type check failed in Player.rename: expected NUMBER, but name looks like TEXT.",
    ],
    "tests/typecheck_method_compat_yesno_field_check_type_bad.claro": [
        "tests/typecheck_method_compat_yesno_field_check_type_bad.claro:4: Type check failed in Player.toggle: expected TEXT, but ready looks like YESNO.",
    ],
}

EXPECTED_OK = [
    "tests/typecheck_function_good.claro",
    "tests/typecheck_function_return_good.claro",
    "tests/typecheck_function_compat_return_good.claro",
    "tests/typecheck_function_compat_lowercase_return_good.claro",
    "tests/typecheck_function_lowercase_return_good.claro",
    "tests/typecheck_function_return_expression_good.claro",
    "tests/typecheck_function_return_multiplication_good.claro",
    "tests/typecheck_function_return_division_good.claro",
    "tests/typecheck_function_return_subtraction_good.claro",
    "tests/typecheck_function_unknown_return_expression_good.claro",
    "tests/typecheck_function_branch_complete_good.claro",
    "tests/typecheck_function_nested_branch_complete_good.claro",
    "tests/typecheck_method_return_good.claro",
    "tests/typecheck_method_field_return_good.claro",
    "tests/typecheck_method_compat_field_return_good.claro",
    "tests/typecheck_method_compat_return_good.claro",
    "tests/typecheck_method_compat_lowercase_return_good.claro",
    "tests/typecheck_method_compat_return_division_good.claro",
    "tests/typecheck_method_compat_return_subtraction_good.claro",
    "tests/typecheck_method_compat_return_multiplication_good.claro",
    "tests/typecheck_method_compat_return_addition_good.claro",
    "tests/typecheck_method_return_expression_good.claro",
    "tests/typecheck_method_return_multiplication_good.claro",
    "tests/typecheck_method_return_division_good.claro",
    "tests/typecheck_method_return_subtraction_good.claro",
    "tests/typecheck_method_return_addition_good.claro",
    "tests/typecheck_method_unknown_return_expression_good.claro",
    "tests/typecheck_method_field_assignment_good.claro",
    "tests/typecheck_method_text_field_assignment_good.claro",
    "tests/typecheck_method_yesno_field_assignment_good.claro",
    "tests/typecheck_method_compat_text_field_assignment_good.claro",
    "tests/typecheck_method_compat_yesno_field_assignment_good.claro",
    "tests/typecheck_method_compat_field_assignment_good.claro",
    "tests/typecheck_method_text_concat_good.claro",
    "tests/typecheck_method_compat_text_concat_good.claro",
    "tests/typecheck_method_field_check_type_good.claro",
    "tests/typecheck_method_compat_field_check_type_good.claro",
    "tests/typecheck_method_compat_yesno_field_check_type_good.claro",
    "tests/typecheck_method_yesno_field_check_type_good.claro",
    "tests/typecheck_method_inline_field_annotation_good.claro",
    "tests/typecheck_method_compat_inline_field_annotation_good.claro",
    "tests/typecheck_method_nested_branch_complete_good.claro",
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
    "tests/typecheck_object_field_text_concat_good.claro",
    "tests/typecheck_object_field_text_concat_reverse_good.claro",
    "tests/typecheck_object_field_text_concat_fields_good.claro",
    "tests/typecheck_object_field_yesno_good.claro",
    "tests/typecheck_object_field_check_type_number_good.claro",
    "tests/typecheck_object_field_check_type_text_good.claro",
    "tests/typecheck_object_field_check_type_yesno_good.claro",
    "tests/typecheck_object_field_check_type_text_yesno_good.claro",
    "tests/typecheck_same_field_name_different_classes_good.claro",
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
