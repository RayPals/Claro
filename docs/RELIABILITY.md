# Reliability checkpoint

Use [release status](RELEASE_STATUS.md) for artifact-specific evidence and
publication state. This page describes tested boundaries, not a universal pass.

The known OBJECT cleanup investigation is resolved for the maintained regression
cases. Historical notes in `HARDENING.md` describe earlier failures, not the current
status of those tested boundaries.

## Repairs and coverage

- Borrowed type/class metadata no longer creates abandoned deep copies.
- Checked assignments, object copies, construction, and OBJECT result temporaries
  release owned values after storage has copied them.
- Function declaration and typechecker parameter arrays, per-file type metadata,
  text transforms, sorting, and REPL teardown have explicit cleanup.
- A lone `!` no longer leaves the tokenizer at the same input position until memory
  is exhausted. It produces a `NOT` repair hint; `!=` remains supported.
- Missing quotes/parentheses/operands and trailing expression tokens are diagnosed.
- Expression recursion and nested control blocks have bounded guardrails. Deep
  block input no longer writes beyond the checker's fixed array.
- Existing function recursion, HTTP response-size, and trusted-command boundaries
  retain their focused checks.

## Reproduce verification

```bash
make -s all
python3 tools/validate_reliability.py
python3 tools/validate_v1_17.py
```

The current reliability runner executes 35 maintained checks and records each exit
status and log in a scratch result directory. It includes the full introductory
learning-path checker and First Hour under ASan/UBSan/LeakSanitizer, with leak
detection enabled. Full release validation invokes this runner; CI has explicit
reliability, single-file C89, and learning-path checks.

The OBJECT regression verifies class name, field count and field content, not a
fictional printed list representation. Five isolated ownership tests separate
metadata, field storage and object construction so one leak cannot hide another.
Malformed-expression and nesting tests check failure diagnostics and valid inputs.

## Diagnostics, JSON and opt-in budgets

Expression errors keep source origins across calls, imports and TRY/CATCH.
The error guide is executable-verified. Malformed JSON now fails instead of
hanging, nesting is bounded, control-character round trips are checked, and
Unicode escapes/surrogate pairs are covered. JSON temporaries, serialization
copies and popped import-stack entries have focused leak-enabled regressions.
The optional step budget counts empty loop entries; READ FILE can enforce a
per-read byte cap. These are not process isolation or wall-clock bounds.

`validate_error_locations.py`, `validate_error_guide.py`, `validate_learner_pilot.py`
and `validate_resource_guards.py` run in the full gate and inside the existing
learning-ownership sanitizer check. The reliability runner still counts 35
maintained top-level checks; subcase coverage has expanded, not been relabeled
as 35 new independent platform tests. Human feedback and native Windows tests
remain separate, blocked acceptance tracks.

## Scope

A passing run establishes the exercised boundaries, not universal leak freedom,
security or correctness for arbitrary programs. POSIX sanitizer coverage does not
establish native Windows behavior. See [runtime limits](RUNTIME_LIMITS.md) for
implemented guards and [portability](PORTABILITY.md) for distribution evidence.
Intentional infinite loops and untrusted-script execution are not made safe by
these checks. Historical beta environment-limit claims are not current guarantees.
