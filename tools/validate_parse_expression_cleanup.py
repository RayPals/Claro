#!/usr/bin/env python3
"""Bounded malformed-expression regressions; sanitizer runs include leak checks."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DRIVER = r'''#define main claro_cli_main
#include "claro.c"
#undef main
int main(int argc,char **argv)
{
    Runtime rt;
    Value result;
    int status;
    if(argc==3 && strcmp(argv[1],"check")==0) return check_file(argv[2]);
    if(argc!=2) return 2;
    rt_init(&rt);
    result=eval_expr(&rt,argv[1]);
    value_free(result);
    status=rt.error?1:0;
    if(rt.error) fprintf(stderr,"%s\n",rt.err_msg);
    runtime_free(&rt);
    return status;
}
'''
CASES = [
    ('!', 'NOT'),
    ('(1 + 2', 'closing'),
    ('1 +', 'value'),
    ('"unfinished', 'quote'),
    ('1 2', 'Unexpected'),
    ('(' * 600 + '1' + ')' * 600, 'nesting'),
    ('NOT ' * 600 + 'YES', 'nesting'),
]


def limited():
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (128 * 1024 * 1024, 128 * 1024 * 1024))


def main():
    if os.name == 'nt':
        print('SKIP: current parser sanitizer driver requires POSIX')
        return
    with tempfile.TemporaryDirectory(prefix='claro-parse-', dir=os.environ.get('TMPDIR')) as tmp:
        work = Path(tmp)
        (work / 'claro.c').write_bytes((ROOT / 'src/claro.c').read_bytes())
        driver = work / 'parse.c'
        driver.write_text(DRIVER)
        flags = ['gcc', '-std=c89', '-pedantic-errors', '-Werror=implicit-function-declaration', '-O0', '-g']
        plain, sanitized = work / 'parse', work / 'parse-asan'
        subprocess.run(flags + [str(driver), '-o', str(plain), '-lm'], check=True)
        for expression, expected in CASES:
            run = subprocess.run([str(plain), expression], cwd=work, capture_output=True, text=True, timeout=5, preexec_fn=limited)
            assert run.returncode == 1 and expected in run.stderr, (expression[:50], run.returncode, run.stderr[-1000:])
        subprocess.run(flags + ['-fsanitize=address,undefined', str(driver), '-o', str(sanitized), '-lm'], check=True)
        env = dict(os.environ, ASAN_OPTIONS='detect_leaks=1:halt_on_error=1', UBSAN_OPTIONS='halt_on_error=1')
        for expression, expected in CASES:
            run = subprocess.run([str(sanitized), expression], cwd=work, env=env, capture_output=True, text=True, timeout=10)
            assert run.returncode == 1 and expected in run.stderr, (expression[:50], run.returncode, run.stderr[-1000:])
            assert not any(marker in run.stderr for marker in ['AddressSanitizer', 'LeakSanitizer', 'runtime error:']), run.stderr
        for expression, expected in CASES[:1] + CASES[3:4]:
            script = work / 'bad.claro'
            script.write_text('SAY ' + expression + '\n')
            run = subprocess.run([str(sanitized), 'check', str(script)], cwd=work, env=env, capture_output=True, text=True, timeout=10)
            assert run.returncode == 1 and expected in run.stdout, ('check', expression, run.returncode, run.stdout, run.stderr[-1000:])
            assert not run.stderr, run.stderr
        for expression in ['(1 + 2) * 3', '(' * 64 + '1' + ')' * 64, 'NOT ' * 64 + 'YES', '"a" + "b"', '1 != 2']:
            run = subprocess.run([str(sanitized), expression], cwd=work, env=env, capture_output=True, text=True, timeout=10)
            assert run.returncode == 0 and not run.stderr, (expression[:50], run.returncode, run.stderr[-1000:])
    print('PASS: seven malformed expressions and five valid expressions terminate cleanly under ASan/UBSan/LSan')


if __name__ == '__main__':
    main()
