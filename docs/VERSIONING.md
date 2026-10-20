# Claro Versioning

Development/release runs use their current UTC date and time:

```text
vYYYY.MM.DD.HHMMSS
```

For example, `v2026.10.20.155641` identifies a run started on
2026-10-20 at 15:56:41 UTC. A timestamp identifies a run, not its maturity.

At the start of a new development/release run:

```bash
python3 tools/stamp_version.py
make -s all
```

The stamper updates current runtime, IDE metadata, generated project and
lockfile versions, validators, and selected current documentation. Historical
release records are preserved. Rebuilding or testing within the same run
retains the stamp; do not stamp again before each validation command.

Check the built version with `./claro --version`. Existing project lockfiles
from older runs can be refreshed with `claro package lock`.

Older `v1.xx.yy` labels describe historical releases, not the current convention.
