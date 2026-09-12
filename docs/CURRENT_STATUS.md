# Claro v1.18.26 Current Status

This file is the beginner-safe status map for the current package. It separates what is ready to use from what is historical, experimental, or still planned.

## How to read the status labels

- **Stable foundation**: good enough for normal examples and beginner learning.
- **Foundation present**: usable, but still missing important polish or coverage.
- **Experimental/planned**: do not rely on it in beginner lessons yet.
- **Historical**: kept for release history, not current instructions.

## Feature matrix

### Beginner scripting core

Status: **Stable foundation**

Ready now:
- variables with `SET`
- output with `SAY`
- input with `ASK`
- choices with `IF` / `ELSE` / `END`
- loops
- lists and maps
- files, JSON, text helpers, and tested path/collection library helpers
- friendly checking with `claro check`

Good starting docs:
- `QUICK_START.md`
- `FIRST_HOUR.md`
- `CLI.md`
- `SPEC.md`

### Functions

Status: **Stable foundation**

Ready now:
- simple modern form: `TEACH name arg` ... `END`
- compatibility form: `TEACH name TAKES arg` ... `LEARNED`
- calls with `DO` or older `CALL ... WITH`

Good starting docs:
- `SIMPLE_FUNCTIONS.md`
- `README.md`

### Static type safety

Status: **Foundation present**

Ready now:
- typed variables such as `SET score NUMBER 10`
- `TYPE OF` and `CHECK TYPE`
- `CHECK TYPE` rejects unknown expected type names with a beginner-facing list of supported types
- typed list/map checks through `claro typecheck`, including a nested `LIST OF MAP` insertion example
- simple function and object-method return checks with `TEACH name ... RETURNS TYPE`, including learner-facing diagnostics for unknown declared return types, mismatched or not-yet-inferable `RETURN` expressions (including method-specific diagnostics naming the class and method, with modern and compatibility method coverage), empty `RETURN` statements, declarations that contain no `RETURN`, and declarations whose only return is inside an incomplete conditional; `RETURNS` is case-insensitive like other Claro keywords and has positive coverage in both modern and compatibility function forms, including lowercase compatibility declarations and lowercase compatibility method declarations, plus a lowercase compatibility-method mismatch diagnostic; `CHECK TYPE` parameter metadata also informs arithmetic return-expression checking, including method return expressions; positive function-return coverage includes numeric multiplication; NUMBER return diagnostics name a known TEXT operand and arithmetic operation instead of hiding the cause behind a generic mismatch, with focused addition, subtraction, multiplication, and division coverage for functions and methods; typed methods can also return class-declared fields by simple name, with positive and mismatch coverage
- a narrow function/method argument check: `CHECK TYPE parameter IS TYPE` inside a function or simple object method lets `claro typecheck` accept correct checked calls, catch mismatched `DO`, `CALL ... WITH`, `DO object.method ...`, and compatibility `CALL object.method WITH ...` arguments, including checked methods that appear after another method in the same class, report missing checked function and method arguments, report missing unchecked arguments for simple functions and simple object methods in both modern `DO` and compatibility `CALL ... WITH` forms, treat empty compatibility calls such as `CALL greet WITH` and `CALL player.rename WITH` as missing-argument mistakes, catch extra arguments to simple functions and checked methods even when the checked method appears after another method in the same class, catch modern `DO` and compatibility `CALL ... WITH` calls to undeclared simple functions, explain when `DO object.method ...` or compatibility `CALL object.method WITH ...` happens before the object is created with `NEW` even if the method name is also wrong, and catch modern plus compatibility calls to undeclared object methods with a class-specific `TEACH` hint
- a narrow object-field assignment/check-type check for simple `NEW Class object` plus direct `SET object.field value` and `CHECK TYPE object.field IS TYPE` cases when the class declares `HAS field TYPE`; validation now covers correct NUMBER, TEXT, and YESNO direct assignments, explicitly typed field assignments, dedicated positive NUMBER/TEXT/YESNO `CHECK TYPE` metadata fixtures, simple and chained object aliases for both field assignments and `CHECK TYPE` metadata (including a chained TEXT-field check), aliased object-method calls including chained aliases in modern `DO` and compatibility `CALL ... WITH` forms (with a dedicated positive modern `DO` chained-alias fixture), field-to-field, compound arithmetic field expressions, and arithmetic/text expression result types, negative NUMBER/TEXT/YESNO field `CHECK TYPE` metadata mismatches, NUMBER/TEXT/YESNO-expectation unknown-field `CHECK TYPE` diagnostics, missing-object field assignment and `CHECK TYPE` diagnostics, NUMBER/TEXT/YESNO wrong-type diagnostics, field collection when a `HAS` field appears after a simple method, NUMBER/TEXT/YESNO-valued unknown-field diagnostics for direct assignments to undeclared fields including explicitly typed assignments, numeric and text results from simple arithmetic/text expressions in object-field assignments, plus a plain beginner-facing unknown-field diagnostic when the assigned expression type is not inferable yet


