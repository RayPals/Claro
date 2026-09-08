#!/usr/bin/env python3
"""Regression tests for complete typecheck fixture coverage."""
import importlib.util
from pathlib import Path
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

    def test_includes_dedicated_yesno_field_check_success_fixture(self):
        self.assertIn(
            "tests/typecheck_object_field_check_type_yesno_good.claro",
            MODULE.EXPECTED_OK,
        )


if __name__ == "__main__":
    unittest.main()
