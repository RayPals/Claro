# Claro Complete Platform Roadmap

Current release: **Claro v1.18.26**

This roadmap tracks the larger goal: Claro as a complete beginner-friendly programming platform, not only a toy scripting interpreter.

## Platform pillars

1. Beginner scripting core
2. Strong but optional-feeling static safety
3. Objects and classes for larger programs
4. Local projects and packages
5. Safe networking and local web apps
6. Cooperative tasks/concurrency
7. Editor/IDE help
8. Optional graphics/game support

## Current status summary

See `CURRENT_STATUS.md` for the detailed matrix.

- Stable foundation: beginner scripting core, functions, friendly CLI/checking
- Foundation present: static types, objects/classes, packages, networking, concurrency, IDE metadata
- Experimental/planned: SDL graphics, package registry, web server, full editor extension/LSP

## Completion definition

Claro should not be called a complete beginner platform until:

- each pillar has at least one beginner lesson
- each pillar has a validation command or regression test
- historical docs are clearly separated from current docs
- optional features fail gracefully when dependencies are missing
- README navigation tells learners exactly where to start

## Next documentation work

- Keep this roadmap and `CURRENT_STATUS.md` updated after each feature change.
- Avoid saying experimental features are ready until examples run with the stable executable.
- Prefer small learner examples over large speculative design docs.
