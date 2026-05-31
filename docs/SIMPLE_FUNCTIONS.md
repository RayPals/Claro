# Simple Functions

Claro teaches functions with plain words.

Preferred beginner style:

```claro
TEACH greet name
    SAY "Hello " + name
END

DO greet "Jon"
```

Older compatible style:

```claro
TEACH greet TAKES name
    SAY "Hello " + name
LEARNED

CALL greet WITH "Jon"
```
