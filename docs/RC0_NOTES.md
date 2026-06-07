# Claro RC0 Notes

> Historical note: this file is kept for release history. The current package is Claro v1.18.26; use `CURRENT_STATUS.md`, `ROADMAP.md`, and the current feature docs for up-to-date beginner guidance.


Claro RC0 is a stabilization pass for the educational scripting-language core.

## Goal

The goal of RC0 is to make Claro feel safe to try with learners:

- the interpreter builds from source
- the examples use one consistent style
- the regression tests pass
- docs and version labels no longer describe the project as a random beta snapshot
- older experimental pieces are clearly separated from the portable core

## What changed

The uploaded beta source had many build blockers and internal inconsistencies. RC0 replaces that broken interpreter snapshot with a compact C99 interpreter that focuses on the language features needed for a first public testing release.

Validated features include:

- output and input with `SAY` and `ASK`
- variables and expressions
- functions using `TEACH`, `CALL`, `RETURN`, and `LEARNED`
- conditionals and loops
- lists and maps
- map/list iteration
- file commands
- JSON parse/make/pretty output
- imports, namespaces, and exports
- error handling with `TRY`, `CATCH`, `RAISE`, and `LASTERROR`
- text, math, random, and CSV stdlib-style imports
- formatter/check/test CLI commands

## Test result

On the RC0 staging build:

```text
PASS: 0 failure(s)
```

This covers all `tests/*.claro` files with matching `.out` expected-output files.

## Accessibility direction

Claro should remain predictable and visually calm:

- plain-English commands
- indentation-based teaching style
- minimal symbolic punctuation
- short examples
- clear error text
- no mandatory advanced setup for early lessons

Future documentation should continue using print-friendly layouts, larger examples, and OpenDyslexic/OpenDyslexia-friendly exports where possible.

## Known limitations

- RC0 is not final 1.0.
- SDL 1.2 game examples from older betas are preserved in `examples/experimental_sdl/`, but SDL is not part of the portable RC0 core.
- The checker is intentionally lightweight.
- Runtime safety limits and richer semantic diagnostics should be strengthened before final 1.0.
- The C interpreter favors readability and portability over speed.

## Recommended next milestone

For RC1:

1. add more beginner lessons and teacher notes
2. expand semantic checking for friendlier mistakes
3. add a print-friendly quick-start PDF generated from the updated syntax
4. add Windows CI-style build/test instructions
5. decide whether SDL/game support belongs in core or a separate optional build
