# Claro Roadmap

Current release: **Claro v1.18.26**

Claro is now in the stable v1 development line. Older RC milestones are kept as historical notes in files such as `RC0_NOTES.md`, `RC3_NOTES.md`, and `RC9_VALIDATION.md`; they are not the current roadmap.

## Current direction

Keep Claro beginner-first while growing into a complete small programming platform:

- readable syntax before clever syntax
- friendly diagnostics before advanced compiler features
- safe local/offline defaults before networked behavior
- small features that are easy to teach, test, and document
- normal feature releases inside the v1 line; reserve v2 for a future full rewrite

## v1.18.26 status snapshot

See `CURRENT_STATUS.md` for the detailed feature matrix.

- Beginner scripting core: stable foundation
- Objects/classes: foundation present; needs polish and stronger type checks
- Package workflow: local foundation present; registry and publishing not complete
- Networking: HTTP client foundation present; beginner web server not complete
- Concurrency: deterministic task foundation; native threads not exposed as beginner API
- Static typing: variables and containers foundation; function/object/import typing incomplete
- IDE support: metadata/helper foundation; full editor/LSP experience incomplete
- Graphics/SDL: experimental/planned; not enabled in the stable executable

## Near-term cleanup priorities

1. Keep beginner-facing docs current and separate from historical release notes.
2. Keep examples aligned with the modern simple syntax (`END`, `DO`, short `SET`, short `ASK`) while documenting older compatibility forms separately.
3. Expand validation around typecheck diagnostics and package/networking safety. Current Forgejo/Gitea CI runs the documented release gates (`claro validate`, typecheck diagnostics validation, version convention validation, package security validation, and CI workflow coverage validation). The workflow coverage validator checks executable `run` steps rather than comments and requires its own validator command. Current package safety validation covers safe project creation, rejecting unsafe project names during `claro new`, safe manifest/lockfile creation, rejecting unsafe package names during `package add`, detecting unsafe package names already present in `claro.project` during `package doctor`, refusing to write lockfile data for unsafe package names during `package lock`, making `package list` fail instead of displaying unsafe package entries as normal package names, making `package init` fail instead of reporting the project ready when unsafe package names are already present, making `package add` fail before changing files when unsafe package names are already present, making `package remove` fail instead of reporting success when unsafe package names remain during lockfile refresh, allowing `package remove` to remove an exact unsafe package entry so learners can repair a bad `claro.project`, making `package doctor` reject stale lockfile checksums for listed packages, and making `package doctor` reject lockfile package entries that are not listed in `claro.project`. Current function validation covers correct checked calls, wrong-type arguments, missing checked-argument diagnostics, missing unchecked-argument diagnostics for simple functions in both modern `DO greet` and empty compatibility `CALL greet WITH` forms, extra-argument diagnostics, and beginner-facing unknown-function diagnostics for mistyped modern `DO` and compatibility `CALL ... WITH` calls; current object-method parameter validation covers correct modern `DO object.method ...` and compatibility `CALL object.method WITH ...` checked calls, wrong-type diagnostics for both call forms, checked methods after another method in the same class, missing and extra checked-argument diagnostics including the extra-argument case for a checked method after another method in the same class, missing unchecked-argument diagnostics for simple object methods, missing-object guidance when `DO player.method ...` or compatibility `CALL object.method WITH ...` appears before `NEW` even if the method name is also wrong, and class-specific unknown-method diagnostics for both modern and compatibility calls when a learner calls a method the class does not declare; current object-field validation covers direct NUMBER/TEXT/YESNO field-assignment positives, direct object-field `CHECK TYPE` metadata positives for NUMBER/TEXT/YESNO fields, negative NUMBER/TEXT/YESNO field metadata mismatches, NUMBER/TEXT/YESNO-expectation unknown-field `CHECK TYPE` diagnostics, direct wrong-type field assignment diagnostics, field collection when a `HAS` field appears after a simple method, direct unknown-field diagnostics for NUMBER/TEXT/YESNO values, a beginner-facing fallback for unknown fields assigned from expressions whose type is not inferable yet, and missing-object diagnostics for both `SET object.field value` and `CHECK TYPE object.field IS TYPE` before `NEW`.
3a. Keep package diagnostics actionable: invalid package manifest format fields now name the file and explain how to repair it, separately from an absent manifest. Keep package validation honest by checking that the project manifest has one non-empty project name, that the project and each listed package manifest declare the exact supported manifest version, package version, local source, and expected package name, and that lockfiles declare exactly one current release version.
3b. Keep package security validation in Forgejo/Gitea CI so unsafe names, exact manifest-version/name/version/checksum mismatches, missing manifests, duplicate project manifest versions and packages, duplicate lock packages, duplicate package manifest names, versions, and checksums, and lockfile errors remain release blockers.
4. Add small examples for each foundation feature before adding bigger syntax. The object-field foundation now includes positive and negative validation for field expressions such as `SET player.score player.name`, `SET player.score player.score + 1`, `SET player.name player.score + 1`, explicitly typed field assignments, explicit typed assignments to undeclared fields, simple and chained aliases such as `SET alias player`, `SET backup alias`, followed by `SET backup.score ...` or `CHECK TYPE backup.score IS ...`, chained aliases in object-method calls through both modern `DO` and compatibility `CALL ... WITH` forms (including a dedicated positive modern `DO` fixture), and arithmetic/text expression mismatches; typed containers also accept a map with nested type metadata when it is added to a `LIST OF MAP`; broader alias/control-flow checking remains planned.
5. Keep the focused typecheck validator complete: every `typecheck_*.claro` fixture, including positive fixtures, is now exercised by both the standalone diagnostic validator and `claro validate`.
6. Continue narrowing expression diagnostics: known TEXT operands now remain visible through arithmetic, with focused numeric-subtraction, numeric-division, and numeric-multiplication positives plus text-operand addition, subtraction, multiplication, and division coverage. Typed function returns now include positive subtraction and division examples alongside multiplication. Text concatenation into TEXT fields is covered in both operand orders, including field-to-field concatenation. Each numeric operator names the text operand and explains that it needs NUMBER values. `CHECK TYPE` also rejects misspelled expected type names.
- Keep typed method return examples balanced: numeric addition, subtraction, division, and multiplication now have dedicated positive compatibility `TAKES` / `LEARNED` method fixtures in the focused validator, alongside compatibility addition mismatch coverage and the existing method return mismatch diagnostics.
- Keep IDE metadata aligned with the current beginner syntax: typed-language keywords such as `RETURNS`, `CHECK`, and `TYPE` are now included in the metadata used by editor helpers.
- Keep compatibility-call coverage aligned with modern calls: empty `CALL object.method WITH` forms now have a focused missing-argument diagnostic fixture alongside the modern `DO object.method` case.
Keep declared return types honest: `claro typecheck` now reports friendly diagnostics for unknown declared return types, mismatched, not-yet-inferable, and empty return expressions, declarations with no `RETURN`, and incomplete conditional branches, when a simple function or object method declares `RETURNS TYPE`; the declaration keyword is case-insensitive like other Claro keywords, with positive coverage in modern and compatibility function forms, including lowercase compatibility declarations and lowercase compatibility method declarations, plus a lowercase compatibility-method mismatch fixture. Complete `IF`/`ELSE` return branches, including nested complete conditionals in functions and methods, are accepted, and modern and compatibility function syntax plus compatibility method syntax are covered by focused fixtures. `CHECK TYPE` parameter metadata also informs arithmetic return-expression checking, including object methods; positive numeric multiplication return coverage now sits beside the mismatch fixtures, including a dedicated compatibility-method multiplication success fixture; typed methods can also return class-declared fields by simple name, with positive and mismatch fixtures, and unknown method return expressions now have dedicated modern and compatibility diagnostic fixtures, and NUMBER return expressions with known TEXT arithmetic operands identify the operation and offending operand, including focused addition, subtraction, multiplication, and division coverage for functions and methods. Full path-sensitive analysis across nested conditionals and loops remains planned.

