#!/usr/bin/env python3
"""Compile the single source in isolation and exercise C89 portability boundaries."""
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FLAGS = ['-std=c89', '-pedantic-errors', '-Werror=implicit-function-declaration']


def main():
    cc = shlex.split(os.environ.get('CLARO_CC', 'gcc'))
    with tempfile.TemporaryDirectory(prefix='claro-c89-', dir=os.environ.get('TMPDIR')) as directory:
        work = Path(directory)
        source = work / 'claro.c'
        source.write_bytes((ROOT / 'src/claro.c').read_bytes())
        exe = work / ('claro.exe' if os.name == 'nt' else 'claro')
        subprocess.run(cc + FLAGS + [str(source), '-o', str(exe), '-lm'], check=True)
        unit = work / 'format_probe.c'
        unit.write_text(r'''#define main claro_application_main
#include "claro.c"
#undef main
#include <assert.h>
int main(void)
{
    char guard[8] = "abcdefg";
    char buffer[400];
    char *number;
    int result;
    result=claro_snprintf(guard+1,4,"%s","123456");
    assert(result==6 && guard[0]=='a' && guard[5]=='f');
    assert(strcmp(guard+1,"123")==0);
    assert(claro_snprintf(NULL,0,"%s:%d","hello",-12)==9);
    assert(claro_snprintf(guard,1,"%s","hello")==5 && guard[0]==0);
    assert(claro_snprintf(buffer,sizeof(buffer),"%.*s",3,"abcdef")==3);
    assert(strcmp(buffer,"abc")==0);
    assert(claro_snprintf(buffer,sizeof(buffer),"%.*s",-1,"abc")==3);
    assert(strcmp(buffer,"abc")==0);
    claro_snprintf(buffer,sizeof(buffer),"%08lx %.15g %.0f %%",(unsigned long)42,1.25,3.0);
    assert(strcmp(buffer,"0000002a 1.25 3 %")==0);
    claro_snprintf(buffer,sizeof(buffer),"%.0f",DBL_MAX);
    assert(strlen(buffer)<sizeof(buffer));
    number=num_to_string(-0.0); assert(strcmp(number,"0")==0); free(number);
    return 0;
}
''')
        unit_exe = work / ('format_probe.exe' if os.name == 'nt' else 'format_probe')
        subprocess.run(cc + FLAGS + [str(unit), '-o', str(unit_exe), '-lm'], check=True)
        subprocess.run([str(unit_exe)], cwd=work, check=True)
        invalid = work / 'invalid.c'
        invalid.write_text('int main(void) { int n = 0; n++; int late = 1; return late; }\n')
        bad = subprocess.run(cc + FLAGS + ['-fsyntax-only', str(invalid)], capture_output=True, text=True)
        assert bad.returncode != 0 and 'error' in bad.stderr.lower(), 'C89 compiler gate accepted invalid C99 syntax'
        script = work / 'probe.claro'
        script.write_text('''TEACH add a b
    RETURN a + b
END
DO add 2 3
SAY RESULT
SAY 2147483648
SAY -2147483649
SAY 9007199254740991
SAY -2.5
IMPORT "lib/random.claro" AS random
DO random.seed 1
DO random.int -2147483648 2147483647
SET sample RESULT
IF sample >= -2147483648
    IF sample <= 2147483647
        SAY "range OK"
    END
END
''')
        run = subprocess.run([str(exe), str(script)], cwd=work, text=True, capture_output=True)
        expected = '5\n2147483648\n-2147483649\n9007199254740991\n-2.5\nrange OK\n'
        assert run.returncode == 0 and run.stdout == expected, (run.returncode, run.stdout, run.stderr)
        print('PASS: standalone strict C89 build, rejected C99 fixture, bounded formatting, functions, numbers, extreme random bounds')


if __name__ == '__main__':
    main()
