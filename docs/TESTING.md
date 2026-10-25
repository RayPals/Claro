# Testing Claro

Run from the repository root. Rebuild rather than trusting an old executable.
The developer gate below is exercised on Linux; Windows sanitizer checks may
skip and do not establish native Windows or Win98 SE acceptance.

## Full developer gate

```bash
make -s all
python3 tools/validate_v1_17.py
python3 tools/validate_compiler_warnings.py
python3 tools/validate_ci_workflow.py
python3 tools/validate_documentation_status.py
```

`validate_v1_17.py` is the current full gate despite its historical filename.
It compiles current source and runs strict C89, VC6 source/build settings, golden
fixtures, built-in validation, First Hour, introductory syntax/behavior, editor
metadata, deterministic task helpers, package security, typecheck diagnostics,
reliability, version consistency and documentation-status checks.

The [reliability runner](RELIABILITY.md) includes leak-enabled ASan/UBSan learning
coverage. Read each exit status and skip; a disabled sanitizer or platform skip
is not a pass for that boundary. No test suite proves arbitrary-program safety.

## Small changes and teaching examples

```bash
./claro --version
./claro test
./claro doctor
./claro validate
python3 tools/validate_learning_syntax.py
python3 tools/validate_first_hour.py
```

A successful built-in golden run ends with `PASS: 0 failure(s)`. The learning
checkers execute input-dependent examples with fixed input and compare output;
a syntax-only check is not sufficient. `CLARO_EXE` can select a specific actual
executable through a launcher, including a sanitizer or Wine build.

Run `./claro check lessons/01_hello.claro` for a focused syntax check. Still test
interaction and recovery with learners using the [pilot checklist](CLASSROOM_READINESS.md).

## Target and archive acceptance

Use [distribution verification](PORTABILITY.md) for standard source/Linux x64/
MinGW Windows x64 archives. It rebuilds or executes extracted payloads, checks
manifests, and records exact artifact results. Source builds are not evidence
that a shipped binary is correct.

For [VC6 / Windows 98 SE](WINDOWS98.md), `build98.bat` builds the x86 executable;
run `claro98.exe test` and `claro98.exe validate`. Modern Python developer tooling
is not a Windows 98 prerequisite. The legacy build ZIP uses its own checksum
manifest and report rather than the generic distribution validator.

Wine results must be labeled Wine results. Claim native Windows/Win98 support
only after running the target tests there. [Release status](RELEASE_STATUS.md)
records the dated scope; [the checklist](FINAL_RELEASE_CHECKLIST.md) governs publication.

## New focused checks

```bash
python3 tools/validate_error_locations.py
python3 tools/validate_error_guide.py
python3 tools/validate_learner_pilot.py
python3 tools/validate_resource_guards.py
```

They are also part of the full gate. `validate_learning_ownership.py` runs them
with leak detection enabled, including negative paths. Pilot code checks are
not learner observations. [Native acceptance](NATIVE_WINDOWS_TESTING.md) requires
real target logs; the Wine-rejecting probe prevents silently substituting a
compatibility-layer result. Current [six-track status](SIX_TRACK_STATUS.md)
separates implemented work from blocked human/hosted acceptance.

## Historical tools

Older `validate_rc*.py` and versioned validators remain for history and focused
compatibility checks. They are not alternative current release entry points.
CI coverage is checked from executable `run` steps, not comments. Hosted CI
success must be verified separately from these local commands.
