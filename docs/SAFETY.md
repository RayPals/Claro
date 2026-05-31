# Safety & Hardening (Beta24)

## 1) Execution step limit
Claro can optionally stop runaway programs (infinite loops) using a step limit.

Set an environment variable:

- `CLARO_STEP_LIMIT=200000`

If the program exceeds that many executed lines/steps, Claro stops with an error.

To disable the limit:
- unset the variable, or set it to `0`.

## 2) Safer container access
LIST bounds errors now report the index and list size:
- `Index out of range: 10 (LIST size 3)`

MAP lookups return NONE when the key is not found.

## 3) Why this exists
Claro is designed for:
- learners
- classroom environments
- scripts that should fail safely

Safety limits help prevent “hangs forever” and provide clearer error messages.
