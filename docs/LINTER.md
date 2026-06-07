# Claro Checker

`claro check file.claro` looks for beginner mistakes before running a program.

The current checker catches:

- unknown commands
- command typos such as `PRINT` or `PRNT`
- missing required words in older compatibility forms
- missing block endings such as `END`, `ENDIF`, `DONE`, `LEARNED`, and `ENDTRY`
- `ELSE` without an `IF`
- `CATCH` without a `TRY`
- common misspelled variables
- variables created by `ASK`, `GET`, `COUNT`, `READ`, `PARSE`, `MAKE`, `FOR`, and `FOR EACH`

The checker is meant to be friendly, not scary. It is still not a complete static analyzer; use `claro typecheck` for the stronger type-checking pass documented in `ADVANCED_STATIC_TYPING.md`.
