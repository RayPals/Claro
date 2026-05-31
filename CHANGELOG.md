# Changelog

## Claro v1.17.26 - Networking Reliability Release

- Updated visible version string to `Claro v1.17.26`.
- Hardened the networking foundation while keeping plain-text commands.
- Added offline-safe `claro://` network test URLs so tests and lessons do not need internet access.
- Improved `HTTP GET`:
  - `HTTP GET "claro://hello" AS page`
  - `HTTP GET "claro://hello" AS page STATUS status`
- Added `HTTP STATUS "url" AS code`.
- Added `HTTP SAVE "url" TO "file" AS code`.
- Added `HTTP CHECK "url" AS safe`.
- Added `LASTHTTP` for the latest HTTP status code.
- Added URL safety checks before shelling out to `curl`.
- Added `examples/networking.claro`.
- Added network tests:
  - `tests/38_network_mock.claro`
  - `tests/39_http_save.claro`
- Added docs:
  - `docs/V1_17_NETWORKING.md`
  - `docs/V1_17_VALIDATION.md`
- Added `tools/validate_v1_17.py`.


## Claro v1.15.26 - Objects and Classes Hardening

- Updated visible version string to `Claro v1.15.26`.
- Hardened `CLASS`, `HAS`, `NEW`, and object field behavior.
- Added class method support with simple syntax such as `DO player.show`.
- Added typed field defaults when creating objects.
- Added runtime checks for typed object fields such as `player.score NUMBER`.
- Added object helper commands: `OBJECT CLASS player AS kind` and `OBJECT FIELDS player AS fields`.
- Improved nested block matching so classes can contain methods that end with plain `END`.
- Updated validation to include the object/class example.
- Added object method and object field type regression tests.

## Claro v1.14.26 - Static Type Hardening

- Updated visible version string to `Claro v1.14.26`.
- Added `claro typecheck FILE` for simple static type checking before a script runs.
- Added runtime type helpers: `TYPE OF value AS name` and `CHECK TYPE value IS TYPE`.
- Added typed input forms such as `ASK "How old are you?" age NUMBER`.
- Added simpler object creation form `NEW Player player` while keeping `NEW Player AS player`.
- Added `examples/type_hardening.claro` and `examples/typed_ask.claro`.
- Added typecheck fixtures and validation docs for v1.14.26.

## Claro v1.10.26 - First Stable v1 Foundation

- Promoted Claro from final candidate to the first stable v1 foundation release.
- Updated visible version string to `Claro v1.10.26`.
- Updated package docs from RC9/final-candidate language to stable-release language.
- Kept the beginner-first syntax:
  - `SET name TO "Jon"`
  - `SET name "Jon"`
  - `ASK "What is your name?" name`
  - `END` as a simple block closer.
- Kept compatibility forms such as `ASK ... AS`, `ENDIF`, `DONE`, and `LEARNED`.
- Kept simple functions:
  - `TEACH greet name`
  - `DO greet "Jon"`
- Kept the practical scripting base:
  - command-line arguments
  - environment lookup
  - files and folders
  - text helpers
  - list helpers
  - random numbers
  - command output capture
  - JSON
  - imports
  - TRY/CATCH
- Kept project and tool commands:
  - `claro help`
  - `claro examples`
  - `claro doctor`
  - `claro validate`
  - `claro repl`
  - `claro new MyProject`
  - `claro run`
  - `claro package init|add|list`
  - `claro ide`
- Added stable-release docs:
  - `docs/STABLE_RELEASE.md`
  - `docs/V1_10_VALIDATION.md`
  - `docs/POST_1_0_ROADMAP.md`
- Added `tools/validate_v1_10.py`.
- Validation result: `PASS: 0 failure(s)`.

## Claro v1.09.26 RC9 - Final Candidate

- Updated visible version string to `Claro v1.09.26`.
- Kept normal development in the `v1.xx.yy` version line.
- Added final-candidate validation with `claro validate`.
- Added/kept package health commands:
  - `claro help`
  - `claro examples`
  - `claro doctor`
  - `claro validate`
- Added simple beginner function syntax:
  - `TEACH greet name`
  - `DO greet "Jon"`
- Preserved older function syntax:
  - `TEACH greet TAKES name`
  - `CALL greet WITH "Jon"`
- Added project helper command:
  - `claro new MyProject`
  - `claro run` to run `main.claro`
- Added REPL command:
  - `claro repl`
- Added text polish helpers:
  - `TEXT STARTS ... WITH ... AS`
  - `TEXT ENDS ... WITH ... AS`
  - `TEXT REPLACE ... FROM ... TO ... AS`
- Added examples and tests for simple functions and text polish.
- Added final release checklist and RC9 validation notes.

## Claro v1.06.26 - Simple Learner Scripting Release

- Updated visible version string to `Claro v1.06.26`.
- Added official Claro logo under `assets/Claro_Logo.jpg`.
- Added `docs/BRANDING.md`.
- Added simple beginner syntax support:
  - `SET name "Jon"`
  - `SET name TO "Jon"`
  - `SET name to "Jon"`
  - `ASK "What is your name?" name`
  - `END` as a beginner-friendly block closer.
- Preserved older RC syntax for compatibility.
- Added command-line argument access, environment lookup, folder/file helpers, command output capture, random numbers, text helpers, and list helpers.
- Added tests for simple syntax, `END`, practical files/folders, text helpers, and list helpers.

## Earlier release candidates

Earlier RCs built the current beginner scripting foundation: output/input, variables, math, conditionals, loops, lists, maps, functions, files, JSON, imports, TRY/CATCH, examples, lessons, checker support, formatter support, and test support.
