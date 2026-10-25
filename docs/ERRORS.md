# Errors and small repairs

An error starts with `filename:line:`. Open that file and find that line.
The line belongs to the function or imported file where the error happened,
not automatically to the caller. Caught errors expose the same origin through
`LASTERRORFILE` and `LASTERRORLINE`.

Use `claro check my_program.claro` for command/block mistakes; running the
program also detects runtime expression/value errors. A checker is not a sandbox.
The examples below are executed by `tools/validate_error_guide.py`.

## Quote

Save as `quote.claro`. Run `claro quote.claro`.

```claro
SAY "Start"
SAY "unfinished
```

Message:

```text
quote.claro:2: Text is missing a closing quote. Add a double quote at the end.
```

One repair:

```claro
SAY "Start"
SAY "finished"
```

## Operand

Save as `operand.claro`. Run `claro operand.claro`.

```claro
SET score 1
SAY score +
```

Message:

```text
operand.claro:2: This expression needs a value after the operator.
```

One repair:

```claro
SET score 1
SAY score + 1
```

## Command

Save as `command.claro`. Run `claro check command.claro`.

```claro
PRNT "Hello"
```

Message:

```text
command.claro:1: I do not know the command "PRNT". Did you mean "SAY"?
```

One repair:

```claro
SAY "Hello"
```

## Assignment

Save as `assignment.claro`. Run `claro check assignment.claro`.

```claro
SET name
```

Message:

```text
assignment.claro:1: SET needs a name and a value. Try: SET name "Alex"
```

One repair:

```claro
SET name "Alex"
SAY name
```

## Choice

Save as `choice.claro`. Run `claro check choice.claro`.

```claro
IF YES
    SAY "Yes"
```

Message:

```text
choice.claro:1: IF block opened here needs END
```

One repair:

```claro
IF YES
    SAY "Yes"
END
```

## Variable

Save as `variable.claro`. Run `claro variable.claro`.

```claro
SET score 10
SAY socre
```

Message:

```text
variable.claro:2: I do not know the variable "socre" yet.
```

One repair:

```claro
SET score 10
SAY score
```

These teach short `SET` and `END`. Older forms remain supported in
[compatibility syntax](COMPATIBILITY.md), not required as repairs.
For a caught error, read its metadata before another error changes it.
