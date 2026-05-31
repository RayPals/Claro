# Claro v1.09.26 RC9 Notes

RC9 is the final-candidate release before the first stable v1 release.

The goal of RC9 is not to make Claro bigger. The goal is to make the current learner-friendly language easier to test, validate, and ship.

## Added in RC9

```bash
claro validate
```

This runs a final-candidate validation pass over the package:

- package health check
- regression tests
- checker pass over lessons
- checker pass over main examples

## Still beginner-first

Claro continues to prefer plain-text, readable code:

```claro
SET name TO "Jon"
ASK "What is your name?" name
SAY "Hello " + name

TEACH greet person
    SAY "Hi " + person
END

DO greet "Friend"
```

## Compatibility

Older RC forms still work:

```claro
ASK "Name?" AS name
TEACH greet TAKES name
    SAY name
LEARNED
CALL greet WITH "Jon"
```

## After RC9

The next recommended release is `Claro v1.10.26`, the first stable v1 release, after final manual testing on Windows and a clean public package check.
