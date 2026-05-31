# Claro v1.10.26 Stable Release

Claro v1.10.26 is the first stable v1 foundation release.

The goal is not to be huge. The goal is to be reliable, readable, and friendly enough for beginner learners while still giving them a real scripting language to grow with.

## Stable core

The v1.10.26 stable core includes:

- `SAY`
- `ASK`
- `SET`
- `IF` / `ELSE` / `END`
- loops
- lists and maps
- simple functions with `TEACH` and `DO`
- files and folders
- JSON
- imports
- `TRY` / `CATCH`
- command-line arguments
- environment lookup
- text helpers
- list helpers
- random numbers
- command output capture
- lessons and examples
- `claro test`
- `claro check`
- `claro fmt`
- `claro repl`
- `claro validate`

## Compatibility

Older RC syntax remains accepted where practical:

- `SET name TO "Jon"`
- `SET name "Jon"`
- `ASK "Name?" AS name`
- `ASK "Name?" name`
- `ENDIF`
- `DONE`
- `LEARNED`
- `END`

## Not finished yet

These are still future-growth areas, not fully finished production systems:

- full SDL game development
- real threaded concurrency
- full networking stack
- online package manager
- strong static type checker
- advanced IDE integration
- large object system

They should grow inside the v1 line over time.
