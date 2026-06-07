# Claro Graphics Status

Current release: **Claro v1.18.26**

Graphics support is intentionally separated from the stable beginner console workflow.

## Beginner-safe track

Use these today:
- console output with `SAY`
- text-based examples
- placeholder graphics docs/examples only when clearly marked experimental

This keeps Claro portable and easy to run on Windows, Linux, macOS, classrooms, and older laptops.

## Experimental SDL track

Real SDL/window support is planned or experimental, not part of the stable `claro.exe` path yet.

Before SDL is treated as beginner-ready, Claro should have:
- an optional build flag/backend
- clear dependency checks
- friendly "graphics unavailable" errors
- tiny drawing examples
- keyboard input examples
- validation that non-graphics Claro still works without SDL installed

See also:
- `SDL12.md`
- `CURRENT_STATUS.md`
- `ROADMAP.md`
