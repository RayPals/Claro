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
- `CHECK TYPE` gives a direct repair hint when the learner forgets the `IS` keyword, for example `CHECK TYPE score` reports `CHECK TYPE needs IS. Try: CHECK TYPE score IS NUMBER.`
- `CHECK TYPE` gives a direct repair hint when `IS` has no expected type, for example `CHECK TYPE score IS` reports `CHECK TYPE score needs a type after IS. Try: CHECK TYPE score IS NUMBER.`
- `CHECK TYPE` explains when the learner leaves out the expression as well, for example bare `CHECK TYPE` reports `CHECK TYPE needs an expression, IS, and a type. Try: CHECK TYPE score IS NUMBER.`
- typed function and method returns reject simple extra tokens after a return value with a direct repair hint, such as `RETURN amount extra` reporting `Keep only one expression after RETURN.` This is covered for modern functions and both modern and compatibility object methods.
- `CHECK TYPE` explains when `IS` is present but the expression is missing, for example `CHECK TYPE IS NUMBER` reports `CHECK TYPE needs an expression before IS. Try: CHECK TYPE score IS NUMBER.`
- `CHECK TYPE` rejects extra words after a valid expected type with a direct repair hint, so `CHECK TYPE score IS NUMBER TEXT` explains that only one type belongs in the check
- `CHECK TYPE` rejects unknown expected type names with a beginner-facing list of supported types
- typed function return diagnostics also identify an unknown return expression in compatibility `TAKES` / `LEARNED` functions, matching the modern function and object-method guidance
- `TYPE OF` reports a direct repair hint when the learner forgets `AS`, for example `TYPE OF score` suggests `TYPE OF score AS kind`
- bare `TYPE OF` reports that the expression, `AS`, and result name are all required, with a complete repair example
- `TYPE OF` reports a direct repair hint when the learner forgets the expression before `AS`, for example `TYPE OF AS kind` reports `TYPE OF needs an expression before AS. Try: TYPE OF score AS kind.`
- `TYPE OF` prioritizes the missing expression diagnostic even when extra words follow the incomplete form, so `TYPE OF AS kind extra` still points the learner to the missing expression first.
- `TYPE OF` reports a direct repair hint when the learner forgets the result name after `AS`, for example `TYPE OF score AS` reports `TYPE OF needs a result name after AS. Try: TYPE OF score AS kind.`
- A valid `TYPE OF score AS kind` statement has a focused positive typecheck fixture, so the complete form is protected from diagnostic-only regression coverage.
- `TYPE OF` remains case-insensitive like other Claro keywords, with focused positive coverage for lowercase `type of score as kind` syntax.
- `CHECK TYPE` remains case-insensitive like other Claro keywords, with focused positive coverage for lowercase `check type score is number` syntax.
- `TYPE OF` rejects extra words after its result name with a direct repair hint, so `TYPE OF score AS kind extra` explains that only one result name belongs there; typed `TEACH ... RETURNS TYPE` declarations likewise reject extra words after the return type with a direct repair hint
- typed `TEACH ... RETURNS` declarations reject a missing return type with a direct repair hint, such as `Function greet needs a return type after RETURNS. Add a type such as NUMBER.` The same diagnostic names the complete class and method, including compatibility `TAKES` / `LEARNED` methods: `Method Player.score needs a return type after RETURNS. Add a type such as NUMBER.`
- typed list/map checks through `claro typecheck`, including a nested `LIST OF MAP` insertion example
- compatibility `TAKES` / `LEARNED` functions also have focused positive numeric-addition, subtraction, division, and multiplication return fixtures, keeping arithmetic return coverage aligned with modern functions and compatibility methods.
- compatibility `TAKES` / `LEARNED` functions have positive complete-branch return coverage beside the incomplete-branch diagnostic, so older conditional examples are checked for both accepted and rejected paths.
- a narrow function/method argument check: `CHECK TYPE parameter IS TYPE` inside a function or simple object method lets `claro typecheck` accept correct checked calls, catch mismatched `DO`, `CALL ... WITH`, `DO object.method ...`, and compatibility `CALL ... WITH` arguments, including checked methods that appear after another method in the same class, report missing checked function and method arguments, report missing unchecked arguments for simple functions and simple object methods in both modern `DO` and compatibility `CALL ... WITH` forms, treat empty compatibility calls such as `CALL greet WITH` and `CALL player.rename WITH` as missing-argument mistakes, catch extra arguments to simple functions and checked methods even when the checked method appears after another method in the same class, catch modern `DO` and compatibility `CALL ... WITH` calls to undeclared simple functions, explain when `DO object.method ...` or compatibility `CALL ...` happens before the object is created with `NEW` even if the method name is also wrong, and catch modern plus compatibility calls to undeclared object methods with a class-specific `TEACH` hint
- simple function and object-method return checks with `TEACH name ... RETURNS TYPE` now include a compatibility `TAKES` / `LEARNED` function whose conditional returns are incomplete, preserving the same every-path diagnostic as modern functions.
- function and method declarations now reject repeated parameter names with a direct repair hint before calls are checked, including modern and compatibility `TAKES` / `LEARNED` functions and methods; object methods with the same name are also rejected within a class with a rename hint in both modern and compatibility method syntax
- top-level function declarations now reject repeated names with a direct repair hint, so two `TEACH greet` blocks cannot silently compete for one callable function; a missing function name after `TEACH` gets a direct beginner-facing repair hint, and a missing method name inside `CLASS` names the class and gives a method example
- class declarations now reject a missing class name after `CLASS` with a direct beginner-facing repair hint
- class declarations now reject repeated field names within the same class with a direct repair hint before field types are used, so two `HAS score ...` lines cannot silently choose conflicting metadata; different classes may independently use the same field name
- class field declarations now reject missing names such as bare `HAS`, missing types such as `HAS score`, unknown types such as `HAS score BANANA`, and extra tokens such as `HAS score NUMBER TEXT` with the field name, class name, supported type examples, and a repair hint before object-field checks use that metadata
- class declarations now reject repeated class names with a direct repair hint, so two `CLASS Player` blocks cannot silently compete for the same name; extra words after a class name also get a direct repair hint instead of becoming part of the class identity
- object creation now rejects repeated object names with a direct repair hint, so two `NEW Player player` statements cannot silently replace one another during type checking; when a script declares at least one class, a misspelled `NEW` class name gets a direct declaration hint without changing the older permissive no-class form; a missing class name or object name gets a direct example repair; extra words after the object name get a direct repair hint instead of being silently ignored
- a narrow object-field assignment/check-type check for simple `NEW Class object` plus direct `SET object.field value` and `CHECK TYPE object.field IS TYPE` cases when the class declares `HAS field TYPE`; validation now covers correct NUMBER, TEXT, and YESNO direct assignments, dedicated positive and explicitly typed NUMBER/TEXT field assignments, explicitly typed method-body assignments to undeclared fields with a `HAS field TYPE` repair hint in modern and compatibility method syntax, dedicated positive NUMBER/TEXT/YESNO `CHECK TYPE` metadata fixtures, simple and chained object aliases for both field assignments and `CHECK TYPE` metadata (including a chained TEXT-field check), aliased object-method calls including chained aliases in modern `DO` and compatibility `CALL ... WITH` forms (with a dedicated positive modern `DO` chained-alias fixture), field-to-field, compound arithmetic field expressions, and arithmetic/text expression result types, negative NUMBER/TEXT/YESNO field `CHECK TYPE` metadata mismatches, NUMBER/TEXT/YESNO-expectation unknown-field `CHECK TYPE` diagnostics, missing-object field assignment and `CHECK TYPE` diagnostics, NUMBER/TEXT/YESNO wrong-type diagnostics, field collection when a `HAS` field appears after a simple method, NUMBER/TEXT/YESNO-valued unknown-field diagnostics for direct assignments to undeclared fields including explicitly typed assignments, numeric and text results from simple arithmetic/text expressions in object-field assignments, plus method-body field assignment and `CHECK TYPE` diagnostics for NUMBER, TEXT, and YESNO fields in modern and compatibility syntax, including compatibility YESNO `CHECK TYPE` metadata coverage, direct method assignments to undeclared fields now produce a beginner-facing missing-field diagnostic when the assigned expression has a known type, and a plain beginner-facing unknown-field diagnostic when the assigned expression is not inferable yet in both modern and compatibility method syntax; method-body `CHECK TYPE` now reports an unknown field with a repair hint in both method syntaxes, including compatibility `TAKES` / `LEARNED` methods; explicitly typed assignments to declared method fields now validate the class-declared field type instead of trusting only the inline type annotation, so a wrong value such as `SET score TEXT \"oops\"` reports the method and field in the diagnostic.
- inline method-field annotations are checked against the class `HAS` declaration in modern and compatibility methods; conflicting known types and unknown annotation names produce field-specific repair guidance, with positive and negative focused fixtures for both syntaxes.
- Direct object-field validation also has positive coverage for explicit `NUMBER`, `TEXT`, and `YESNO` annotations, such as `SET player.ready YESNO YES`, while the shorter unannotated form remains supported; a conflicting annotation such as `SET player.score TEXT "oops"` now explains the class-declared type and how to repair it.

