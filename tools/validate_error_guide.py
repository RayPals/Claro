#!/usr/bin/env python3
"""Execute every error-guide failure and repair against the actual interpreter."""
from pathlib import Path
import json, os, re, shlex, subprocess, tempfile
ROOT = Path(__file__).resolve().parents[1]
def main():
    cases = json.loads((ROOT/'tests/error_examples.json').read_text())
    guide = (ROOT/'docs/ERRORS.md').read_text()
    blocks = re.findall(r'```claro\n(.*?)```',guide,re.S)
    expected = [c[k] for c in cases for k in ['code','repair']]
    assert blocks == expected, 'Every error and repair block must match executable coverage'
    with tempfile.TemporaryDirectory(prefix='claro-error-guide-',dir=os.environ.get('TMPDIR')) as tmp:
        work=Path(tmp); override=os.environ.get('CLARO_EXE'); exe=Path(override).resolve() if override else work/'claro'
        if not override:
            subprocess.run(shlex.split(os.environ.get('CLARO_CC','gcc'))+['-std=c89','-pedantic-errors',str(ROOT/'src/claro.c'),'-o',str(exe),'-lm'],check=True)
        for case in cases:
            path=work/case['filename'];path.write_text(case['code'])
            cmd=[str(exe)]+(['check'] if case['mode']=='check' else [])+[path.name]
            r=subprocess.run(cmd,cwd=work,capture_output=True,text=True,timeout=10)
            assert r.returncode==1 and case['diagnostic'] in r.stdout+r.stderr,(case['name'],r.stdout,r.stderr)
            assert case['diagnostic'] in guide
            path.write_text(case['repair']);r=subprocess.run([str(exe),path.name],cwd=work,capture_output=True,text=True,timeout=10)
            assert r.returncode==0 and r.stdout==case['output'],(case['name'],r.stdout,r.stderr)
            print('PASS error guide:',case['name'])
if __name__=='__main__':main()
