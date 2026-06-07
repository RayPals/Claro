#!/usr/bin/env python3
import os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)

exe = './claro.exe' if os.name == 'nt' else './claro'
cmds = [
    ['gcc', '-std=c99', 'src/claro.c', '-O0', '-o', exe, '-lm'],
    [exe, '--version'],
    [exe, 'test'],
    [exe, 'validate'],
    [exe, 'check', 'examples/objects_classes.claro'],
]
for cmd in cmds:
    print('+', ' '.join(cmd))
    rc = subprocess.call(cmd)
    if rc != 0:
        sys.exit(rc)
print('Claro v1.15.26 validation passed.')
