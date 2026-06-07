#!/usr/bin/env python3
"""Compatibility wrapper around the built-in Claro RC0 test runner."""
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLARO = ROOT / ("claro.exe" if os.name == "nt" else "claro")

if not CLARO.exists():
    print("Build first: gcc -std=c99 src/claro.c -O0 -o " + ("claro.exe" if os.name == "nt" else "claro") + " -lm")
    raise SystemExit(2)

raise SystemExit(subprocess.call([str(CLARO), "test"], cwd=str(ROOT)))