Still needed:
- Keep the focused typecheck validator's fixture list complete as new positive and negative examples are added. `claro validate` now executes the complete focused fixture matrix as well, so release validation cannot silently omit a listed typecheck example.
- The expression checker now carries a known TEXT operand through all arithmetic operators so object-field and typed-function-return diagnostics do not hide addition, subtraction, multiplication, or division mistakes; focused numeric-subtraction, numeric-division, and numeric-multiplication positives plus text-operand addition, subtraction, multiplication, and division negatives protect this behavior. Typed-function return diagnostics now also have focused division coverage. Text concatenation into a TEXT field has focused positive fixtures for both operand orders, including concatenation of two TEXT object fields. Each numeric operator names the text operand and explains that it needs NUMBER values.
- Method return validation now has focused positive subtraction and division fixtures alongside the existing arithmetic return coverage, including a compatibility `TAKES` / `LEARNED` division case, so checked NUMBER method parameters and numeric subtraction or division remain accepted by the release validator in both method spellings.
- richer typed function signatures and return values beyond the focused simple function/method `RETURNS TYPE` check
- type checking through branches and loops
- richer object field type checking beyond simple direct assignments
- typed imports/modules

Good starting docs:
- `ADVANCED_STATIC_TYPING.md`
- `V1_14_STATIC_TYPES.md` (feature history plus examples)

### Objects and classes

Status: **Foundation present**

Ready now:
- `CLASS`
- typed `HAS` fields
- `NEW`
- field access such as `player.score`
- simple methods, including static diagnostics for checked method parameters
- direct object-field assignments with a narrow static diagnostic for wrong value types
- object helper commands

Still needed:
- broader object field type checking across aliases, methods, and more complex object flows
- constructor/default-value polish
- clearer object debugging and teaching examples

Good starting docs:
- `V1_15_OBJECTS_CLASSES.md`
- `README.md`

### Package and project workflow

Status: **Foundation present**

Ready now:
- `claro new`
- `claro package init`
- `claro package add/list/remove/doctor/lock`
- local project files such as `claro.project`, `claro.lock`, and `packages/`
- starter projects from `claro new` now use the same manifest-version and lock-version headers as `claro package init`
- the default `make` target builds both `claro` and `claro.exe`, so cross-platform release validators exercise freshly built executables
- project-name safety checks for `claro new`, so unsafe names such as `../bad` are rejected before Claro creates folders
- package-name safety checks when adding packages, including the 64-character package-name limit, when `claro package doctor` audits an existing `claro.project`, when `claro package lock` writes lockfile data, when `claro package list` shows existing packages, when `claro package init` sees unsafe names already present in `claro.project`, when `claro package add` sees unsafe names already present in `claro.project`, when `claro package remove` refreshes the lockfile after an edit, when learners need to remove an unsafe package entry that is already present, when `claro package doctor` verifies lockfile checksums for listed packages, and when `claro package doctor` rejects lockfile package entries that are not listed in `claro.project`
- `claro package doctor` rejects a listed package manifest whose `name:` does not match the package name in `claro.project`
- `claro package doctor` compares the complete manifest `name:` value, so a prefix such as `math-tools-extra` cannot be accepted for package `math-tools`
- `claro package doctor` requires exactly one complete supported package `manifest-version: 1` field; missing, blank, unsupported, or duplicate format fields get a `BAD package manifest version` diagnostic with the file path and a repair hint, rather than calling an existing file missing
- `claro package doctor` compares the complete manifest `checksum:` value, so a valid checksum followed by extra text is rejected
- `claro package doctor` requires the complete supported `manifest-version: 1` value in `claro.project`, so a prefix such as `manifest-version: 10` is rejected
- `claro package doctor` requires the complete supported `version: 1` value in each local package manifest, so a prefix such as `version: 10` is rejected
- `claro package doctor` requires exactly one current `version: v1.18.26` line in `claro.lock`, so stale, missing, blank, or duplicate lockfile release versions are rejected
- `claro package doctor` requires the complete supported `source: local` value in each local package manifest, so a prefix such as `source: local-extra` is rejected
- package project entries must be unique; `claro package doctor`, `list`, `add`, `init`, and `lock` reject duplicate names instead of generating ambiguous package or lockfile data
- lockfile package entries must also be unique; `claro package doctor` reports duplicate lock entries instead of accepting ambiguous package/checksum data
- package manifest `name:` entries must also be unique; `claro package doctor` reports `BAD package manifest name` instead of accepting ambiguous package identity data
- package manifest `checksum:` entries must also be unique; `claro package doctor` reports `BAD package checksum` instead of accepting ambiguous integrity data
- package manifest `version:` entries must also be unique and must contain exactly `1`; `claro package doctor` reports `BAD package version` instead of accepting ambiguous package metadata
- project manifests must contain exactly one `manifest-version: 1` field; duplicate or prefix-matching values are rejected with `BAD project manifest version: expected 1`
- project manifests must contain exactly one non-empty `name:` field; `claro package doctor` reports `BAD project manifest name: expected a non-empty name` when the project identity is missing or blank

