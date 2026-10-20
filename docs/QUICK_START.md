# Claro Quick Start Guide

Programming Made Simple

## What is Claro?

Claro is a small scripting language designed for beginners. It uses readable commands like `SAY`, `ASK`, `SET`, and `TEACH`.

## Before you start

Build Claro with `make` from the project folder, or use its C89 build command
in the [README](../README.md). Save the first example below as `hello.claro`
in that folder. Run the command shown beneath it. Try the later examples one
at a time, saving your changes before running again.

Use one spelling throughout these lessons: short `ASK` and `SET`, `TEACH`
with `DO`, and `END` for choices, counted loops, and functions. The
[syntax guide](SYNTAX.md) keeps these rules in one place.

## 1. Show a message

```claro
SAY "Hello!"
```

Run it:

```bash
./claro hello.claro
```

## 2. Ask a question

```claro
ASK "What is your name?" name
SAY "Hello " + name
```

## 3. Remember information

```claro
SET score 10
SAY score
```

## 4. Make a choice

```claro
SET score 8

IF score >= 5
    SAY "Good job!"
ELSE
    SAY "Try again."
END
```

## 5. Repeat something

```claro
DO 3 TIMES
    SAY "Practice"
END
```

## 6. Use a list

```claro
SET items LIST
ADD "milk" TO items
ADD "bread" TO items

FOR EACH item IN items
    SAY item
END
```

## 7. Teach a function

```claro
TEACH greet name
    RETURN "Hello " + name
END
DO greet "Alex"
SAY RESULT
```

## 8. Save a file

```claro
WRITE FILE "note.txt" WITH "Hello from Claro"
READ FILE "note.txt" AS note
SAY note
```

## Good first project: a quiz

```claro
SAY "Tiny Quiz"
ASK "What is 2 + 2?" answer

IF answer = 4
    SAY "Correct!"
ELSE
    SAY "The answer is 4."
END
```

## Tips

- Use `SAY` to show information.
- Use `ASK` to get information.
- Use `SET` to remember information.
- Use `IF` when the program needs to choose.
- Use `DO` or `FOR` when something repeats.
- Use `TEACH` to make reusable code.
