# Hardening Notes (Beta23)

## File loading safety
Claro now reads source lines dynamically (no 4KB truncation).

Safety caps (to prevent memory abuse):
- Maximum single line length: 65,535 characters
- Maximum program lines: 500,000

If a file exceeds these limits, the loader fails cleanly.

## Expression-token cleanup

Each expression now releases its token strings and token-array storage before returning. This is a narrow cleanup boundary; runtime-owned variables, loaded programs, and other allocations remain separate follow-up work.

Focused verification:

```text
python3 tools/validate_memory_cleanup.py
```

The validator builds an AddressSanitizer/UndefinedBehaviorSanitizer binary, runs a repeated variable-overwrite probe, and confirms LeakSanitizer no longer reports allocations from `tokenize`/`toks_add`. The interpreter remains a trusted-script runtime, not a sandbox.

## Overwritten-value cleanup

Runtime variables and map entries own deep copies of their values. Replacing an existing variable or map entry now releases the previous string, list, or map value before storing its replacement. This is intentionally limited to overwrite boundaries; final runtime teardown and discarded expression temporaries remain follow-up cleanup slices.

Focused verification also checks the cleanup helper in the ASan/UBSan build and exercises string, list, and map overwrites without sanitizer errors.
