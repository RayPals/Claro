# Claro Trace Mode (Beta27)

Trace mode prints each executed line as Claro runs your program.

## Run trace
```bash
claro trace yourfile.claro
```

Or:
```bash
claro run yourfile.claro --trace
```

## What you’ll see
Trace prints to **stderr**:

```
TRACE main.claro:1 | SET x TO 0
TRACE main.claro:2 | REPEAT
TRACE main.claro:3 | SET x TO x + 1
...
```

This is useful when:
- the program hangs
- you want to see where execution is looping
- you want a “step-by-step” view without a debugger
