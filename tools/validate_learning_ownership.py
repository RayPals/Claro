#!/usr/bin/env python3
"""Run the full introductory learning path with invalid-access and leak checks."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    if os.name == 'nt':
        print('SKIP: learning LeakSanitizer validation requires POSIX')
        return
    with tempfile.TemporaryDirectory(prefix='claro-learning-ownership-', dir=os.environ.get('TMPDIR')) as tmp:
        binary = Path(tmp) / 'claro-asan'
        subprocess.run(['gcc', '-std=c89', '-pedantic-errors', '-Werror=implicit-function-declaration', '-O0', '-g', '-fsanitize=address,undefined', str(ROOT / 'src/claro.c'), '-o', str(binary), '-lm'], check=True)
        env = dict(os.environ, ASAN_OPTIONS='detect_leaks=1:halt_on_error=1', UBSAN_OPTIONS='halt_on_error=1', CLARO_EXE=str(binary))
        for checker in ['validate_learning_syntax.py', 'validate_first_hour.py', 'validate_error_locations.py', 'validate_error_guide.py', 'validate_learner_pilot.py', 'validate_resource_guards.py']:
            result = subprocess.run([sys.executable, str(ROOT / 'tools' / checker)], cwd=ROOT, env=env, capture_output=True, text=True, timeout=90)
            if result.returncode:
                print(result.stdout + result.stderr)
                raise SystemExit(result.returncode)
            print('PASS: leak-checked', checker)
    print('PASS: introductory lessons, examples, checker paths and REPL under ASan/UBSan/LSan')


if __name__ == '__main__':
    main()
