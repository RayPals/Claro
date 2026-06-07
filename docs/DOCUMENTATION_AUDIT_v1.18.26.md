# Claro v1.18.26 Documentation Audit

Date: 2026-06-05

## Scope

Reviewed the Markdown documentation in the Claro v1.18.26 package:

- `README.md`
- `CHANGELOG.md`
- `lessons/README.md`
- `docs/*.md` — 55 files

Total Markdown files inventoried: 57.

## Overall finding

This audit is a historical snapshot from the first v1.18.26 documentation cleanup pass. At audit time, the docs were useful and broad, but they read like a historical bundle plus a current release bundle. That was okay for internal development, but before a polished public release the documentation needed to be reorganized so beginners saw one clear current path and advanced/history material was separated.

The cleanup notes at the end of this file record the follow-up work that has already been completed. For current learner guidance, use `CURRENT_STATUS.md`, `ROADMAP.md`, and the README documentation map before relying on the problem list below.

## Current strongest documentation

These docs are clear and should remain part of the current user-facing docs:

- `README.md` — good high-level overview of Claro v1.18.26.
- `docs/QUICK_START.md` — important beginner entry point.
- `docs/FIRST_HOUR.md` — useful learner sequence.
- `lessons/README.md` — useful for guided learning.
- `docs/CLI.md` — needed command reference.
- `docs/SPEC.md` — core language reference.
- `docs/ERRORS.md` — important for beginner-friendly diagnostics.
- `docs/FORMATTER.md`
- `docs/LINTER.md`
- `docs/TESTING.md`
- `docs/ADVANCED_STATIC_TYPING.md`
- `docs/IDE.md`
- `docs/CONCURRENCY.md`
- `docs/V1_15_OBJECTS_CLASSES.md`
- `docs/V1_16_PACKAGES_PROJECTS.md`
- `docs/V1_17_NETWORKING.md`
- `docs/SDL12.md`
- `docs/FUTURE_FEATURES_ROADMAP.md`

## Main documentation problems found at audit time

### 1. Old RC language is still mixed with current docs

At audit time, several docs still said or implied that Claro was in an old release-candidate phase:

- `docs/ROADMAP.md` still says:
  - `RC3 - Classroom Readiness`
  - `RC4 - Final Polish`
  - `1.0 - Stable Beginner Release`
- `docs/CLASSROOM_READINESS.md` says `Claro RC3 is suitable... but not final 1.0`.
- `docs/LINTER.md` says `RC3 catches:`.
- `docs/TESTING.md` mentions validating an RC3 package and `validate_rc3.py`.
- `docs/FIRST_HOUR.md` references `RC2` behavior.

Recommendation: keep historical RC docs, but move them under a clear `docs/history/` section or label them as historical at the top.

### 2. Current version story is inconsistent

The package is v1.18.26, but several docs are tied to old versions:

- `docs/STABLE_RELEASE.md` is specifically `Claro v1.10.26 Stable Release`.
- `docs/POST_1_0_ROADMAP.md` lists old future milestones like v1.11.26 through v1.15.26, even though many are already superseded.
- `docs/V1_14_STATIC_TYPES.md`, `docs/V1_15_OBJECTS_CLASSES.md`, etc. are useful but read like version-specific release notes instead of current feature docs.

Recommendation: use current feature docs for beginners and keep old version docs as historical release notes.

### 3. The complete-platform roadmap needs to be promoted

`docs/FUTURE_FEATURES_ROADMAP.md` is the best roadmap for the complete beginner-language goal:

1. Advanced static typing
2. IDE support
3. Concurrency
4. Web programming
5. GUI/game engine
6. Package registry
7. Optimization

But it should now explicitly reflect the user's desired completion targets:

- SDL graphics
- classes/objects
- package manager
- networking
- threads/concurrency
- strong static types
- advanced IDE support

Recommendation: rename or supplement it with `docs/COMPLETE_PLATFORM_ROADMAP.md` and track each feature as Not Started / Foundation / Beta / Stable.

### 4. SDL graphics are correctly marked as not stable, but need a clearer beginner path

`docs/SDL12.md` is honest and says SDL is not included in the current stable executable. That is good.

Current status:

- Placeholder graphics commands exist.
- Real SDL commands are planned/experimental.
- `examples/experimental_sdl/` will fail with current `claro.exe`.

Recommendation: add `docs/GRAPHICS.md` with two tracks:

