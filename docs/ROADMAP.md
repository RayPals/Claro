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
3. Expand validation around typecheck diagnostics and package/networking safety.
4. Add small examples for each foundation feature before adding bigger syntax.

## Complete-platform milestones

### 1. Strong static types

Goal: make larger beginner programs safer without making first scripts harder.

Needed next:
- richer typed function signatures
- typed function returns
- type checking across branches and loops
- typed imports/modules
- richer object field checking and method return typing
- clearer error messages for type mismatches

### 2. Objects and classes polish

Goal: keep object-oriented examples readable enough for beginners.

Needed next:
- constructor-style defaults or beginner-friendly initialization helpers
- method return checks
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
