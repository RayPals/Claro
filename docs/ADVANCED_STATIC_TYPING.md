# Advanced Static Typing

Claro v1.18.26 adds the first advanced static-typing foundation: typed containers checked by `claro typecheck`.

## Typed lists

```claro
SET names AS LIST OF TEXT TO LIST
ADD "Ada" TO names
ADD "Grace" TO names
```

The type checker now rejects wrong item types:

```claro
SET names AS LIST OF TEXT TO LIST
ADD 123 TO names
```

Output:

```text
Type mismatch for list names: expected TEXT item, but this value looks like NUMBER.
```

## Typed maps

```claro
SET scores AS MAP OF NUMBER TO MAP
PUT scores KEY "math" VALUE 98
```

The type checker rejects wrong value types:

```claro
SET scores AS MAP OF NUMBER TO MAP
PUT scores KEY "oops" VALUE "high"
```

Output:

```text
Type mismatch for map scores: expected NUMBER value, but this value looks like TEXT.
```

## Function parameter checks

Claro now has a small static-checking foundation for function arguments. Keep the beginner-friendly function syntax, then put the expected type inside the function with `CHECK TYPE`:

```claro
TEACH square amount
    CHECK TYPE amount IS NUMBER
    SAY amount
END

DO square 4
```

If a learner calls the function with the wrong kind of value, `claro typecheck` explains which parameter needs which type:

```claro
TEACH square amount
    CHECK TYPE amount IS NUMBER
    SAY amount
END

DO square "oops"
```

Output:

```text
Type mismatch for function square: parameter amount needs NUMBER, but this argument looks like TEXT.
```

## Status

This is currently a static checker feature. It improves `claro typecheck` and validation confidence. Runtime enforcement for every container mutation and richer function signatures can be added later after the syntax is classroom-tested.
