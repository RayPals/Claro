# Practical Scripting in Claro

Claro v1.10.26 includes simple commands that make small automation scripts possible.

## Arguments

```claro
COUNT ARGUMENTS AS total
GET ARGUMENT 1 AS first
GET ALL ARGUMENTS AS args
```

Run with:

```bash
claro myscript.claro apple banana
```

## Environment

```claro
GET ENV "PATH" AS path
SAY path
```

## Folders and files

```claro
CREATE FOLDER "output"
WRITE FILE "output/hello.txt" WITH "Hello"
COPY FILE "output/hello.txt" TO "output/copy.txt"
MOVE FILE "output/copy.txt" TO "output/moved.txt"
LIST FOLDER "output" AS files
DELETE FILE "output/hello.txt"
DELETE FILE "output/moved.txt"
DELETE FOLDER "output"
```

## Text helpers

```claro
TEXT UPPER "hello" AS loud
TEXT LOWER "LOUD" AS quiet
TEXT TRIM "  neat  " AS clean
TEXT LENGTH clean AS size
TEXT CONTAINS "hello world" NEEDLE "world" AS found
```

## List helpers

```claro
SORT names
REVERSE names
FIND "Jon" IN names AS place
REMOVE "Jon" FROM names
```

## External commands

```claro
RUN COMMAND "echo hello" AS output
SAY output
SAY LASTEXIT
```

Use this carefully. It runs commands on the user's computer.
