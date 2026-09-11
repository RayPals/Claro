#!/usr/bin/env python3
"""Regression tests for complete typecheck fixture coverage."""
import importlib.util
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_typecheck_diagnostics", ROOT / "tools" / "validate_typecheck_diagnostics.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateTypecheckDiagnosticsTests(unittest.TestCase):
    def test_lists_every_typecheck_fixture(self):
        listed = set(MODULE.EXPECTED) | set(MODULE.EXPECTED_OK)
        fixtures = {
            str(path.relative_to(ROOT))
            for path in (ROOT / "tests").glob("typecheck_*.claro")
        }
        fixtures.add("tests/37_object_field_types.claro")
        self.assertEqual(listed, fixtures)

    def test_includes_modern_chained_alias_method_success_fixture(self):
        self.assertIn(
            "tests/typecheck_object_alias_method_do_good.claro",
            MODULE.EXPECTED_OK,
        )
    def test_has_compatibility_chained_alias_method_extra_arg_fixture(self):
        self.assertTrue(
            (ROOT / "tests/typecheck_object_alias_method_call_extra_arg_bad.claro").exists()
        )

    def test_includes_dedicated_yesno_field_check_success_fixture(self):
        self.assertIn(
            "tests/typecheck_object_field_check_type_yesno_good.claro",
            MODULE.EXPECTED_OK,
        )

    def test_includes_reverse_text_concatenation_success_fixture(self):
        self.assertIn(
            "tests/typecheck_object_field_text_concat_reverse_good.claro",
            MODULE.EXPECTED_OK,
        )

    def test_includes_typed_function_return_fixtures(self):
        self.assertIn("tests/typecheck_function_return_bad.claro", MODULE.EXPECTED)
        self.assertIn("tests/typecheck_function_return_good.claro", MODULE.EXPECTED_OK)

    def test_includes_unknown_function_return_expression_fixtures(self):
        self.assertIn(
            "tests/typecheck_function_unknown_return_expression_bad.claro",
            MODULE.EXPECTED,
        )
        self.assertIn(
            "tests/typecheck_function_unknown_return_expression_good.claro",
            MODULE.EXPECTED_OK,
        )

    def test_includes_lowercase_compatibility_return_success_fixture(self):
        self.assertIn(
            "tests/typecheck_function_lowercase_return_good.claro",
            MODULE.EXPECTED_OK,
        )

    def test_includes_lowercase_compatibility_syntax_return_success_fixture(self):
        self.assertIn(
            "tests/typecheck_function_compat_lowercase_return_good.claro",
            MODULE.EXPECTED_OK,
        )

    def test_includes_missing_function_return_fixture(self):
        self.assertIn("tests/typecheck_function_missing_return_bad.claro", MODULE.EXPECTED)

    def test_includes_branch_missing_function_return_fixture(self):
        self.assertIn("tests/typecheck_function_branch_missing_return_bad.claro", MODULE.EXPECTED)

    def test_includes_empty_function_return_fixture(self):
        self.assertIn("tests/typecheck_function_empty_return_bad.claro", MODULE.EXPECTED)

    def test_includes_missing_method_return_fixture(self):
        self.assertIn("tests/typecheck_method_missing_return_bad.claro", MODULE.EXPECTED)

    def test_includes_typed_method_return_expression_fixtures(self):
        self.assertIn("tests/typecheck_method_return_expression_bad.claro", MODULE.EXPECTED)
        self.assertIn("tests/typecheck_method_return_expression_good.claro", MODULE.EXPECTED_OK)

    def test_includes_unknown_method_return_expression_fixtures(self):
        self.assertIn(
            "tests/typecheck_method_unknown_return_expression_bad.claro",
            MODULE.EXPECTED,
        )
        self.assertIn(
            "tests/typecheck_method_unknown_return_expression_good.claro",
            MODULE.EXPECTED_OK,
        )

    def test_includes_method_field_return_diagnostic_fixture(self):
        self.assertIn("tests/typecheck_method_field_return_bad.claro", MODULE.EXPECTED)
        self.assertIn("tests/typecheck_method_field_return_good.claro", MODULE.EXPECTED_OK)

    def test_includes_compatibility_method_return_success_fixture(self):
        self.assertIn("tests/typecheck_method_compat_return_good.claro", MODULE.EXPECTED_OK)

    def test_includes_lowercase_compatibility_method_return_success_fixture(self):
        self.assertIn(
            "tests/typecheck_method_compat_lowercase_return_good.claro",
            MODULE.EXPECTED_OK,
        )

    def test_includes_compatibility_missing_method_argument_fixture(self):
        self.assertIn(
            "tests/typecheck_method_call_missing_unchecked_arg_bad.claro",
            MODULE.EXPECTED,
        )

    def test_release_validation_runs_method_call_fixture(self):
        result = subprocess.run(
            [str(ROOT / "claro"), "validate"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("tests/typecheck_method_call_bad.claro", result.stdout)
        self.assertIn(
            '"tests/typecheck_method_compat_lowercase_return_good.claro"',
            (ROOT / "src" / "claro.c").read_text(),
        )


if __name__ == "__main__":
    unittest.main()
