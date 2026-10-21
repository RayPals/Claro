#!/usr/bin/env python3
"""Keep the introductory learning path consistent and executable."""
import os
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXE = Path(os.environ.get('CLARO_EXE', str(ROOT / ('claro.exe' if os.name == 'nt' else 'claro')))).resolve()
DOCS = ['README.md', 'docs/QUICK_START.md', 'docs/FIRST_HOUR.md', 'docs/SIMPLE_FUNCTIONS.md']
LEGACY = re.compile(r'^\s*(?:CALL\b|LEARNED\b|ENDIF\b|DONE\b|TEACH\b[^\n]*\bTAKES\b|SET\s+\w+\s+TO\b|ASK\s+"(?:[^"\\]|\\.)*"\s+AS\b)', re.MULTILINE)
LESSONS = {
    '01_hello.claro': ('', 'Lesson 1: Hello\nClaro can show messages with SAY.\nHello from Claro!\n'),
    '02_ask_name.claro': ('Ada\n', 'Lesson 2: Ask a question\nWhat is your name?\nHello Ada\n'),
    '03_variables.claro': ('', 'Lesson 3: Variables\nAlex\n5\n'),
    '04_math.claro': ('', 'Lesson 4: Math\n5\n'),
    '05_if_else.claro': ('', 'Lesson 5: Choices\nYou passed!\n'),
    '06_loops.claro': ('', 'Lesson 6: Loops\nPractice\nPractice\nPractice\n1\n2\n3\n'),
    '07_lists.claro': ('', 'Lesson 7: Lists\nmilk\nbread\n'),
    '08_functions.claro': ('', 'Lesson 8: Functions with TEACH\nHello Alex\n'),
    '09_files.claro': ('', 'Lesson 9: Files\nClaro saved this note.\n'),
    '10_final_quiz.claro': ('4\n', 'Lesson 10: Tiny Quiz\nWhat is 2 + 2?\nCorrect!\n'),
}
QUICK = [('', 'Hello!\n'), ('Ada\n', 'What is your name?\nHello Ada\n'),
         ('', '10\n'), ('', 'Good job!\n'), ('', 'Practice\n' * 3),
         ('', 'milk\nbread\n'), ('', 'Hello Alex\n'), ('', 'Hello from Claro\n'),
         ('4\n', 'Tiny Quiz\nWhat is 2 + 2?\nCorrect!\n')]
FIRST_HOUR = [
    ('', 'Hello!\n'),
    ('Ada\n', 'What is your name?\nHello Ada\n'),
    ('', '0\n'),
    ('', '1\n'),
    ('4\n', 'What is 2 + 2?\nCorrect!\n'),
    ('', 'Practice helps\n' * 3),
    ('', 'milk\nbread\n'),
    ('', '5\n'),
    ('', 'Hello\n'),
]


def blocks(path):
    return re.findall(r'```claro\s*\n(.*?)\n```', path.read_text(encoding='utf-8'), re.S)


def check_run(work, label, code, input_text, expected):
    script = work / 'example.claro'
    script.write_text(code + '\n', encoding='utf-8')
    for command in ['check', 'typecheck']:
        checked = subprocess.run([str(EXE), command, str(script)], cwd=work, text=True, capture_output=True, timeout=10)
        assert checked.returncode == 0, (label, command, checked.stdout, checked.stderr)
    result = subprocess.run([str(EXE), str(script)], cwd=work, input=input_text,
                            text=True, capture_output=True, timeout=10)
    assert result.returncode == 0 and result.stdout == expected and not result.stderr, (label, result.returncode, result.stdout, result.stderr)
    print('PASS:', label)


