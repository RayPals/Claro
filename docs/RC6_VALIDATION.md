# Claro v1.06.26 Validation

> Historical note: this file is kept for release history. The current package is Claro v1.18.26; use `CURRENT_STATUS.md`, `ROADMAP.md`, and the current feature docs for up-to-date beginner guidance.


Validated from the source tree with:

```bash
gcc -std=c99 src/claro.c -O0 -o claro -lm
./claro --version
./claro test
./claro check tests/25_simple_syntax.claro
./claro check tests/26_end_alias.claro
./claro check tests/28_text_list_helpers.claro
./claro tests/29_arguments_demo.claro apple banana
```

Expected results:

```text
Claro v1.06.26
PASS: 0 failure(s)
OK
OK
OK
2
apple
2
```
