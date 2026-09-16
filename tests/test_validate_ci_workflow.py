#!/usr/bin/env python3
"""Regression tests for the CI workflow release-gate validator."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_ci_workflow", ROOT / "tools" / "validate_ci_workflow.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateCiWorkflowTests(unittest.TestCase):
    def test_accepts_release_gate_commands_in_run_steps(self):
        workflow = """
        steps:
          - name: Build
            run: make
          - name: Release gates
            run: ./claro validate
          - name: Type diagnostics
            run: python3 tools/validate_typecheck_diagnostics.py
          - name: Version
            run: python3 tools/validate_version_convention.py
          - name: Packages
            run: python3 tools/validate_package_security.py
          - name: Compiler warnings
            run: python3 tools/validate_compiler_warnings.py
          - name: CI workflow
            run: python3 tools/validate_ci_workflow.py
        """
        self.assertEqual(MODULE.missing_release_gates(workflow), [])

    def test_requires_the_workflow_validator_to_run_in_ci(self):
        self.assertIn("python3 tools/validate_ci_workflow.py", MODULE.REQUIRED_COMMANDS)

    def test_rejects_commands_that_only_appear_in_comments(self):
        workflow = """
        steps:
          # run: ./claro validate
          # python3 tools/validate_typecheck_diagnostics.py
          - name: Build
            run: make
        """
        self.assertEqual(
            MODULE.missing_release_gates(workflow), MODULE.REQUIRED_COMMANDS
        )


if __name__ == "__main__":
    unittest.main()
