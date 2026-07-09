# Changelog

## v1.18.26-dev object field CHECK TYPE unknown-field diagnostic

- Added a focused negative `claro typecheck` fixture for direct object-field metadata checks against an undeclared field: `CHECK TYPE player.level IS NUMBER` after `NEW Player player` when the class only declares `HAS score NUMBER`.
- Improved the narrow direct object-field `CHECK TYPE` diagnostic so simple unknown fields name the object class and suggest the matching `HAS level NUMBER` declaration.

## v1.18.26-dev object field CHECK TYPE NUMBER negative validation

- Added a focused negative `claro typecheck` fixture for direct object-field metadata checks: `CHECK TYPE player.score IS TEXT` is rejected after `NEW Player player` and `SET player.score 10` when the class declares `HAS score NUMBER`.
- Wired the fixture into both the typecheck diagnostics validator and `claro validate`; no production typechecker behavior change was needed because the existing direct object-field metadata diagnostic already reports the learner-friendly NUMBER mismatch.

## v1.18.26-dev object field CHECK TYPE YESNO negative validation

- Added a focused negative `claro typecheck` fixture for direct object-field metadata checks: `CHECK TYPE player.ready IS TEXT` is rejected after `NEW Player player` and `SET player.ready YES` when the class declares `HAS ready YESNO`.
- Wired the fixture into both the typecheck diagnostics validator and `claro validate`; no production typechecker behavior change was needed because the existing direct object-field metadata diagnostic already reports the learner-friendly YESNO mismatch.

## v1.18.26-dev object field CHECK TYPE TEXT negative validation

- Added a focused negative `claro typecheck` fixture for direct object-field metadata checks: `CHECK TYPE player.name IS NUMBER` is rejected after `NEW Player player` and `SET player.name "Ada"` when the class declares `HAS name TEXT`.
- Wired the fixture into both the typecheck diagnostics validator and `claro validate`; no production typechecker behavior change was needed because the existing direct object-field metadata diagnostic already reports the learner-friendly mismatch.

## v1.18.26-dev object field CHECK TYPE TEXT/YESNO validation

- Added a focused positive `claro typecheck` fixture for direct object-field metadata checks: `CHECK TYPE player.name IS TEXT` and `CHECK TYPE player.ready IS YESNO` after `NEW Player player` and direct field assignments.
- Wired the fixture into both the typecheck diagnostics validator and `claro validate`; no production typechecker change was needed because the existing direct object-field metadata path already accepts these checks.

## v1.18.26-dev object field unknown YESNO diagnostic validation

- Added a focused negative `claro typecheck` fixture for direct object-field assignment to an undeclared field with a YESNO value: `NEW Player player` followed by `SET player.ready YES` when the class only declares `HAS score NUMBER`.
- Wired the YESNO-valued unknown-field fixture into both the typecheck diagnostics validator and `claro validate`; no production typechecker change was needed because the existing narrow direct object-field diagnostic already reported the learner-friendly message.

## v1.18.26-dev object field unknown TEXT diagnostic validation

- Added a focused negative `claro typecheck` fixture for direct object-field assignment to an undeclared field with a TEXT value: `NEW Player player` followed by `SET player.nickname "Ace"` when the class only declares `HAS score NUMBER`.
- Wired the TEXT-valued unknown-field fixture into both the typecheck diagnostics validator and `claro validate`; no production typechecker change was needed because the existing narrow direct object-field diagnostic already reported the learner-friendly message.

## v1.18.26-dev object field unknown-field diagnostic

- Added a focused negative `claro typecheck` fixture for direct object-field assignment to an undeclared field: `NEW Player player` followed by `SET player.level 3` when the class only declares `HAS score NUMBER`.
- Improved the narrow direct object-field diagnostic so simple unknown fields explain the missing field name and suggest adding a matching `HAS` declaration.

## v1.18.26-dev object field TEXT negative validation

