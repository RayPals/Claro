#!/usr/bin/env python3
"""Execute the pilot's six starter tasks, not simulated human observations."""
from pathlib import Path
import json,os,re,shlex,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
def main():
    tasks=json.loads((ROOT/'tests/learner_pilot.json').read_text())
    blocks=re.findall(r'```claro\n(.*?)```',(ROOT/'docs/LEARNER_PILOT.md').read_text(),re.S)
    assert blocks==[t['code'] for t in tasks]
    with tempfile.TemporaryDirectory(prefix='claro-pilot-',dir=os.environ.get('TMPDIR')) as tmp:
        work=Path(tmp);override=os.environ.get('CLARO_EXE');exe=Path(override).resolve() if override else work/'claro'
        if not override:subprocess.run(shlex.split(os.environ.get('CLARO_CC','gcc'))+['-std=c89','-pedantic-errors',str(ROOT/'src/claro.c'),'-o',str(exe),'-lm'],check=True)
        for i,t in enumerate(tasks):
            p=work/f'task{i}.claro';p.write_text(t['code']);r=subprocess.run([str(exe),p.name],cwd=work,input=t['input'],capture_output=True,text=True,timeout=10)
            assert r.returncode==0 and r.stdout==t['output'],(t['name'],r.stdout,r.stderr)
            print('PASS pilot code:',t['name'])
        assert (work/'practice.txt').read_text()=='My first file'
    print('Human usability/accessibility: NOT TESTED')
if __name__=='__main__':main()