def main():
    actual = {p.name for p in (ROOT / 'lessons').glob('*.claro')}
    assert actual == set(LESSONS), ('Lesson coverage changed; update checker', actual)
    sources = [(name, '\n'.join(blocks(ROOT / name))) for name in DOCS]
    sources += [('lessons/' + name, (ROOT / 'lessons' / name).read_text()) for name in LESSONS]
    examples = json.loads((ROOT / 'tests/learning_examples.json').read_text())
    assert len(examples) == 10, 'Introductory example coverage changed'
    sources += [('examples/' + name, (ROOT / 'examples' / name).read_text()) for name in examples]
    for name, code in sources:
        found = LEGACY.search(code)
        assert not found, f'{name}: introductory syntax must use short ASK/SET, TEACH/DO, and END; found {found.group(0)!r}'
    print('PASS: introductory syntax policy')
    with tempfile.TemporaryDirectory(prefix='claro-learning-', dir=os.environ.get('TMPDIR')) as tmp:
        work = Path(tmp)
        modern_function = blocks(ROOT / 'docs/FIRST_HOUR.md')[7]
        function_script = work / 'modern-function.claro'
        function_script.write_text(modern_function + '\n')
        for command in ['check', 'typecheck']:
            result = subprocess.run([str(EXE), command, str(function_script)], cwd=work, text=True, capture_output=True, timeout=10)
            assert result.returncode == 0, ('modern multi-argument function', command, result.stdout, result.stderr)
            print('PASS: modern function accepted by', command)
        mistakes = [
            ('SET', 'SET\n', 'Try: SET name "Alex"'),
            ('IF', 'IF YES\n    SAY "yes"\n', 'IF block opened here needs END'),
            ('TEACH', 'TEACH greet name\n    SAY name\n', 'TEACH block opened here needs END'),
            ('DO', 'DO 2 TIMES\n    SAY "practice"\n', 'DO block opened here needs END'),
            ('FOR', 'FOR i FROM 1 TO 3\n    SAY i\n', 'FOR block opened here needs END'),
            ('REPEAT', 'REPEAT\n    SAY "practice"\n', 'REPEAT block opened here needs UNTIL'),
        ]
        for label, code, hint in mistakes:
            script = work / 'mistake.claro'
            script.write_text(code)
            result = subprocess.run([str(EXE), 'check', str(script)], cwd=work, text=True, capture_output=True, timeout=10)
            assert result.returncode != 0 and hint in result.stdout, (label, result.returncode, result.stdout)
            assert not re.search(r'needs (?:ENDIF|DONE|LEARNED)|SET name TO', result.stdout), result.stdout
            print('PASS: beginner repair hint for', label)
        first_hour = blocks(ROOT / 'docs/FIRST_HOUR.md')
        assert len(first_hour) == len(FIRST_HOUR), 'First Hour block coverage changed'
        for number, (code, (input_text, expected)) in enumerate(zip(first_hour, FIRST_HOUR), 1):
            check_run(work, f'First Hour block {number}', code, input_text, expected)
        check_run(work, 'First Hour quiz wrong answer', first_hour[4], '3\n',
                  'What is 2 + 2?\nThe answer is 4.\n')
        check_run(work, 'quoted multi-argument function', 'TEACH greet first last\n    RETURN first + last\nEND\nDO greet "Hello " "Ada"\nSAY RESULT', '', 'Hello Ada\n')
        check_run(work, 'bare container constructors', 'SET items LIST\nSET pairs MAP\nSAY items\nSAY pairs', '', '[list]\n[map]\n')
        for name, (input_text, expected) in LESSONS.items():
            check_run(work, name, (ROOT / 'lessons' / name).read_text(), input_text, expected)
        check_run(work, 'quiz wrong answer', (ROOT / 'lessons/10_final_quiz.claro').read_text(), '3\n', 'Lesson 10: Tiny Quiz\nWhat is 2 + 2?\nThe answer is 4.\n')
        quick = blocks(ROOT / 'docs/QUICK_START.md')
        assert len(quick) == len(QUICK), 'Quick Start block coverage changed'
        for number, (code, (input_text, expected)) in enumerate(zip(quick, QUICK), 1):
            check_run(work, f'Quick Start block {number}', code, input_text, expected)
        functions = blocks(ROOT / 'docs/SIMPLE_FUNCTIONS.md')
        assert len(functions) == 1, 'Function guide should teach one initial form'
        check_run(work, 'simple function guide', functions[0], '', 'Hello Jon\n')
        older = blocks(ROOT / 'docs/COMPATIBILITY.md')
        assert len(older) == 1, 'Compatibility guide coverage changed'
        compatibility = older[0]
        check_run(work, 'legacy syntax remains supported', compatibility, '4\n', '5\nNumber?\n8\n8\n')
        for name, (input_text, expected) in examples.items():
            check_run(work, 'examples/' + name, (ROOT / 'examples' / name).read_text(), input_text, expected)
        result = subprocess.run([str(EXE), 'new', 'Starter'], cwd=work, text=True, capture_output=True, timeout=10)
        assert result.returncode == 0, result.stderr
        starter = (work / 'Starter/main.claro').read_text()
        assert not LEGACY.search(starter), 'Generated starter still teaches older syntax'
        check_run(work, 'generated starter', starter, '', 'Welcome to Claro!\nHello Learner\nNice to meet you, Friend\n')
        repl = subprocess.run([str(EXE), 'repl'], cwd=work, input='HELP\nEXIT\n', text=True, capture_output=True, timeout=10)
        assert repl.returncode == 0 and 'SET name "Jon"' in repl.stdout and 'SET name TO' not in repl.stdout, repl.stdout
        metadata = json.loads(subprocess.check_output([str(EXE), 'ide'], cwd=work, text=True))
        snippets = {item['name']: item['body'] for item in metadata['snippets']}
        for name in ['hello', 'if_else', 'function']:
            assert not LEGACY.search(snippets[name]), ('IDE snippet still teaches older syntax', name)
        check_run(work, 'IDE choice snippet', 'SET condition YES\n' + snippets['if_else'], '', 'Yes\n')
        check_run(work, 'IDE function snippet', snippets['function'] + '\nDO name "Ada"', '', 'Ada\n')
        print('PASS: REPL help and beginner IDE snippets')
    print('Learning syntax validation complete')


if __name__ == '__main__':
    main()
