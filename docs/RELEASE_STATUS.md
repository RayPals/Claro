# Release status and verified builds

## Publication snapshot — 2026-10-20

The accumulated learning-syntax, reliability, distribution and Windows 98 build
changes are **not published** to Gitea `main` in the check performed for this cleanup.
The local HEAD and a read-only `git ls-remote --heads gitea main` both returned:

```text
8ea2f772cd8552d4651bf551bed9a8a03b4ed2a9
```

That commit is the earlier single-file C89 refactor, not the current dirty tree.
This is a dated branch check, not a live remote badge. Hosted tags, release pages
and hosted CI were not audited by that check; no new hosted release or CI pass
is claimed. Refresh the remote state before any authorized publication.

A development timestamp is not a stable-release designation. Use
[current status](CURRENT_STATUS.md) for the learning scope and
[the release checklist](FINAL_RELEASE_CHECKLIST.md) before publishing.

## Immutable artifact checkpoints

These are verified build artifacts previously delivered for testing, **not a
claim of a hosted release**. Their reports/logs were delivered outside Git.
The filenames and SHA-256 values identify the exact archives; they are not
public download URLs or digital signatures. Do not substitute a newly stamped
binary for one of these archived checkpoints.

### Source — v2026.10.20.184951

- Archive: `Claro-v2026.10.20.184951-source.zip`.
- SHA-256: `3531d2fc82e2d008fee8affc82864a56e7d8f5c917ef5556f5cfac0b3b828d38`.
- Extracted-source verification on Linux: isolated strict C89 compilation, make,
  golden/learning/First Hour checks and the full release gate, including 35
  maintained reliability checks. This is not proof for an arbitrary OS/compiler.
- Report: `source-verification.json`.

### Linux x86-64 — v2026.10.20.180131

- Archive: `Claro-v2026.10.20.180131-linux-x86_64.zip`.
- SHA-256: `9f53394643e1bd9360940ed90e77af89a43ad160f976bf12fabe500bda0d16e6`.
- Static-musl ELF; extracted payload passed all 51 golden fixtures, learning
  checks, nine First Hour examples, built-in validation and standalone checks
  on the Linux x86-64 build host. Other distributions/kernels/CPUs are unverified.
- Report: `final-linux-verification.json`.

### MinGW Windows x86-64 — v2026.10.20.180131

- Archive: `Claro-v2026.10.20.180131-windows-x86_64.zip`.
- SHA-256: `59b452ccfe96848fa45db3915aa7d03610cc5fba35cf6a294718d1cff67c6ec0`.
- Genuine PE x64, 16 MiB stack; extracted executable passed all 51 golden fixtures,
  learning checks, nine First Hour examples and built-in/standalone checks under
  **Wine on Linux**. Native Windows execution remains **unverified**.
- Report: `final-windows-verification.json`.

### MSVC600 / Windows 98 SE compilation — v2026.10.20.184951

- Archive: `Claro-v2026.10.20.184951-Win98SE-VC6-build.zip`.
- SHA-256: `914d14373ec6f202fea4ff74ed0ffbde20e0ff3a9d708b9a2ac72ddf37c488cd`.
- Actual Microsoft compiler **12.00.8804** compiled/linked through `build98.bat`
  without an `intptr_t` alias flag. PE32 x86, subsystem 4.10, static VC6 CRT,
  16 MiB stack reserve, only KERNEL32.dll imported.
- The executable passed all 51 golden fixtures, the introductory checker, nine
  First Hour examples and built-in validation under **Wine**. The final ZIP was
  re-extracted, its manifest/source/binary hashes checked, and its golden suite,
  doctor, version and built-in validation rerun.
- **Actual Windows 98 SE execution remains unverified.** PE headers and Wine
  behavior do not establish the real OS loader, CRT, console or filesystem behavior.
- Reports: `WINDOWS98_BUILD_REPORT.md` and `package-verification.json`.
- Frozen source SHA-256: `b3efcf9f3d60627a2b98159d3638c3b3639cb329998017c163d815046c32d1bf`.

## Reproduce or extend evidence

[Testing](TESTING.md), [portability](PORTABILITY.md) and the
[Windows 98 build guide](WINDOWS98.md) describe the commands and boundaries.
The standard archive helper covers source/Linux x64/MinGW x64. The separate VC6
build ZIP uses its own checksum manifest and report, not the generic validator.

macOS, ARM, native modern Windows, Windows 98 SE/XP, DOS and other targets need
separate execution evidence. Accessibility needs intended-learner feedback;
automated tests alone do not establish it. Claro is trusted code, not a sandbox.
