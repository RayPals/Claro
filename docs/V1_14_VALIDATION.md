# Claro v1.14.26 Validation

> Historical note: this file is kept for release history. The current package is Claro v1.18.26; use `CURRENT_STATUS.md`, `ROADMAP.md`, and the current feature docs for up-to-date beginner guidance.


Validated commands:

```bash
gcc -std=c99 src/claro.c -O0 -o claro -lm
./claro --version
./claro test
./claro typecheck tests/typecheck_good.claro
./claro validate
```

Expected version:

```text
Claro v1.14.26
```

Expected test result:

```text
PASS: 0 failure(s)
```

Expected typecheck result for `tests/typecheck_good.claro`:

```text
Type check OK
```

`tests/typecheck_bad.claro` is intentionally bad and should report type errors.
