# Claro v1.06.26 Notes

RC6 keeps Claro focused on the original goal: a plain-text scripting language simple enough for learners with learning disabilities, while still growing into a useful tool for real scripts.

## Main theme

**Simple learner scripting.**

RC6 avoids big systems such as SDL, classes, networking, threads, or packages. Those belong later. This release strengthens the small scripting core first.

## Beginner syntax kept simple

Claro now accepts:

```claro
SET name "Jon"
SET name TO "Jon"
SET name to "Jon"
ASK "What is your name?" name
END
```

The older forms still work:

```claro
ASK "What is your name?" AS name
ENDIF
DONE
LEARNED
ENDTRY
```

## Practical scripting additions

RC6 adds command-line arguments, environment lookup, folder/file helpers, command output capture, random numbers, text helpers, and list helpers.

These are meant to make Claro useful for small real scripts while staying readable.
