#!/usr/bin/env python3
"""Isolate borrowed metadata and owned object temporaries with ASan/UBSan/LSan."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DRIVER = r'''#define main claro_cli_main
#include "claro.c"
#undef main
#include <assert.h>
int main(int argc,char **argv)
{
    Runtime rt;
    Value obj,text;
    ClassDef *cls;
    int i,which;
    const char *name;
    char typebuf[320];
    assert(argc==2);
    which=atoi(argv[1]);
    rt_init(&rt);
    if(which==1){
        for(i=0;i<2000;i++) assert(rt_set_checked(&rt,"probe",1,"score","NUMBER",v_num(i)));
    } else if(which==2){
        text=v_str("NUMBER"); rt_set(&rt,"__type_score",text); value_free(text);
        for(i=0;i<2000;i++){
            name=runtime_type_for(&rt,"score",typebuf,sizeof(typebuf));
            assert(name && strcmp(name,"NUMBER")==0);
        }
    } else if(which==3){
        obj=v_map(); text=v_str("Person"); map_put(obj.map,"class",text); value_free(text);
        for(i=0;i<2000;i++){
            name=object_class_name(obj); assert(name && strcmp(name,"Person")==0);
        }
        value_free(obj);
    } else if(which==4){
        obj=v_map(); rt_set(&rt,"person",obj); value_free(obj);
        for(i=0;i<2000;i++) assert(rt_set_checked(&rt,"probe",1,"person.score","NUMBER",v_num(i)));
    } else if(which==5){
        cls=add_class(&rt,"Person"); class_add_field(cls,"name","TEXT");
        for(i=0;i<2000;i++) create_object_value(&rt,"probe",1,"Person","person");
    } else return 2;
    assert(!rt.error);
    runtime_free(&rt);
    return 0;
}
'''


def main():
    if os.name == 'nt':
        print('SKIP: LeakSanitizer ownership checks require POSIX')
        return
    failures = []
    with tempfile.TemporaryDirectory(prefix='claro-ownership-', dir=os.environ.get('TMPDIR')) as tmp:
        work = Path(tmp)
        (work / 'claro.c').write_bytes((ROOT / 'src/claro.c').read_bytes())
        driver = work / 'ownership.c'
        driver.write_text(DRIVER)
        binary = work / 'ownership'
        subprocess.run(['gcc', '-std=c89', '-pedantic-errors', '-Werror=implicit-function-declaration', '-g', '-O0', '-fsanitize=address,undefined', str(driver), '-o', str(binary), '-lm'], check=True)
        env = dict(os.environ, ASAN_OPTIONS='detect_leaks=1:halt_on_error=1', UBSAN_OPTIONS='halt_on_error=1')
        for number, name in enumerate(['checked type storage', 'runtime type metadata', 'object class metadata', 'object field copies', 'object construction'], 1):
            run = subprocess.run([str(binary), str(number)], cwd=work, env=env, capture_output=True, text=True, timeout=20)
            if run.returncode or run.stderr:
                failures.append(name)
                print('FAIL:', name, run.stderr[-3500:])
            else:
                print('PASS:', name)
    if failures:
        raise SystemExit('Ownership failures: ' + ', '.join(failures))


if __name__ == '__main__':
    main()
