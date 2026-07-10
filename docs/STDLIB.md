# Claro Standard Library

Claro keeps common tasks readable. Most beginner programs can use commands such as `TEXT LENGTH`, `COUNT`, `GET`, `PUT`, `READ FILE`, and `WRITE FILE` directly. For reusable helper functions, import a standard-library module.

## Path helpers

```claro
IMPORT "lib/path.claro" AS path

CALL path.join WITH "notes", "today.txt"
SAY RESULT                 # notes/today.txt

CALL path.basename WITH "notes/today.txt"
SAY RESULT                 # today.txt

CALL path.dirname WITH "notes/today.txt"
SAY RESULT                 # notes

CALL path.ext WITH "notes/today.txt"
SAY RESULT                 # txt

CALL path.stem WITH "notes/today.txt"
SAY RESULT                 # today

CALL path.absolute WITH "/home/learner"
SAY RESULT                 # YES
```

`path.join` returns portable `/`-separated paths. `path.absolute` recognizes `/`, `\\`, and Windows drive-letter paths.

## Collection helpers

```claro
IMPORT "lib/collections.claro" AS collections

SET names AS LIST OF TEXT TO LIST
ADD "Ada" TO names
ADD "Grace" TO names

CALL collections.length WITH names
SAY RESULT                 # 2
CALL collections.join WITH names, " and "
SAY RESULT                 # Ada and Grace
CALL collections.contains WITH names, "Grace"
SAY RESULT                 # YES
CALL collections.index WITH names, "Grace"
SAY RESULT                 # 2
```

Available list helpers:

- `collections.length WITH items`
- `collections.contains WITH items, value`
- `collections.index WITH items, value` — returns a **1-based** position, or `0` when absent
- `collections.join WITH items, separator`
- `collections.reversed WITH items` — returns a new list; the source list is unchanged

Available map helpers:

- `collections.has_key WITH values, key`
- `collections.get WITH values, key, fallback`
- `collections.keys WITH values`
- `collections.values WITH values`

Use the returned value through `RESULT`, exactly as with other Claro function calls.

## Existing modules

- `lib/text.claro`: text case checks and simple splitting
- `lib/math.claro`: numeric helpers
- `lib/random.claro`: deterministic seed and integer helpers
- `lib/csv.claro`: CSV read/write helpers

## Commands rather than promises

The `PATH ...` and `TIME ...` command forms in older planning material are not part of the stable Claro command set. Use the documented `path` module above and the core file commands instead. This page describes the APIs currently shipped and validated in the stable executable.
