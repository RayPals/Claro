# Release checklist

This is an **unchecked template**, not a claim that every item is still missing
from earlier verified builds. Record evidence for the exact candidate; see
[release status](RELEASE_STATUS.md) for completed artifact checkpoints.

## Identify the candidate

- [ ] Review the working tree and preserve unrelated local changes.
- [ ] Stamp a new run once with `python3 tools/stamp_version.py`, using UTC
      `vYYYY.MM.DD.HHMMSS`; keep that stamp through rebuilding and verification.
- [ ] Confirm runtime, IDE metadata, generated starter/lockfiles and current docs
      agree. Never re-label old verified binaries with a new timestamp.
- [ ] Name each intended target and distinguish build, Wine and native OS tests.

## Verify source and learning behavior

- [ ] Build both executable names required by the developer checks: `make -s all`.
- [ ] Run `python3 tools/validate_v1_17.py` (the current full gate despite its name).
- [ ] Run compiler-warning, CI-coverage and documentation-status checks from
      [testing](TESTING.md). Confirm expected failures, skips and actual exit codes.
- [ ] Exercise interactive lessons and common mistakes with intended learners;
      automated examples alone do not validate accessibility.
- [ ] Keep the recommended introductory syntax consistent and preserve aliases.
- [ ] Describe trust boundaries and unverified behavior without claiming a sandbox.

## Verify deliverables, not just the checkout

- [ ] Build clean archives with [distribution tooling](PORTABILITY.md).
- [ ] Extract each artifact, verify its inventory/hashes, and test its actual
      executable, lessons, files and paths containing spaces.
- [ ] Record artifact/source SHA-256, compiler, environment, results and limitations.
- [ ] Include the license and applicable runtime notices; exclude compiler/SDK
      bundles, credentials, caches and development build outputs.
- [ ] For the VC6 target, compile through [build98.bat](../build98.bat) without
      a global `intptr_t` macro; inspect PE32, subsystem 4.10 and stack reserve.
- [ ] If claiming Windows or Windows 98 SE runtime support, execute the tests on
      that actual OS. Otherwise label it unverified; Wine is not a substitute.
- [ ] Confirm checksums identify exact files, not publisher authenticity/signatures.

The generic archive helper covers source, Linux x64 and MinGW Windows x64.
The separately verified VC6 build ZIP has its own checksum manifest and report;
do not claim it was produced or accepted by that helper.

## Publish only with authorization

- [ ] Review and test the exact proposed commit/package snapshot.
- [ ] Obtain authorization before committing, pushing or publishing releases.
- [ ] Verify the remote branch after a push and download/test hosted artifacts
      before claiming a hosted release or CI result.
- [ ] Update the dated release ledger with the actual version, hashes, scope,
      publication location and remaining limitations. Keep older evidence intact.

Do not expand the language to complete a release. Reliability, clear learning
instructions and honest platform claims take priority.
