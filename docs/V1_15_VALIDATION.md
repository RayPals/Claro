# Claro v1.15.26 Validation

> Historical note: this file is kept for release history. The current package is Claro v1.18.26; use `CURRENT_STATUS.md`, `ROADMAP.md`, and the current feature docs for up-to-date beginner guidance.


Validated commands:

```bash
gcc -std=c99 src/claro.c -O0 -o claro -lm
./claro --version
./claro test
./claro validate
```

Expected result:

```text
Claro v1.15.26
PASS: 0 failure(s)
Validation passed. Claro v1.15.26 object/class package is ready for use.
```

Also validated:

```bash
./claro examples/objects_classes.claro
./claro check examples/objects_classes.claro
```
