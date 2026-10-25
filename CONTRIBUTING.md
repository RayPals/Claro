# Contributing to Claro

Claro is a learning tool first. Read [`docs/LEARNING_FIRST.md`](docs/LEARNING_FIRST.md)
before proposing learner-facing changes. Keep each change small and predictable,
teach one recommended syntax per concept, preserve supported compatibility
syntax, and prioritize runnable examples and plain-language diagnostics over
feature breadth. Do not claim accessibility validation without testing with
intended learners.

For behavior changes, add a focused regression before implementation and verify
that it fails for the intended reason. Then build and run the affected examples
and the repository validation gates. See [`docs/ROADMAP.md`](docs/ROADMAP.md) for
how the current charter relates to older planning documents.

## Repository layout

- `src/claro.c` — C89 interpreter.
- `lessons/` — ordered beginner lessons.
- `examples/` — programs to try and change.
- `docs/` — learning guides, reference, and historical notes.
- `tests/` — regression fixtures and expected output.
- `tools/` — validation and release helpers.
- `lib/` — existing library helpers.
- `support/` — optional editor support.

## Build and verify

At the beginning of a development/release run, stamp its UTC version once:

```bash
python3 tools/stamp_version.py
make -s all
```

Ordinary rebuilds use `make -s all` without changing the run timestamp.
Validation helpers also require Python 3. Run:

```bash
./claro test
./claro doctor
./claro validate
python3 tools/validate_v1_17.py
```

The last command is the current full validation entry point; its filename is
historical. Use focused sanitizer checks for relevant C runtime changes and
report known failures explicitly.

Execute teaching examples with suitable input and assert their expected output;
syntax checking alone is not enough. Update the relevant guide, rerun checks
after the final edit, and finish with `git diff --check`. Preserve unrelated
local work; exclude generated binaries, caches, and unverified experiments
from commits. See [versioning](docs/VERSIONING.md) for the timestamp convention.


The runtime must remain a single C89 implementation file. The full gate runs
`python3 tools/validate_c89.py` to compile it independently with strict C89 flags
and test formatting, numeric boundaries, and simple functions. Do not introduce
C99 syntax or depend on generated project headers. See [C89 notes](docs/C89.md).


## Learning-first charter

Claro is a learning tool first and a general-purpose language second. Keep the
core small, predictable, and beginner-focused; prioritize executable lessons,
useful diagnostics, and reliability over feature breadth. Teach one recommended
spelling per concept while preserving supported compatibility forms. Do not
claim accessibility validation without feedback from intended learners. The
[learning-first charter](docs/LEARNING_FIRST.md) is the current product guidance.
Older ambitious plans are retained as historical context, not active priorities;
they do not imply that existing features are removed. See the current
[learning-first roadmap](docs/ROADMAP.md).

## Beginner syntax consistency

Follow [the syntax guide](docs/SYNTAX.md) in introductory teaching material.
Keep older spellings in [compatibility reference](docs/COMPATIBILITY.md), not
parallel first-lesson examples. `tools/validate_learning_syntax.py` enforces the
policy and checks actual output; extend its explicit coverage when adding a
lesson or recommended example. Preserve supported parser aliases.
