# Claro Editor and IDE Support Plan

Current release: **Claro v1.18.26**

Claro has an IDE metadata/helper foundation. It does not yet have a complete editor extension or LSP experience.

## Ready now

- `claro ide`
- metadata JSON
- completion list
- diagnostics helper
- formatter/checker commands that editor tools can call

## Goal

Give beginners fast, friendly feedback while they type, without requiring them to understand compiler internals.

## Suggested phases

1. Syntax highlighting grammar for `.claro` files.
2. Editor snippets for common beginner patterns.
3. On-save `claro check` diagnostics.
4. Formatter integration.
5. Hover help from command metadata.
6. Code actions for common mistakes such as `PRNT` -> `SAY`.
7. LSP server only after the metadata and diagnostics formats are stable.

## Beginner safety rules

- Messages should explain the fix, not just the error.
- Suggestions should prefer modern simple syntax.
- Editor tooling should never run network commands unless the user explicitly asks.
- Lessons should still work from the terminal without an editor extension.

See also:
- `IDE.md`
- `CURRENT_STATUS.md`
- `ROADMAP.md`