Still needed:
- Keep the focused typecheck validator's fixture list complete as new positive and negative examples are added. `claro validate` now executes the complete focused fixture matrix as well, so release validation cannot silently omit a listed typecheck example.
- The expression checker now carries a known TEXT operand through all arithmetic operators so object-field and typed-function-return diagnostics do not hide addition, subtraction, multiplication, or division mistakes; focused numeric-subtraction, numeric-division, and numeric-multiplication positives plus text-operand addition, subtraction, multiplication, and division negatives protect this behavior. Typed-function return diagnostics now have focused subtraction and division positives alongside multiplication coverage. Text concatenation into a TEXT field has focused positive fixtures for both operand orders, including concatenation of two TEXT object fields. Each numeric operator names the text operand and explains that it needs NUMBER values.
- Method return validation now has focused positive subtraction and division fixtures alongside the existing arithmetic return coverage, including compatibility `TAKES` / `LEARNED` subtraction and division cases, so checked NUMBER method parameters and numeric subtraction or division remain accepted by the release validator in both method spellings.
- Modern and compatibility `TAKES` / `LEARNED` methods have positive NUMBER, TEXT, and YESNO field-assignment coverage, and modern plus compatibility method-body `CHECK TYPE` metadata now have positive YESNO coverage beside the wrong-value diagnostics.
- Modern method-body TEXT concatenation has positive coverage in both operand orders, such as `SET first first + "!"` and `SET last "Dr. " + last`.
- Compatibility method-body TEXT concatenation has matching positive coverage in both operand orders, so `TAKES` / `LEARNED` methods keep the same beginner-safe field update behavior.
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
- Forgejo/Gitea CI coverage for the current release validation gates (`claro validate`, typecheck diagnostics validation, version convention validation, package security validation, compiler warning validation, and the CI workflow coverage check); the compiler warning validator rebuilds `src/claro.c` and rejects path-truncation warnings, while the workflow validator verifies these commands, including its own command, occur in executable `run` steps rather than comments

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
