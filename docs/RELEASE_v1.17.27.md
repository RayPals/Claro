# Claro v1.18.26 Stable Release

> Historical note: this file is kept for release history. The current package is Claro v1.18.26; use `CURRENT_STATUS.md`, `ROADMAP.md`, and the current feature docs for up-to-date beginner guidance.


Claro v1.18.26 is a stability release for the beginner-friendly programming language Claro.

## What changed

- Windows `claro test` now discovers and runs the full golden test suite instead of only three basic tests.
- Runtime error file paths are normalized to forward slashes so expected output is stable across Windows, Linux, and macOS.
- Release/version text was updated for the stable v1.18.26 package.

## Validation completed

Validated on Windows using Zig cc as the C compiler:

```bash
zig cc -std=c99 src/claro.c -O0 -o claro.exe -lm
./claro.exe --version
./claro.exe test
./claro.exe validate
python tools/validate_v1_17.py
```

Results:

- Version: `Claro v1.18.26`
- Golden tests: 44 run, 0 failures
- Full package validation: passed
- Networking example validation: passed

## Release recommendation

This package is ready to share as a stable Windows source/binary release for testing with learners. Keep future changes small and test-first.
