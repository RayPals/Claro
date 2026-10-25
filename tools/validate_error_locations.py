#!/usr/bin/env python3
"""Verify real runtime diagnostic origins, including functions/imports/TRY."""
from pathlib import Path
import os
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix='claro-error-locations-', dir=os.environ.get('TMPDIR')) as temp:
        work = Path(temp)
        override = os.environ.get('CLARO_EXE')
        exe = Path(override).resolve() if override else work / 'claro'
        if not override:
            compiler = shlex.split(os.environ.get('CLARO_CC', 'gcc'))
            subprocess.run(compiler + ['-std=c89', '-pedantic-errors', str(ROOT / 'src/claro.c'), '-o', str(exe), '-lm'], check=True)
        cases = [
            ('quote.claro', 'SAY "Start"\nSAY "unfinished\n', 2, 'Text is missing a closing quote.'),
            ('operand.claro', 'SET score 1\nSAY score +\n', 2, 'needs a value after the operator'),
            ('parenthesis.claro', 'SAY "Start"\nSAY (1 + 2\n', 2, 'needs a closing parenthesis'),
            ('function.claro', 'TEACH broken\n    SAY 1 +\nEND\nDO broken\n', 2, 'needs a value after the operator'),
            ('repeat.claro', 'REPEAT\n    SAY "Once"\nUNTIL (\n', 3, 'needs a value after the operator'),
        ]
        for name, text, line, message in cases:
            (work / name).write_text(text)
            result = subprocess.run([str(exe), name], cwd=work, capture_output=True, text=True, timeout=10)
            output = result.stdout + result.stderr
            assert not any(t in output for t in ["AddressSanitizer", "LeakSanitizer", "runtime error:"]), output
            assert result.returncode == 1, (name, result.returncode, output)
            assert f'{name}:{line}:' in output and ':0:' not in output and message in output, (name, output)
            print('PASS origin:', name, line)
        (work / 'broken-module.claro').write_text('TEACH broken\n    SAY 1 +\nEND\n')
        (work / 'caller.claro').write_text('IMPORT "broken-module.claro" AS problem\nDO problem.broken\n')
        result = subprocess.run([str(exe), 'caller.claro'], cwd=work, capture_output=True, text=True, timeout=10)
        assert result.returncode == 1 and 'broken-module.claro:2:' in result.stderr, result.stderr
        print('PASS origin: imported function')
        (work / 'caught.claro').write_text('TRY\n    DO problem.broken\nCATCH\n    SAY LASTERRORFILE\n    SAY LASTERRORLINE\nENDTRY\n')
        (work / 'caller.claro').write_text('IMPORT "broken-module.claro" AS problem\nTRY\n    DO problem.broken\nCATCH\n    SAY LASTERRORFILE\n    SAY LASTERRORLINE\nENDTRY\n')
        result = subprocess.run([str(exe), 'caller.claro'], cwd=work, capture_output=True, text=True, timeout=10)
        assert result.returncode == 0 and result.stdout.replace('\\', '/').endswith('broken-module.claro\n2\n'), (result.stdout, result.stderr)
        print('PASS origin: caught error metadata')


if __name__ == '__main__':
    main()
