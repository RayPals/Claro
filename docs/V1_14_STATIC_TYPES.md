# Claro v1.14.26 Static Type Hardening

Claro is still beginner-first. You can keep writing simple scripts like:

```claro
SET name "Jon"
SAY name
```

v1.14.26 adds stronger type tools for learners who are ready for safer, larger programs.

## Simple typed variables

```claro
SET score NUMBER 10
SET name TEXT "Jon"
SET ready YESNO YES
```

Claro remembers the type. If a variable starts as a `NUMBER`, Claro protects it from accidentally becoming text later.

```claro
SET score NUMBER 10
SET score "hello"
```

Friendly error:

```text
score must be NUMBER, but got TEXT.
```

## Type checking before running

Use:

```bash
claro typecheck my_script.claro
```

Example:

```claro
SET score NUMBER 10
SET score "hello"
```

The type checker explains the mistake before the learner runs the program.

## Type helper commands

```claro
TYPE OF score AS kind
SAY kind

CHECK TYPE score IS NUMBER
```

`TYPE OF` stores the visible type name as text.

`CHECK TYPE` stops the script if the value is not the expected type.

## Typed input

```claro
ASK "How old are you?" age NUMBER
ASK "Are you ready?" ready YESNO
```

Claro converts `NUMBER` input into a number and `YESNO` input into `YES` or `NO`.

## Supported simple types

```text
NUMBER
TEXT
YESNO
LIST
MAP
OBJECT
ANY
```

This is not the final complete type system. It is the safe beginner foundation for stronger static checking in later v1 releases.
