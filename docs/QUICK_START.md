# Claro Quick Start Guide

Programming Made Simple

## What is Claro?

Claro is a small scripting language designed for beginners. It uses readable commands like `SAY`, `ASK`, `SET`, and `TEACH`.

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
ASK "What is your name?" AS name
SAY "Hello " + name
```

## 3. Remember information

```claro
SET score TO 10
SAY score
```

## 4. Make a choice

```claro
IF score >= 5
    SAY "Good job!"
ELSE
    SAY "Try again."
ENDIF
```

## 5. Repeat something

```claro
DO 3 TIMES
    SAY "Practice"
DONE
```

## 6. Use a list

```claro
SET items TO LIST
ADD "milk" TO items
ADD "bread" TO items

FOR EACH item IN items
    SAY item
DONE
```

## 7. Teach a function

```claro
TEACH greet TAKES name
    RETURN "Hello " + name
LEARNED

CALL greet WITH "Alex"
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
ASK "What is 2 + 2?" AS answer

IF answer = 4
    SAY "Correct!"
ELSE
    SAY "The answer is 4."
ENDIF
```

## Tips

- Use `SAY` to show information.
- Use `ASK` to get information.
- Use `SET` to remember information.
- Use `IF` when the program needs to choose.
- Use `DO` or `FOR` when something repeats.
- Use `TEACH` to make reusable code.