## Complete-platform milestones

### 1. Strong static types

Goal: make larger beginner programs safer without making first scripts harder.

Needed next:
- richer typed function signatures beyond the focused simple `RETURNS TYPE` check
- typed function returns beyond the focused simple function/method `RETURNS TYPE` check
- type checking across branches and loops
- typed imports/modules
- broader object field checking and richer method return typing
- clearer error messages for type mismatches

### 2. Objects and classes polish

Goal: keep object-oriented examples readable enough for beginners.

Needed next:
- constructor-style defaults or beginner-friendly initialization helpers
- richer method return checks beyond the focused simple `RETURNS TYPE` check
- object printing/debugging helpers
- better examples that avoid abstract toy OOP

### 3. Package manager and registry

Goal: make sharing beginner libraries safe and predictable.

Needed next:
- local package install from a folder
- version constraints
- package export/publish format
- lock-file verification
- remote registry design with checksums/signatures before downloads

### 4. Networking and web apps

Goal: allow safe beginner networking and small local web apps.

Needed next:
- beginner web server syntax
- routes
- request/response helpers
- local-only safe default mode
- examples that work offline or on localhost

### 5. Tasks, concurrency, and possible threads

Goal: teach concurrency as safe tasks first, not low-level thread hazards.

Needed next:
- cooperative scheduler semantics
- cancellation
- timeouts
- message passing or channels
- explicit decision on whether native threads are needed later

### 6. IDE/editor support

Goal: give beginners fast feedback in their editor.

Needed next:
- syntax highlighting grammar
- editor extension packaging
- hover/help text
- go-to-definition where practical
- code actions for common mistakes
- LSP server after metadata and diagnostics stabilize

### 7. Graphics and SDL

Goal: make visual/game examples possible without making the portable stable build fragile.

Needed next:
- keep placeholder graphics commands beginner-safe
- define optional SDL build flag/backend
- add graceful errors when graphics are unavailable
- document which examples require experimental builds

## Documentation rule

Every new feature should update three places before it is treated as release-ready:

1. `README.md` or the relevant feature doc for beginner-facing usage
2. `CURRENT_STATUS.md` for status and limitations
3. a validation note or test command showing how it was checked
