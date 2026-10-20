# Current runtime guards

These are implemented guardrails, not a sandbox or a promise that arbitrary
scripts have bounded resource use.

- **Function/method calls:** at most 256 active calls. Excessive recursion raises
  a Claro error. Other limits can stop a program earlier.
- **Expressions:** at most 128 nested parser levels, covering parentheses and
  unary operations. Excessive nesting produces a diagnostic instead of
  continuing recursive parsing.
- **Control blocks:** at most 128 additional nested control-block frames. The
  runtime and syntax checker reject deeper blocks. Function-call frames have
  their own guard.
- **HTTP response bodies:** limited to 1,048,576 bytes by the existing HTTP path.

Malformed expressions such as a lone `!`, an unclosed quote/parenthesis,
a missing operand, or trailing expression tokens are rejected by the runtime.
Use `NOT` for logical negation; `!=` remains a supported comparison.

## Not provided

The former beta document described `CLARO_STEP_LIMIT`, `CLARO_MAX_FILE_BYTES`,
and `CLARO_MAX_JSON_BYTES`. Those environment controls are not implemented in
the current `src/claro.c`; do not depend on them. The original document is
preserved under [history](history/RUNTIME_LIMITS_BETA25.md).

Ordinary intentional loops can still run indefinitely. This checkpoint does
not establish a general JSON recursion limit, global file/output-size limit,
CPU budget, or untrusted-script protection. Scripts and `RUN COMMAND` execute
with the user's permissions.

See [reliability verification](RELIABILITY.md) for the tested scope.
