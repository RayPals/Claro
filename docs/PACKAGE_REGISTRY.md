# Claro Package Registry Plan

Current release: **Claro v1.18.26**

Claro already has a local project/package foundation. A remote package registry should come later, after safety and teaching rules are clear.

## Ready now

- `claro new`
- `claro package init`
- `claro package add`
- `claro package list`
- `claro package remove`
- `claro package doctor`
- `claro package lock`
- package-name safety checks

## Registry goals

A beginner-friendly registry should be:
- predictable
- safe by default
- easy to inspect
- offline-tolerant where possible
- resistant to path traversal and confusing package names

## Needed before downloads

- package manifest format
- semantic version or simple v1-compatible version rules
- dependency constraints
- lock-file checksums
- package archive format
- signature or checksum verification
- local cache rules
- clear error messages when the network is unavailable

## Suggested phases

1. Local install from a folder.
2. Package export to a `.claro-package` archive.
3. Lock-file checksum verification.
4. Read-only registry index download.
5. Safe install from registry.
6. Publishing flow only after moderation/auth rules are designed.

See also:
- `V1_16_PACKAGES_PROJECTS.md`
- `CURRENT_STATUS.md`
- `ROADMAP.md`
