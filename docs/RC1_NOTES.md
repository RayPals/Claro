# Claro RC1 Notes

Claro RC1 is a learner-testing release candidate for the portable teaching core.

## What RC1 is for

RC1 is meant to be tested by the project maintainer, early learners, and teachers. It is not final 1.0, but it is intended to be buildable, runnable, and consistent enough to evaluate the language design.

## Main changes since RC0

- Version updated to `Claro RC1`.
- The C interpreter now compiles quickly with GCC using the documented command.
- Regression tests pass with `PASS: 0 failure(s)`.
- `claro check` has friendlier beginner diagnostics.
- Checker examples were added under `tests/checker_fixtures/`.

## Recommended command sequence

```bash
gcc -std=c99 src/claro.c -O0 -o claro -lm
./claro --version
./claro test
./claro examples/hello.claro
```

Windows:

```powershell
.\build.ps1
.\claro.exe --version
.\claro.exe test
.\claro.exe examples\hello.claro
```

## What is still not 1.0-ready

- The checker is not yet a full semantic checker.
- Documentation needs a final accessibility pass.
- The printed learner guide should be regenerated from the final syntax.
- SDL/graphics support remains experimental and outside the portable core.
- More negative tests are needed.
