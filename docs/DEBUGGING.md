# Debugging Claro Programs

## 1) Runtime errors (OOPS screen)

When Claro hits a runtime error, it prints a message like:

```
*** OOPS! ***
main.claro:12: Division by zero
Stack trace:
  at updateScore (game.claro:44)
  at main (main.claro:12)
```

### What it means
- `file:line:` is where the error happened.
- The stack trace lists the most recent function calls.

## 2) TRY / CATCH

Errors inside TRY jump to CATCH:

```claro
TRY
    CALL mightFail WITH 1
CATCH
    SAY LASTERROR
    SAY LASTERRORFILE
    SAY LASTERRORLINE
ENDTRY
```

## 3) Static checks

Use:
```bash
claro check yourfile.claro
```

This catches:
- missing ENDIF/DONE/LEARNED/etc.
- unknown keywords
- CALL unknown function / wrong arg counts (semantic checks)

## 4) Formatting

Use:
```bash
claro fmt yourfile.claro --inplace
```

This normalizes indentation and whitespace.
