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

The `REMOVE` command now releases its evaluated needle and copied list/map value after updating runtime storage. Focused verification: `python3 tools/validate_remove_expression_cleanup.py` runs 2,000 discarded string needles under ASan/UBSan/LSan; it passed with no reported leaks. This slice does not yet address the separate ownership of an item removed from a populated copied list.

The `PUT ... KEY ... VALUE ...` command now releases its evaluated map, key, and value copies after `map_put`/`rt_set` have copied the data they own. Focused verification: `python3 tools/validate_put_expression_cleanup.py` exercises 2,000 string-valued writes under ASan/UBSan/LSan and passes with no reported leaks. This covers expression-temporary ownership only; broader malformed-input sanitizer runs still report the previously documented `rt_error` diagnostic-string leaks.

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

## Control-flow expression cleanup

Conditions evaluated by `IF` are temporary runtime values. The `IF` command now
releases its condition after choosing a branch, including when the condition is
a text expression. This is a narrow cleanup boundary; other expression
temporaries remain separate follow-up work.

Focused verification:

```text
python3 tools/validate_control_expression_cleanup.py
```

The validator builds with AddressSanitizer/UndefinedBehaviorSanitizer,
executes 2,000 temporary `IF` conditions under LeakSanitizer, and checks the
expected output.

## ASK temporary-value cleanup

`ASK` releases the evaluated prompt value after converting it to display text,
and releases the temporary input value after `rt_set_checked` copies it into
runtime storage. This keeps prompt and input strings from accumulating during
repeated input loops without changing prompt or input behavior.

Focused verification:

```text
python3 tools/validate_ask_prompt_cleanup.py
```

The validator runs 2,000 prompt/input operations with AddressSanitizer, UndefinedBehaviorSanitizer, and LeakSanitizer enabled. The dedicated validator passes. A separate malformed-input sanitizer smoke run (`gcc -std=c99 -O0 -g -fsanitize=address,undefined src/claro.c -o ... -lm` followed by the generated malformed script) exits 1 due to two existing leaked error-message strings (140 bytes total) allocated in `rt_error` at `src/claro.c:142`; this is outside the ASK cleanup slice and remains a blocker to sanitizer-clean malformed-input validation.

## GET KEY temporary-value cleanup

`GET ... KEY ... AS ...` releases its evaluated map copy and key value after storing the selected value. `python3 tools/validate_get_key_expression_cleanup.py` runs 2,000 lookups under ASan/UBSan/LSan; before the cleanup it reproduced 1,004,000 bytes leaked, and after it passes with the expected output and no reported leaks.
