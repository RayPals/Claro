# Runtime Guards & Limits (Beta25)

Claro includes optional safety limits to prevent hangs and memory abuse.

## 1) Step limit (runaway protection)
Environment variable:
- `CLARO_STEP_LIMIT=200000`

Stops a program if it executes too many steps/lines.

## 2) File size limit
Environment variable:
- `CLARO_MAX_FILE_BYTES=16777216` (default 16 MiB)

Applies to:
- `READ FILE ...`
- `WRITE FILE ... WITH ...`
- `APPEND FILE ... WITH ...`

## 3) JSON size limit
Environment variable:
- `CLARO_MAX_JSON_BYTES=8388608` (default 8 MiB)

Applies to:
- `PARSE JSON ...`
- `MAKE JSON ...`
- `MAKE JSON PRETTY ...`

## 4) Error output
Runtime errors include:
- `file:line: message`
- stack trace (CALL chain)
- and JSON parse errors include `Near: ...` snippet
