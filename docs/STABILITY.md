# Claro Stability and Versioning Policy

Goal: make Claro safe to use for real work by minimizing breaking changes and documenting behavior.

## Status levels

- **Alpha**: features are changing quickly; breaking changes expected.
- **Beta**: features mostly in place; breaking changes avoided; focus on tests + polish.
- **RC (Release Candidate)**: no new features; only bug fixes and documentation.
- **1.0**: stable spec + compatibility promise.

## Compatibility target for 1.0

For **Claro 1.x**:
- programs that follow the spec (docs/SPEC.md) should keep working
- minor updates add features but don’t break existing code
- patch updates only fix bugs

## Deprecation (1.x)
- deprecate in a minor release
- keep working for at least 2 minor releases
- provide a replacement and migration note

## What counts as breaking?
- renaming/removing keywords
- changing operator precedence
- changing LIST indexing (must remain 1-based)
- changing TRY/CATCH semantics
- changing import resolution order
