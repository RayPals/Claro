#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXE = os.path.join(ROOT, 'claro.exe' if os.name == 'nt' else 'claro')
SRC = os.path.join(ROOT, 'src', 'claro.c')

cmd = ['gcc', '-std=c99', SRC, '-O0', '-o', EXE, '-lm']
print('+', ' '.join(cmd))
subprocess.check_call(cmd, cwd=ROOT)

checks = [
    [EXE, '--version'],
    [EXE, 'test'],
    [EXE, 'check', 'tests/25_simple_syntax.claro'],
    [EXE, 'check', 'tests/26_end_alias.claro'],
    [EXE, 'check', 'tests/28_text_list_helpers.claro'],
    [EXE, 'tests/29_arguments_demo.claro', 'apple', 'banana'],
]

for c in checks:
    print('+', ' '.join(c))
    subprocess.check_call(c, cwd=ROOT)

print('RC6 validation completed.')
