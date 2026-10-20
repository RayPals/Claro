# Hardening notes: current entry point

The earlier Beta23 notes and later cleanup investigation are **historical**.
Their former failure reports, resource-cap claims and pending-work statements
must not be read as the status of today's tested runtime.

- [Current reliability checkpoint](RELIABILITY.md): repairs, maintained checks
  and their limitations, including the resolved OBJECT ownership regressions.
- [Actual runtime guards](RUNTIME_LIMITS.md): implemented bounds and absent limits.
- [Testing](TESTING.md): commands to reproduce current evidence.
- [Preserved hardening log](history/HARDENING_BEFORE_STATUS_CLEANUP.md): earlier
  observations retained without rewriting them as modern acceptance results.

Claro runs trusted scripts with the user's permissions and is **not a sandbox**.
Passing maintained regressions does not establish universal leak freedom or
untrusted-script safety. Treat newly reproduced failures as new findings with
exact versions, inputs, diagnostics and regression tests.
