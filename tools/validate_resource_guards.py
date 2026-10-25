#!/usr/bin/env python3
"""Exercise bounded malformed JSON, opt-in resource guards and empty loops."""
from pathlib import Path
import json
import os
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix='claro-resource-guards-', dir=os.environ.get('TMPDIR')) as tmp:
        work = Path(tmp)
        override = os.environ.get('CLARO_EXE')
        exe = Path(override).resolve() if override else work / 'claro'
        if not override:
            subprocess.run(shlex.split(os.environ.get('CLARO_CC', 'gcc')) + ['-std=c89', '-pedantic-errors', str(ROOT/'src/claro.c'), '-o', str(exe), '-lm'], check=True)
        def run(name, text, error=None, limits=None):
            (work/name).write_text(text)
            env = dict(os.environ)
            for key in ['CLARO_STEP_LIMIT', 'CLARO_READ_FILE_LIMIT']:
                env.pop(key, None)
            env.update(limits or {})
            try:
                r = subprocess.run([str(exe), name], cwd=work, env=env, capture_output=True, text=True, timeout=8)
            except subprocess.TimeoutExpired:
                raise AssertionError(f'{name}: interpreter failed to terminate') from None
            output = r.stdout+r.stderr
            assert not any(t in output for t in ["AddressSanitizer", "LeakSanitizer", "runtime error:"]), output
            assert r.returncode == (1 if error else 0), (name, r.returncode, output)
            if error:
                assert error in output and ':0:' not in output, (name, output)
            print('PASS:', name)
            return r
        (work/'invalid.json').write_text('[?]')
        run('bad-json.claro', 'READ FILE "invalid.json" AS text\nPARSE JSON text AS data\n', 'JSON')
        for number, text in enumerate(['[1,]', '{"x" 1}', '[1 2]', '"unterminated', '1 extra', '01', '[', '{', '{"x":}', '1e+', '"\\uD800"', '"\\uDC00"', '"\\u12zz"', '"\\u0000"', '"\\q"']):
            (work/'invalid.json').write_text(text)
            run(f'malformed-{number}.claro', 'READ FILE "invalid.json" AS text\nPARSE JSON text AS data\n', 'JSON')
        (work/'nested.json').write_text('['*129+'0'+']'*129)
        run('deep-json.claro','READ FILE "nested.json" AS text\nPARSE JSON text AS data\n','nesting')
        (work/'valid.json').write_text('['*128+'0'+']'*128)
        run('valid-depth.claro','READ FILE "valid.json" AS text\nPARSE JSON text AS data\n')
        (work/'valid.json').write_text('{"text":"\\u0041\\uD83D\\uDE00", "n": -1.25e2, "ok": true}')
        r=run('valid-json.claro','READ FILE "valid.json" AS text\nPARSE JSON text AS data\nGET data KEY "text" AS result\nSAY result\n')
        assert r.stdout=='A😀\n',r.stdout
        original = {"text": "tab\tnewline\ncontrol\x01quote\"", "values": [1, True, None, "A😀"]}
        (work/'valid.json').write_text(json.dumps(original))
        run('roundtrip.claro','READ FILE "valid.json" AS text\nPARSE JSON text AS data\nMAKE JSON data AS encoded\nWRITE FILE "roundtrip.json" WITH encoded\n')
        assert json.loads((work/'roundtrip.json').read_text()) == original
        for name, text in [('empty-repeat.claro','REPEAT\nUNTIL NO\n'),('empty-count.claro','DO 1000000000 TIMES\nEND\n'),('empty-for.claro','FOR i FROM 1 TO 1000000000\nEND\n')]:
            run(name,text,'step limit',{'CLARO_STEP_LIMIT':'20'})
        run('finite.claro','DO 3 TIMES\nSAY "Yes"\nEND\n',limits={'CLARO_STEP_LIMIT':'20'})
        run('missing-until.claro','REPEAT\nSAY "Oops"\n','UNTIL')
        (work/'large.txt').write_bytes(b'x'*1048577)
        run('read-limit.claro','READ FILE "large.txt" AS data\n','file limit',{'CLARO_READ_FILE_LIMIT':'1048576'})
        (work/'boundary.txt').write_bytes(b'x'*32)
        r=run('read-boundary.claro','READ FILE "boundary.txt" AS data\nTEXT LENGTH data AS length\nSAY length\n',limits={'CLARO_READ_FILE_LIMIT':'32'})
        assert r.stdout=='32\n',r.stdout
        run('unlimited-read.claro','READ FILE "large.txt" AS data\n')
        run('caught-budget.claro','TRY\nREPEAT\nUNTIL NO\nCATCH\nSAY "must not escape"\nENDTRY\n','step limit',{'CLARO_STEP_LIMIT':'20'})
        r=run('long-finite.claro','SET i 0\nREPEAT\nSET i i + 1\nUNTIL i = 20000\nSAY i\n',limits={'CLARO_STEP_LIMIT':'200000'})
        assert r.stdout=='20000\n',r.stdout
        run('overflow-limit.claro','SAY "must not execute"\n','CLARO_STEP_LIMIT',{'CLARO_STEP_LIMIT':'999999999999999999999999999999'})
        run('invalid-limit.claro','SAY "must not execute"\n','CLARO_STEP_LIMIT',{'CLARO_STEP_LIMIT':'-1'})


if __name__=='__main__':
    main()