- Added a focused negative `claro typecheck` fixture for direct object-field assignment with a TEXT field: `NEW Player player` followed by `SET player.name 123` when the class declares `HAS name TEXT`.
- Wired the TEXT wrong-type fixture into both the typecheck diagnostics validator and `claro validate`, completing NUMBER/TEXT/YESNO negative coverage for the current narrow direct object-field diagnostic foundation.

## v1.18.26-dev object field YESNO negative validation

- Added a focused negative `claro typecheck` fixture for direct object-field assignment with a YESNO field: `NEW Player player` followed by `SET player.ready "yes"` when the class declares `HAS ready YESNO`.
- Wired the YESNO wrong-type fixture into both the typecheck diagnostics validator and `claro validate`, complementing the existing NUMBER wrong-type diagnostic and NUMBER/TEXT/YESNO positive field fixtures.

## v1.18.26-dev object field YESNO positive validation

- Added a focused positive `claro typecheck` fixture for direct object-field assignment with a YESNO field: `NEW Player player` followed by `SET player.ready YES` when the class declares `HAS ready YESNO`.
- Wired the YESNO object-field fixture into both the typecheck diagnostics validator and `claro validate`, complementing the existing NUMBER/TEXT positive fixtures and wrong-type field diagnostic fixture.

## v1.18.26-dev object field TEXT positive validation

- Added a focused positive `claro typecheck` fixture for direct object-field assignment with a TEXT field: `NEW Player player` followed by `SET player.name "Ada"` when the class declares `HAS name TEXT`.
- Wired the TEXT object-field fixture into both the typecheck diagnostics validator and `claro validate`, complementing the existing NUMBER positive fixture and wrong-type field diagnostic fixture.

## v1.18.26-dev object field positive validation

- Added a focused positive `claro typecheck` fixture for direct object-field assignment: `NEW Player player` followed by `SET player.score 10` when the class declares `HAS score NUMBER`.
- Wired the positive object-field fixture into both the typecheck diagnostics validator and `claro validate`, complementing the existing wrong-type field diagnostic fixture.

## v1.18.26-dev object field assignment diagnostics

- Added a narrow `claro typecheck` diagnostic for direct wrong-type object field assignment after `NEW Class object`, such as `SET player.score "ten"` when `HAS score NUMBER` is known.
- Wired the new negative fixture into typecheck validation while keeping the existing object method positive/negative checks and object-field runtime fixture green.
- Documented the narrow object-field diagnostic scope in beginner-facing status and static typing docs.

## v1.18.26-dev object method parameter diagnostics

- Extended the narrow `CHECK TYPE` argument diagnostic foundation to simple object methods such as `DO player.add "five"` when `player` was created with `NEW Player player`.
- Added focused positive and negative typecheck fixtures for object method parameter diagnostics and wired them into package/typecheck validation.
- Documented the current method-parameter diagnostic behavior in the README, current status, roadmap, and advanced static typing guide.

## v1.18.26-dev multi-parameter function diagnostics

- Extended the function-argument typecheck foundation so both `DO` and compatibility `CALL ... WITH` calls can report checked parameter mismatches.
- Added multi-parameter positive and negative fixtures that verify each wrong argument gets a clear parameter-specific diagnostic.
- Included the function argument fixtures in `claro validate` so package validation covers the diagnostic foundation directly.

## v1.18.26-dev typed function diagnostic foundation

- Added a narrow `claro typecheck` foundation for function argument diagnostics: if a function body declares a parameter expectation with `CHECK TYPE parameter IS TYPE`, calls to that function are checked against the expected argument type.
- Added positive and negative fixtures for the function-argument diagnostic path.
- Extended `tools/validate_typecheck_diagnostics.py` to verify both the new friendly error and a matching successful call.

## v1.18.26-dev learner documentation status cleanup

- Grouped the README documentation map by current feature status so new learners can see what is ready, what is foundation-level, and what is still planned or experimental.
- Added a learner-first trust order to `docs/CURRENT_STATUS.md`.
- Marked `docs/FUTURE_FEATURES_ROADMAP.md` as a historical implementation plan plus remaining ideas, with completed slices separated from still-planned work.

