# Claro Language Specification (Draft)

Version: **0.19-draft** (Beta19-Spec)  
Status: **Draft** (stability work in progress)

This document defines the intended behavior of the Claro language. It’s written to reduce breaking
changes and make the path to 1.0 clear.

---

## 1. Design goals

1. Easy to learn: readable keywords, minimal punctuation.
2. Accessible: consistent rules, simple mental model, clear errors.
3. General-purpose scripting: files, JSON/CSV, small tools.
4. Safe by default: TRY/CATCH, predictable runtime behavior.

Non-goals for 1.0:
- Concurrency / threads
- Advanced static typing
- Metaprogramming / macros

---

## 2. Source files

- UTF-8 text files.
- LF or CRLF line endings.
- Trailing whitespace is ignored.
- Empty lines are ignored.

---

## 3. Comments

### 3.1 Single-line
`#` starts a comment to end-of-line.

### 3.2 Multi-line block
A block comment starts with `COMMENT` and ends with `ENDCOMMENT`.
Everything between is ignored.

---

## 4. Runtime values (types)

Claro is dynamically typed. A value is one of:

- NONE
- NUMBER (floating point; also used for integers)
- TEXT
- BOOL (`YES` / `NO`)
- LIST (ordered; **1-based indexing**)
- MAP (dictionary; keys are TEXT)

---

## 5. Variables

### 5.1 Assignment
```
SET name TO "Alex"
SET n TO 10
```

### 5.2 Built-ins
These names are used by the runtime:

- RESULT — value returned by the most recent CALL
- LASTERROR — most recent error message
- LASTERRORFILE — file name for most recent error
- LASTERRORLINE — line number for most recent error

User code can read these. Writing them is allowed but discouraged.

---

## 6. Expressions

Expressions can appear in SET/IF/RETURN/etc.

Operators (high → low precedence):

1. `( ... )`
2. `NOT x`
3. `* /`
4. `+ -`
5. `= != < <= > >=`
6. `AND OR`

Rules:
- `+` concatenates text if either operand is TEXT.
- Comparisons return BOOL.

---

## 7. Commands (statements)

Keywords are case-insensitive. Each statement is one line beginning with a keyword.

### Output
```
SAY expr
```

### Conditionals
```
IF cond
    ...
ELSEIF cond
    ...
ELSE
    ...
ENDIF
```

### Loops

Numeric:
```
FOR i FROM a TO b
    ...
DONE
```

Iteration:
```
FOR EACH item IN listOrMap
    ...
DONE
```

Repeat:
```
REPEAT
    ...
UNTIL cond
```

---

## 8. Functions

Define:
```
TEACH name TAKES a, b
    ...
    RETURN expr
LEARNED
```

Call:
```
CALL name WITH x, y
```

After CALL, RESULT contains the returned value (or NONE if no RETURN executed).

---

## 9. Errors

Raise:
```
RAISE "message"
```

Handle:
```
TRY
    ...
CATCH
    SAY LASTERROR
ENDTRY
```

Rules:
- Errors inside TRY jump to CATCH.
- Errors outside TRY terminate the program with non-zero exit code.
- LASTERROR*, including file/line, update on error.

---

## 10. Data structures

### LIST
1-based indexing:
```
SET xs TO LIST
ADD 1 TO xs
GET xs AT 1 AS first
```

### MAP
TEXT keys:
```
SET m TO MAP
PUT m KEY "k" VALUE 1
GET m KEY "k" AS v
```

---

## 11. JSON

Parse:
```
PARSE JSON text AS value
```

Make:
```
MAKE JSON value AS text
MAKE JSON PRETTY value AS text
```

Parse errors should report a position (character offset) and context snippet.

---

## 12. Imports

```
IMPORT "path/to/module.claro" AS mod
EXPORT ALL
```

Import resolution order:
1. Relative to the importing file’s folder
2. Each folder in CLARO_PATH
3. Current working directory

---

## 13. CLI

```
claro run file.claro
claro repl
claro fmt file.claro [--inplace]
claro check file.claro
claro test
```

---

## 14. Beta “may change” list

Until 1.0, these are still being stabilized:
- exact numeric precision rules
- MAP iteration ordering (1.0 will define it)
- exact wording/format of error messages
- REPL multi-line behaviors
