# Claro RC3 Validation

> Historical note: this file is kept for release history. The current package is Claro v1.18.26; use `CURRENT_STATUS.md`, `ROADMAP.md`, and the current feature docs for up-to-date beginner guidance.


Validated commands:

```bash
gcc -std=c99 src/claro.c -O0 -o claro -lm
./claro --version
./claro test
./claro check lessons/01_hello.claro
./claro check lessons/08_functions.claro
./claro check tests/checker_fixtures/bad_unknown_command.claro
```

Expected result:

```text
Claro RC3
PASS: 0 failure(s)
OK
OK
```

The bad checker fixture should exit with a non-zero status and print a helpful diagnostic.
