# Claro v1.17.26

<img src="assets/Claro_Logo.jpg" alt="Claro logo" width="160">

Claro is a small, readable scripting language designed to help beginners — especially learners with learning disabilities — learn programming without being overwhelmed by punctuation-heavy syntax.

Claro stays plain-text first: simple enough to start with `SET name "Jon"`, but able to grow into stronger typed scripts, objects, packages, graphics, networking, and tooling over the v1 line.

## Status

**Current release:** Claro v1.17.26

Validated in this package:

```bash
./claro --version
# Claro v1.17.26

./claro test
# PASS: 0 failure(s)

./claro validate
# Validation passed. Claro v1.17.26 networking reliability is ready for use.
```

## Beginner-first syntax

Claro accepts both the sentence-like style and the shorter simple style:

```claro
SET name TO "Jon"
SET name "Jon"
SET city to "Edmonton"

ASK "What is your name?" name
SAY "Hello " + name

IF name = "Jon"
    SAY "Nice name!"
END
```

Older forms such as `ASK "Name?" AS name`, `ENDIF`, `DONE`, and `LEARNED` still work so older Claro examples do not break.

## Simple functions

```claro
TEACH greet name
    SAY "Hello " + name
END

DO greet "Jon"
```

Older function syntax still works:

```claro
TEACH greet TAKES name
    SAY "Hello " + name
LEARNED

CALL greet WITH "Jon"
```

## Objects and classes

Classes can have typed fields and simple methods.

```claro
CLASS Player
    HAS name TEXT
    HAS score NUMBER

    TEACH show
        SAY name
        SAY score
    END

    TEACH add points
        SET score score + points
    END
END

NEW Player player
SET player.name "Jon"
SET player.score 10

DO player.show
DO player.add 5
SAY player.score
```

Object helper commands:

```claro
OBJECT CLASS player AS kind
OBJECT FIELDS player AS fields
```

## Static type safety

Beginners can still write the simplest form:

```claro
SET name "Jon"
```

When learners are ready, Claro can protect variables with plain-text types:

```claro
SET score NUMBER 10
SET name TEXT "Jon"
SET ready YESNO YES

TYPE OF score AS kind
SAY kind

CHECK TYPE score IS NUMBER
```

## Project and package workflow

v1.17.26 hardens Claro's project/package workflow.

Create a starter project:

```bash
claro new MyProject
cd MyProject
claro run
```

Manage packages:

```bash
claro package init
claro package add text
claro package add sdl
claro package list
claro package remove text
claro package doctor
claro package lock
```

Claro now creates and maintains:

```text
claro.project
claro.lock
packages/
```

Package names are checked so unsafe names such as `../bad` are rejected.


## Networking

v1.17.26 adds safer beginner networking commands with offline `claro://` test URLs.

```claro
HTTP CHECK "claro://hello" AS safe
SAY safe

HTTP GET "claro://hello" AS page STATUS status
SAY page
SAY status

HTTP SAVE "claro://json" TO "network_demo.json" AS saveStatus
SAY saveStatus
```

The latest HTTP status is also stored in `LASTHTTP`. Real `http://` and `https://` requests use `curl` when available, while `claro://` works offline for lessons and tests.

## Useful commands

```bash
claro help
claro --version
claro test
claro validate
claro doctor
claro examples
claro check examples/quiz.claro
claro typecheck examples/type_hardening.claro
claro fmt examples/quiz.claro
claro repl
claro new MyProject
claro run
claro package init
claro package add text
claro package list
claro package doctor
claro ide
```

## Good first scripts

```bash
./claro lessons/01_hello.claro
./claro examples/quiz.claro
./claro examples/simple_functions.claro
./claro examples/objects_classes.claro
./claro examples/text_polish.claro
./claro examples/networking.claro
```

## Release direction

Claro should remain in the `v1.xx.yy` line for normal development. A future Claro v2 should mean a full rewrite years later, not an ordinary feature update.
