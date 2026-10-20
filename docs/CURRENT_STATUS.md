# Claro current status

Development version: **v2026.10.20.223203**

Claro is a **learning tool first**. The development timestamp identifies source;
it does not mean that a release was published or every platform was tested.
See [release status](RELEASE_STATUS.md) for dated, artifact-specific evidence.

## Beginner core — tested learning path

- Input/output, variables, arithmetic, decisions, loops, lists, simple functions,
  and text-file save/load have executable lesson/example coverage.
- Teach short `ASK` and `SET`, `TEACH` with `DO`, and `END` for introductory blocks.
  [Older forms](COMPATIBILITY.md) remain supported, outside the first lessons.
- The [first hour](FIRST_HOUR.md), [ten lessons](../lessons/README.md), generated
  starter and introductory examples are checked for behavior, not just syntax.
- The runtime remains one C89 file: [src/claro.c](../src/claro.c).

This is a foundation for learner trials, not proof of accessibility or classroom
readiness. Intended learners have **not yet validated** accessibility; use the
[classroom pilot checklist](CLASSROOM_READINESS.md) to gather that evidence.

## Reliability and trust boundary

Maintained checks cover ownership cleanup, malformed expressions, nested blocks,
call depth and the learning path under leak-enabled sanitizers. See
[reliability](RELIABILITY.md) for scope and [testing](TESTING.md) to reproduce it.
Earlier failure logs are history, not current unresolved findings.

Claro runs trusted scripts with the user's permissions. It is **not a sandbox**.
Intentional loops can run indefinitely, and global file/JSON/CPU budgets are not
provided. See [actual runtime guards](RUNTIME_LIMITS.md).

## Platforms — do not confuse compilation with OS acceptance

- Strict GCC C89 and extracted source validation have passed on Linux.
- Linux x86-64 static-musl downloads have been tested on the build host.
- MinGW x64 and MSVC600 x86 executables have been built and tested under Wine.
- The dedicated [Windows 98 SE build](WINDOWS98.md) uses `build98.bat`.
- **Native modern Windows and Windows 98 SE execution remain unverified.**
- macOS, ARM, DOS and other untested targets are not implied by C89 compliance.

Exact versions and tested environments are in the [release ledger](RELEASE_STATUS.md).
The [portability guide](PORTABILITY.md) explains the standard archive targets.

## Existing optional features versus plans

Types, objects, local projects/packages, HTTP and editor helpers remain available
in their reference guides; beginners do not need them. Existing deterministic
task helpers are not a claim of native parallel execution or a full scheduler.

Graphics/SDL, a web server, remote registry, richer concurrency and a full editor
integration are plans or experiments, not beginner-ready platform promises.
They are **not active expansion priorities** without a separate request.

## What is next

1. Observe actual beginners and improve instructions/error recovery.
2. Verify the Windows builds on their real target operating systems.
3. Review the accumulated local changes and publish only when authorized.

Follow the [small active roadmap](ROADMAP.md). The
[previous detailed status](history/CURRENT_STATUS_BEFORE_STATUS_CLEANUP.md) and
[hardening log](history/HARDENING_BEFORE_STATUS_CLEANUP.md) preserve older claims,
implementation notes and investigations; they are not current acceptance criteria.
