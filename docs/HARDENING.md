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

Runtime variables and map entries own deep copies of their values. Replacing an existing variable or map entry now releases the previous string, list, or map value before storing its replacement. This is intentionally limited to overwrite boundaries; final runtime teardown remains a follow-up cleanup slice.

## Split-argument cleanup

Command argument lists created by `DO`, `CALL`, `TEXT ... CONTAINS`, and `RANDOM` are temporary parser storage. They now share one cleanup helper, so repeated calls do not retain the duplicated argument strings or pointer array. The helper does not change argument evaluation or syntax compatibility.

Focused verification builds with AddressSanitizer/UndefinedBehaviorSanitizer, repeatedly exercises a four-argument `DO`, and checks the cleanup helper before confirming the existing string, list, and map overwrite behavior.

## HTTP response handling

HTTP responses are capped at 1,048,576 bytes. Exceeding the cap produces a beginner-facing runtime error instead of retaining an unbounded response. The curl status suffix is taken from the final status marker, so a response body containing marker-like text is preserved. Existing `HTTP CHECK` URL safety rules remain unchanged.

Focused verification:

```text
python3 tools/validate_http_hardening.py
```

This validator uses a local HTTP server to check marker-like response text, status `200`, and the oversized-response diagnostic.

## External command trust boundary

`RUN COMMAND` intentionally executes a shell command with the user's permissions. It is a trusted-code capability, not a sandbox or an untrusted-script safety feature. Claro does not attempt a fragile blacklist sanitizer; users must review scripts before running them.

Focused documentation verification:

```text
python3 tools/validate_trusted_command_docs.py
```
