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
- typed list/map checks through `claro typecheck`
- a narrow function/method argument check: `CHECK TYPE parameter IS TYPE` inside a function or simple object method lets `claro typecheck` accept correct checked calls and catch mismatched `DO`, `CALL ... WITH`, and `DO object.method ...` arguments
- a narrow object-field assignment/check-type check for simple `NEW Class object` plus direct `SET object.field value` and `CHECK TYPE object.field IS TYPE` cases when the class declares `HAS field TYPE`; validation now covers correct NUMBER, TEXT, and YESNO direct assignments, direct `CHECK TYPE` metadata acceptance for NUMBER/TEXT/YESNO fields, negative NUMBER/TEXT/YESNO field `CHECK TYPE` metadata mismatches, NUMBER/TEXT/YESNO-expectation unknown-field `CHECK TYPE` diagnostics, NUMBER/TEXT/YESNO wrong-type diagnostics, plus NUMBER/TEXT/YESNO-valued unknown-field diagnostics for direct assignments to undeclared fields

Still needed:
- richer typed function signatures and return values
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
- package-name safety checks

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
- completion list
- diagnostics helper

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
