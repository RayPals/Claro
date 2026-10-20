# Simple Functions

Claro teaches functions with plain words.

Preferred beginner style:

```claro
TEACH greet name
    SAY "Hello " + name
END

DO greet "Jon"
```

`TEACH` defines an action. `DO` runs it. `END` closes the definition.
Older programs are still supported; see [compatibility syntax](COMPATIBILITY.md)
only when reading one.
