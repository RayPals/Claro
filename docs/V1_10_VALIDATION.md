# Claro v1.10.26 Validation

> Historical note: this file is kept for release history. The current package is Claro v1.18.26; use `CURRENT_STATUS.md`, `ROADMAP.md`, and the current feature docs for up-to-date beginner guidance.


Validated from a clean package with:

```bash
gcc -std=c99 src/claro.c -O0 -o claro -lm
./claro --version
./claro test
./claro validate
```

Expected result:

```text
Claro v1.10.26
PASS: 0 failure(s)
Validation passed. Claro v1.10.26 stable package is ready for use.
```

Also validate a few first scripts:

```bash
./claro lessons/01_hello.claro
./claro examples/quiz.claro
./claro examples/simple_functions.claro
./claro examples/text_polish.claro
```
