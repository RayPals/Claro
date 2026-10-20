#!/usr/bin/env python3
"""Deep control blocks must produce diagnostics, not checker/CPU stack overflows."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    if os.name == 'nt':
        print('SKIP: current nesting sanitizer build requires POSIX')
        return
    with tempfile.TemporaryDirectory(prefix='claro-nesting-', dir=os.environ.get('TMPDIR')) as tmp:
        work = Path(tmp)
        exe = work / 'claro-asan'
        subprocess.run(['gcc', '-std=c89', '-pedantic-errors', '-Werror=implicit-function-declaration', '-O0', '-g', '-fsanitize=address,undefined', str(ROOT / 'src/claro.c'), '-o', str(exe), '-lm'], check=True)
        env = dict(os.environ, ASAN_OPTIONS='detect_leaks=1:halt_on_error=1', UBSAN_OPTIONS='halt_on_error=1')
        for depth, expected in [(64, 0), (600, 1)]:
            script = work / 'nested.claro'
            script.write_text('IF YES\n' * depth + 'SAY "OK"\n' + 'END\n' * depth)
            for command in ['check', 'run']:
                run = subprocess.run([str(exe), command, str(script)], cwd=work, env=env, capture_output=True, text=True, timeout=15)
                combined = run.stdout + run.stderr
                assert run.returncode == expected, (depth, command, run.returncode, combined[-2000:])
                assert not any(s in combined for s in ['AddressSanitizer', 'LeakSanitizer', 'runtime error:']), combined
                if expected:
                    assert 'block nesting' in combined.lower(), (command, combined)
                else:
                    assert run.stdout == ('OK\n' if command == 'run' else 'OK\n'), (command, combined)
                print('PASS:', command, 'block depth', depth)


if __name__ == '__main__':
    main()