## v1.18.26-dev documentation audit consistency update

- Clarified that `docs/DOCUMENTATION_AUDIT_v1.18.26.md` is a historical snapshot from the first documentation cleanup pass.
- Pointed current readers toward `CURRENT_STATUS.md`, `ROADMAP.md`, and the README documentation map before the original audit problem list.

## v1.18.26-dev type mismatch diagnostics update

- Improved `claro typecheck` messages so scalar, list, map, and `CHECK TYPE` mismatches use one beginner-friendly `Type mismatch` / `Type check failed` style.
- Diagnostics now name the variable/container, the expected type, and the detected value type in plain language.
- Added `tools/validate_typecheck_diagnostics.py` and wired it into `tools/validate_v1_17.py`.
- Strengthened `tools/validate_v1_17.py` so it rebuilds `claro.exe` before validation instead of trusting a stale binary.
- Updated advanced static typing docs with the clearer diagnostic examples.

## v1.18.26-dev package manifest and security foundation update

- Promoted the next development slice to `Claro v1.18.26`.
- Added `manifest-version: 1` to `claro.project` and local `claro.package` files.
- Added deterministic package checksums to local package manifests and `claro.lock`.
- Hardened `claro package doctor` so it validates package manifests and checksums.
- Added `tools/validate_package_security.py` and wired it into `tools/validate_v1_17.py`.

## v1.18.26-dev cooperative concurrency foundation update

- Added beginner-friendly `YIELD` and `TASK STATUS name AS variable` support.
- Documented deterministic cooperative concurrency in `docs/CONCURRENCY.md`.
- Added `tests/40_tasks_status.claro` and `tools/validate_concurrency.py`.
- Improved unfinished block diagnostics so missing task endings say the opened block needs `ENDTASK`.
- Wired concurrency validation into `tools/validate_v1_17.py`.

## v1.18.26-dev LSP diagnostics helper update

- Replaced the old completion-word-only `support/lsp/claro_lsp_stub.py` with a command-based helper.
- Added JSON `metadata`, `completions`, and `diagnostics` helper modes.
- Diagnostics now combine `claro check` and `claro typecheck` output into editor-friendly JSON objects.
- Added `tools/validate_lsp_helper.py` and wired it into `tools/validate_v1_17.py`.
- Expanded `docs/IDE.md` with LSP/helper usage.

## v1.18.26-dev IDE foundation update

- Expanded `claro ide` into valid editor metadata JSON with `file_extensions`, `commands`, `snippets`, and `diagnostics`.
- Added typed container names to IDE metadata, including `LIST OF TEXT` and `MAP OF NUMBER`.
- Added `tools/validate_ide_metadata.py` and wired it into `tools/validate_v1_17.py`.
- Added `docs/IDE.md` for editor integration guidance.

## v1.18.26 development foundation

- Added static checking for typed lists such as `LIST OF TEXT`.
- Added static checking for typed maps such as `MAP OF NUMBER`.
- Added `tests/typecheck_container_good.claro` and `tests/typecheck_container_bad.claro`.
- Added `docs/FUTURE_FEATURES_ROADMAP.md` covering IDE, registry, concurrency, GUI/game, web, and optimization tracks.
- Added `docs/ADVANCED_STATIC_TYPING.md`.

## Claro v1.18.26 - SDL Documentation Correction

- Clarified that SDL 1.2 is not included in the stable executable.
- Removed the misleading `claro package add sdl` README example.
- Marked `examples/experimental_sdl/` as future/experimental examples only.

## Claro v1.18.26 - Stable Test Runner Fix

- Promoted the package to stable `Claro v1.18.26`.
- Fixed Windows `claro test` so it discovers and runs the full golden test suite.
- Normalized runtime error paths to forward slashes for cross-platform expected-output stability.
- Validated version, full tests, package validation, and networking example.

## Claro v1.18.26 - Networking Reliability Release

- Updated visible version string to `Claro v1.18.26`.
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
