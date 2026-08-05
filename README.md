# Claro v1.18.26

<img src="assets/Claro_Logo.jpg" alt="Claro logo" width="160">

Claro is a small, readable scripting language designed to help beginners — especially learners with learning disabilities — learn programming without being overwhelmed by punctuation-heavy syntax.

Claro stays plain-text first: simple enough to start with `SET name "Jon"`, but able to grow into stronger typed scripts, objects, packages, networking, and tooling over the v1 line. Graphics/SDL work is experimental and not enabled in the stable executable.

## Status

**Current release:** Claro v1.18.26

Validated in this package:

```bash
./claro --version
# Claro v1.18.26

./claro test
# PASS: 0 failure(s)

./claro validate
# Validation passed. Claro v1.18.26 networking reliability is ready for use.
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

Advanced container checks are available through `claro typecheck`:

```claro
SET names AS LIST OF TEXT TO LIST
ADD "Ada" TO names

SET scores AS MAP OF NUMBER TO MAP
PUT scores KEY "math" VALUE 98
```

`claro typecheck` also has an early function-argument diagnostic foundation. A function can state a parameter expectation with `CHECK TYPE`, and calls with the wrong value type get a friendly error:

```claro
TEACH square amount
    CHECK TYPE amount IS NUMBER
    SAY amount
END

DO square "oops"
```

```text
Type mismatch for function square: parameter amount needs NUMBER, but this argument looks like TEXT.
```

For functions with more than one checked parameter, Claro reports each mismatched argument with the parameter name:

```claro
TEACH label TAKES name, age
    CHECK TYPE name IS TEXT
    CHECK TYPE age IS NUMBER
END

CALL label WITH 7, "old"
```

The same narrow diagnostic foundation now covers simple object method calls when the object was created with `NEW` and the method body uses `CHECK TYPE` for a parameter. Correct calls such as `DO player.add 5` are covered by validation, and wrong-type calls get a focused learner-facing error:

```claro
CLASS Player
    HAS score NUMBER

    TEACH add points
        CHECK TYPE points IS NUMBER
        SET score score + points
    END
END

NEW Player player
DO player.add "five"
```

```text
Type mismatch for method Player.add: parameter points needs NUMBER, but this argument looks like TEXT.
```

For simple object fields created with `NEW Class name`, `claro typecheck` also catches direct wrong-type field assignments such as `SET player.score "ten"` when the class says `HAS score NUMBER`:

```text
Type mismatch for field player.score: expected NUMBER, but this value looks like TEXT.
```

It also catches direct assignments to undeclared fields and suggests the matching `HAS` line:

```text
Object Player has no field level. Check the field name or add HAS level NUMBER to the class.
```

TEXT-valued and YESNO-valued field-name mistakes are validated too:

```text
Object Player has no field nickname. Check the field name or add HAS nickname TEXT to the class.
Object Player has no field ready. Check the field name or add HAS ready YESNO to the class.
```

Direct object-field `CHECK TYPE` metadata mismatches are validated for NUMBER, TEXT, and YESNO fields too. For example, after `HAS ready YESNO` and `SET player.ready YES`, `CHECK TYPE player.ready IS TEXT` reports:

```text
Type check failed: expected TEXT, but player.ready looks like YESNO.
```

If `CHECK TYPE` names an undeclared field, Claro now gives the same class-and-field hint as direct field assignment. For example, `CHECK TYPE player.level IS NUMBER` after `NEW Player player` reports:

```text
Object Player has no field level. Check the field name or add HAS level NUMBER to the class.
```

TEXT expectations are validated with the same pattern, for example `CHECK TYPE player.nickname IS TEXT` reports:

```text
Object Player has no field nickname. Check the field name or add HAS nickname TEXT to the class.
```

YESNO expectations are validated too; `CHECK TYPE player.enabled IS YESNO` reports:

```text
Object Player has no field enabled. Check the field name or add HAS enabled YESNO to the class.
```

If a learner checks a field before creating the object with `NEW`, `claro typecheck` points to the missing object setup:

```text
Object player is not known yet. Create it with NEW ClassName player before checking player.score.
```

## Project and package workflow

v1.18.26 hardens Claro's project/package workflow.

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


## Standard-library path and collection helpers

Claro includes tested, namespaced helpers for everyday programs:

```claro
IMPORT "lib/path.claro" AS path
IMPORT "lib/collections.claro" AS collections

CALL path.join WITH "notes", "today.txt"
SAY RESULT

SET names AS LIST OF TEXT TO LIST
ADD "Ada" TO names
ADD "Grace" TO names
CALL collections.join WITH names, " and "
SAY RESULT
```

The `path` module includes `join`, `basename`, `dirname`, `ext`, `stem`, and `absolute`. The `collections` module includes list length/search/join/reverse helpers and map key/value/default-access helpers. See `docs/STDLIB.md` for the complete, current API.

## Networking

v1.18.26 adds safer beginner networking commands with offline `claro://` test URLs.

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

## Documentation map

If you are new to Claro, start here:

1. `docs/QUICK_START.md`
2. `docs/FIRST_HOUR.md`
3. `lessons/README.md`
4. `docs/CLI.md`
5. `docs/CURRENT_STATUS.md`

Feature references by current status:

- **Ready for beginner lessons:** language reference (`docs/SPEC.md`), friendly errors/checking (`docs/ERRORS.md`, `docs/LINTER.md`, `docs/TESTING.md`), formatter (`docs/FORMATTER.md`), and simple functions (`docs/SIMPLE_FUNCTIONS.md`).
- **Foundation present, still being polished:** static typing (`docs/ADVANCED_STATIC_TYPING.md`), objects/classes (`docs/V1_15_OBJECTS_CLASSES.md`), local projects/packages (`docs/V1_16_PACKAGES_PROJECTS.md`), HTTP client networking (`docs/V1_17_NETWORKING.md`), cooperative tasks (`docs/CONCURRENCY.md`), and IDE metadata/helper support (`docs/IDE.md`).
- **Planned or experimental, not stable beginner features yet:** remote package registry (`docs/PACKAGE_REGISTRY.md`), web server API (`docs/WEB_SERVER_PLAN.md`), full editor extension/LSP (`docs/EDITOR_EXTENSION_PLAN.md`), and real SDL graphics (`docs/GRAPHICS.md`, `docs/SDL12.md`).
- **Roadmaps:** `docs/ROADMAP.md` for the current v1 direction and `docs/COMPLETE_PLATFORM_ROADMAP.md` for the larger platform goal.

Historical release notes and validation logs are kept in files such as `docs/RC*_NOTES.md`, `docs/RC*_VALIDATION.md`, and older `docs/V1_*_VALIDATION.md`. They are useful for project history, but they are not the beginner starting path.

## Release direction

Claro should remain in the `v1.xx.yy` line for normal development. A future Claro v2 should mean a full rewrite years later, not an ordinary feature update.
