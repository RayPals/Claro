# Historical Post-1.0 Roadmap

> Historical note: this file records an older planning view from earlier v1 development. For the current roadmap, use `ROADMAP.md`, `CURRENT_STATUS.md`, and `COMPLETE_PLATFORM_ROADMAP.md`.

Claro should continue in the v1 line. Claro v2 should be reserved for a future full rewrite, not normal feature additions.

## What changed since this roadmap was first written

Several items that were once planned for later v1 releases now have foundations in the current package:

- Type safety polish: foundation present through typed variables and `claro typecheck`.
- Objects/classes: foundation present through `CLASS`, `HAS`, `NEW`, fields, and simple methods.
- Package manager: local project/package workflow foundation present.
- Networking: HTTP client foundation present with offline `claro://` URLs.
- Concurrency/tasks: deterministic foundation present.
- IDE support: metadata/helper foundation present.

## Still open

The larger complete-platform work is not finished yet:

- strong function/object/import typing
- package registry and publishing
- beginner web server API
- full cooperative task scheduler
- editor extension or LSP
- real SDL/graphics support in an optional build

Use the current roadmap files for next steps.
