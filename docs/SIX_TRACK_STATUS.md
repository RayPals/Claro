# Six-track progress — development candidate v2026.10.21.010934

This is a work/acceptance map, not a stable release or a claim all six external
milestones are complete. Real learner sessions and native OS access were not
supplied in the clarification request. No simulated observations are recorded.

## 1. Error reporting — implemented, regression-tested

Expressions retain file/line origins through functions, imports, UNTIL and
TRY/CATCH metadata. The first failing location is not overwritten by its caller.
Focused tests cover direct, nested and caught paths, including leak-enabled runs.

## 2. Error guide — aligned and executable-verified

The [guide](ERRORS.md) now shows current short SET/END forms and six actual
failure/repair pairs. `tests/error_examples.json` is checked against every guide
code block and against the interpreter's diagnostic and repaired output.

## 3. Beginner testing — kit ready; actual learner acceptance BLOCKED

The [pilot kit](LEARNER_PILOT.md) contains six small starter tasks (three primary,
three optional), observer instructions and a [blank feedback form](LEARNER_FEEDBACK_TEMPLATE.md).
Automated code/output checks are not a person testing the language. A willing,
consenting learner and anonymous real observations are still required.

## 4. Native Windows — test kit prepared; target acceptance BLOCKED

[Native checks](NATIVE_WINDOWS_TESTING.md) require an authorized Windows login or
real Windows 98 SE VM. No such access was supplied. The OS helper explicitly
rejects Wine and can require Win98 SE 4.10.2222 before a PASS marker is written.
Compiler/Wine checks are separate evidence and never counted as target acceptance.

## 5. Robustness — focused fixes and guards, not a sandbox

Malformed JSON such as `[?]` previously hung; it now produces a located diagnostic.
Containers are bounded at 128, separators/numbers/escapes are checked, Unicode
escapes/surrogate pairs and control-character serialization are covered. JSON
parse/serialize temporaries and popped import entries have cleanup regressions.
Missing UNTIL is rejected. Opt-in step and per-READ FILE byte budgets are described
in [runtime guards](RUNTIME_LIMITS.md). Empty loops consume work budget; TRY/CATCH
does not reset it. These do not bound all memory, time, output or external commands.

## 6. Release delivery — candidate validation; hosted gate BLOCKED

Local source/Linux/Windows candidate archives must pass extracted-payload checks
before delivery. Actual checksums/reports belong to those frozen artifacts, not
just the source checkout. The VC6 ZIP uses a separate manifest/report path.

On this run the Gitea repository metadata reported `has_actions: false`; the
Actions runs API returned HTTP 401, the Actions web page was unavailable, and
there was no authenticated browser/API credential. Secure vault entry was not
available in this session. Hosted CI cannot be verified or enabled from Git SSH
access alone. No hosted release or CI success is claimed and no release assets
have been uploaded. Authenticated administration and enabled/configured Actions
are needed before completing the requested hosted CI/release gate.

The repository API also reported `private: false`. No visibility change was made;
do not put credentials or sensitive learner/native-host information into this repo.

See [release status](RELEASE_STATUS.md) for dated earlier checkpoints. Candidate
build evidence does not retroactively validate native Windows or accessibility.
