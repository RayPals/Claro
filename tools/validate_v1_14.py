#!/usr/bin/env python3
"""Validate Claro v1.14.26 from the package root."""
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXE = os.path.join(ROOT, 'claro_validate')
SRC = os.path.join(ROOT, 'src', 'claro.c')

def run(cmd, **kwargs):
    print('+', ' '.join(cmd))
    return subprocess.run(cmd, cwd=ROOT, text=True, **kwargs)

if run(['gcc', '-std=c99', SRC, '-O0', '-o', EXE, '-lm']).returncode:
    sys.exit(1)
if run([EXE, '--version']).returncode:
    sys.exit(1)
if run([EXE, 'test']).returncode:
    sys.exit(1)
if run([EXE, 'typecheck', 'tests/typecheck_good.claro']).returncode:
    sys.exit(1)
bad = run([EXE, 'typecheck', 'tests/typecheck_bad.claro'])
if bad.returncode == 0:
    print('Expected typecheck_bad.claro to fail')
    sys.exit(1)
if run([EXE, 'validate']).returncode:
    sys.exit(1)
print('Claro v1.14.26 validation passed.')
