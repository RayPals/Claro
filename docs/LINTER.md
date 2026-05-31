# Claro Checker

`claro check file.claro` looks for beginner mistakes before running a program.

RC3 catches:

- unknown commands
- command typos such as `PRINT` or `PRNT`
- missing `TO` in `SET`
- missing `AS` in `ASK`, `GET`, and `COUNT`
- missing `ENDIF`, `DONE`, `LEARNED`, `ENDTRY`, and other block endings
- `ELSE` without an `IF`
- `CATCH` without a `TRY`
- common misspelled variables
- variables created by `ASK`, `GET`, `COUNT`, `READ`, `PARSE`, `MAKE`, `FOR`, and `FOR EACH`

The checker is meant to be friendly, not scary. It is still not a complete static analyzer.
