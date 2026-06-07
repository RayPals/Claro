# Claro Performance and Optimization Notes

Current release: **Claro v1.18.26**

Performance work should come after language behavior is stable and measured. Do not optimize blindly.

## Current priority

Claro's current priority is correctness, accessibility, friendly diagnostics, and reliable beginner examples.

## Before optimization work

Add:
- small benchmark scripts
- expected-output checks for benchmark examples
- a timing command or repeatable timing script
- documentation for what is being measured

## Optimization rules

- Keep beginner-visible behavior unchanged.
- Measure before and after every optimization.
- Prefer simple interpreter cleanup before complex compiler architecture.
- Do not add bytecode, JIT, or advanced compiler stages until the v1 semantics are stable.

See also:
- `ROADMAP.md`
- `CURRENT_STATUS.md`
- `FUTURE_FEATURES_ROADMAP.md`
