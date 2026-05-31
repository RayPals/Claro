# Claro v1.15.26 Objects and Classes

Claro objects are meant to stay plain and readable. Learners can start with variables and functions, then grow into classes when they are ready.

## Basic class

```claro
CLASS Player
    HAS name TEXT
    HAS score NUMBER
END

NEW Player player
SET player.name "Jon"
SET player.score 10

SAY player.name
SAY player.score
```

## Methods

Methods are taught with the same `TEACH` word used for normal functions.

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

Inside a method, class fields such as `name` and `score` are available directly.

## Typed fields

Fields can have simple Claro types:

```claro
HAS name TEXT
HAS score NUMBER
HAS ready YESNO
```

When an object is created, Claro creates default field values and remembers their types. This means an accidental bad value can be caught:

```claro
SET player.score "oops"
```

will fail because `score` is a `NUMBER` field.

## Object helper commands

```claro
OBJECT CLASS player AS kind
OBJECT FIELDS player AS fields
```

These are useful for teaching and debugging.