Still needed:
- install from local path
- package version constraints
- publish/export format
- remote registry protocol
- checksum/signature verification before downloads

Good starting docs:
- `V1_16_PACKAGES_PROJECTS.md`
- `PACKAGE_REGISTRY.md`

### Networking

Status: **Foundation present**

Ready now:
- beginner HTTP commands
- offline `claro://` URLs for tests and lessons
- `LASTHTTP`
- real `http://` and `https://` through `curl` when available

Still needed:
- web server syntax
- routes
- request/response helpers
- localhost-safe server mode

Good starting docs:
- `V1_17_NETWORKING.md`
- `WEB_SERVER_PLAN.md`

### Concurrency and tasks

Status: **Foundation present**

Ready now:
- deterministic task/concurrency helpers where documented
- beginner-safe direction toward cooperative tasks

Still needed:
- full cooperative scheduler semantics
- cancellation
- timeouts
- message passing
- decision on whether native threads should ever be exposed

Good starting docs:
- `CONCURRENCY.md`

### IDE/editor support

Status: **Foundation present**

Ready now:
- `claro ide`
- metadata JSON
- completion list, including the current typed-language keywords `RETURNS`, `CHECK`, and `TYPE`
- diagnostics helper
- Forgejo/Gitea CI coverage for the current release validation gates (`claro validate`, typecheck diagnostics validation, version convention validation, package security validation, and the CI workflow coverage check); the workflow validator verifies these commands, including its own command, occur in executable `run` steps rather than comments

Still needed:
- syntax highlighting package
- editor extension
- hover help
- go-to-definition
- code actions/fixes
- full LSP server if/when useful

Good starting docs:
- `IDE.md`
- `EDITOR_EXTENSION_PLAN.md`

### Graphics and SDL

Status: **Experimental/planned**

Ready now:
- placeholder/planned graphics documentation
- experimental examples may exist for future SDL work

Not ready in the stable executable:
- real SDL window/drawing support
- beginner game lessons that run everywhere

Good starting docs:
- `GRAPHICS.md`
- `SDL12.md`

## Historical docs

Files named `RC*_NOTES.md`, `RC*_VALIDATION.md`, older `V1_*_VALIDATION.md`, and older release notes are kept for project history. They may mention old version numbers, old planned milestones, or old validation scripts. Use them to understand how Claro evolved; do not treat them as the current beginner path.

## Which docs should a new learner trust first?

For the current v1.18.26 package, read docs in this order:

1. `QUICK_START.md`, `FIRST_HOUR.md`, and `lessons/README.md` for first programs.
2. `README.md` and this file for the current feature map.
3. `ROADMAP.md` for the next v1 work.

Use feature docs with these expectations:

- **Ready for beginner lessons:** `SPEC.md`, `SIMPLE_FUNCTIONS.md`, `ERRORS.md`, `LINTER.md`, `TESTING.md`, `FORMATTER.md`.
- **Foundation present:** `ADVANCED_STATIC_TYPING.md`, `V1_14_STATIC_TYPES.md`, `V1_15_OBJECTS_CLASSES.md`, `V1_16_PACKAGES_PROJECTS.md`, `V1_17_NETWORKING.md`, `CONCURRENCY.md`, `IDE.md`.
- **Plans or experiments:** `PACKAGE_REGISTRY.md`, `WEB_SERVER_PLAN.md`, `EDITOR_EXTENSION_PLAN.md`, `GRAPHICS.md`, `SDL12.md`, `COMPLETE_PLATFORM_ROADMAP.md`, `FUTURE_FEATURES_ROADMAP.md`.

If a doc sounds more ambitious than this status map, treat this file as the current source of truth and update the older doc before teaching from it.
