# Current runtime guards

Claro runs trusted scripts with the user's permissions. These guards are **not
a sandbox**, a wall-clock timeout, or proof that arbitrary scripts use bounded resources.

## Always-on nesting/response guards

- Function/method calls: at most 256 active calls.
- Expressions and additional nested control blocks: at most 128 levels.
- Parsed JSON: at most 128 nested arrays/objects. A scalar inside 128 containers
  is allowed; a 129th container is rejected. Malformed syntax fails with a Claro
  diagnostic rather than looping without consuming input. JSON Unicode escapes
  and surrogate pairs are decoded; embedded zero characters are rejected because
  Claro text uses zero-terminated strings. This is not a general encoding validator.
- HTTP response bodies: the existing 1,048,576-byte cap remains.

Errors raised during expressions keep the executing source file and line,
including imported functions and caught `LASTERRORFILE`/`LASTERRORLINE` metadata.
REPEAT without UNTIL is rejected before accessing a missing terminator.

## Optional guards — disabled by default

`CLARO_STEP_LIMIT` sets a non-negative interpreter-work budget. Zero/unset means
unlimited. It counts source-line dispatches and block/range entries, including
empty loop iterations; it is **not** an exact statement count or elapsed time.
Once exhausted it reports a source-located error suggesting the loop be checked.
The consumed budget is not reset by TRY/CATCH or by calling a function.

`CLARO_READ_FILE_LIMIT` sets the maximum bytes read by each `READ FILE` command.
Zero/unset means unlimited. The exact boundary is accepted; larger input errors
without storing a partial result. It does not cap source loading, package metadata,
all file operations, aggregate memory or output. Invalid/overflowing limit values
fail configuration; supported numeric range depends on the compiler's unsigned long.

For example, in a Windows command prompt before running a reviewed script:

```bat
set CLARO_STEP_LIMIT=10000
set CLARO_READ_FILE_LIMIT=1048576
claro98.exe practice.claro
```

On Linux/macOS shells the equivalent is an environment assignment before `./claro`.
These optional budgets do not interrupt a blocked ASK, a shell command, curl,
or an individual long-running builtin. They are not untrusted-code protection.

## Not provided

There is no general CPU/time budget, process isolation, total-allocation limit,
global file/output limit or JSON byte-size control. The old beta names
`CLARO_MAX_FILE_BYTES` and `CLARO_MAX_JSON_BYTES` are still not implemented.
The newer READ FILE guard is deliberately narrower. The former unimplemented
step-limit claim is preserved as history; the current step guard is the explicit
implementation described above, not validation of those older promises.

Without the optional step budget ordinary intentional loops can run indefinitely.
Run only trusted scripts. See [reliability](RELIABILITY.md),
[errors and repairs](ERRORS.md), and the [historical limits](history/RUNTIME_LIMITS_BETA25.md).