- Current: beginner-safe placeholder graphics commands.
- Future: optional SDL backend behind a build flag.

### 5. Advanced IDE support has a foundation, not a complete IDE experience

`docs/IDE.md` documents:

- `claro ide`
- metadata JSON
- completion list
- diagnostics helper

Missing for a complete beginner platform:

- syntax highlighting package
- real LSP server or editor extension
- hover help
- go-to definition
- code actions/fixes
- integrated lesson/help flow

Recommendation: add `docs/EDITOR_EXTENSION_PLAN.md` or expand `docs/IDE.md` with a phased roadmap.

### 6. Static types are currently partial

`docs/ADVANCED_STATIC_TYPING.md` clearly documents typed lists and maps checked by `claro typecheck`.

Missing for strong static types:

- function parameter types
- function return types
- object method type checking
- typed imports
- better type checking across branches/loops
- runtime enforcement strategy for containers

Recommendation: add a `Strong Static Types` section to the roadmap and keep the beginner syntax examples very small.

### 7. Concurrency is deterministic foundation, not real threads yet

`docs/CONCURRENCY.md` is clear that Claro has cooperative concurrency foundations and no native threads yet.

Missing for complete platform:

- real cooperative scheduler
- cancellation
- timeouts
- message passing
- eventually optional native threads only if safe

Recommendation: avoid saying "threads" in user-facing docs until semantics are safe; use "tasks" first.

### 8. Package manager foundation exists, but registry is not complete

`docs/V1_16_PACKAGES_PROJECTS.md` documents local package workflow, manifests, lock files, and safety rules.

Missing for full package ecosystem:

- dependency versions
- local install from path
- package publish/export
- remote registry protocol
- signature/checksum verification for downloaded packages

Recommendation: add `docs/PACKAGE_REGISTRY.md` before implementing online downloads.

### 9. Networking foundation exists, web server does not

`docs/V1_17_NETWORKING.md` is good for HTTP client commands and offline `claro://` URLs.

Missing for complete platform:

- beginner web server syntax
- routes
- request/response objects
- local-only safe server mode
- docs and examples for web apps

Recommendation: add `docs/WEB_SERVER_PLAN.md` before implementing sockets.

## Recommended cleanup order from the original audit

1. Add a `docs/CURRENT_STATUS.md` file with a plain feature matrix for v1.18.26.
2. Rewrite `docs/ROADMAP.md` so it no longer describes RC3/RC4 as current.
3. Move or label RC docs as historical.
4. Split docs into beginner-facing vs maintainer/history docs.
5. Add complete-platform roadmap docs for:
   - strong static types
   - IDE/editor support
   - cooperative tasks/threads
   - package registry
   - web server/networking
   - SDL graphics
   - object/class polish
6. Update `README.md` to point beginners only to current docs.

## Feature status summary

- Beginner scripting core: stable foundation.
- Classes/objects: foundation present; needs polish and stronger typing.
- Package manager: local foundation present; registry incomplete.
- Networking: HTTP client foundation present; web server incomplete.
- Threads/concurrency: cooperative foundation present; real scheduling/threads incomplete.
- Strong static types: typed variables and containers foundation present; function/object/import typing incomplete.
- Advanced IDE support: metadata/helper foundation present; full editor/LSP experience incomplete.
- SDL graphics: not included in stable executable; experimental/planned only.

## Bottom line

Documentation is good enough for internal development, but before the complete beginner-language release it needs a current-status pass. The largest documentation problem is not missing docs; it is that historical RC/version docs are mixed into the current package without clear labeling.


## Cleanup pass completed

A documentation cleanup pass was applied after this audit:

- Added `CURRENT_STATUS.md`.
- Rewrote `ROADMAP.md` so old RC3/RC4/1.0 milestones are no longer presented as current.
- Added complete-platform planning docs: `COMPLETE_PLATFORM_ROADMAP.md`, `GRAPHICS.md`, `PACKAGE_REGISTRY.md`, `WEB_SERVER_PLAN.md`, and `EDITOR_EXTENSION_PLAN.md`.
- Updated `README.md` with a beginner-first documentation map.
- Updated stale current-facing docs: `CLASSROOM_READINESS.md`, `LINTER.md`, `TESTING.md`, `FIRST_HOUR.md`, `SPEC.md`, and `POST_1_0_ROADMAP.md`.
- Labeled RC and older validation/release files as historical.
