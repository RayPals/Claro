# Native Windows acceptance kit

**Prepared, not executed on a native target.** Wine results do not satisfy this
checklist. A Windows login/authorized VM was not supplied for this run.

Use a **fresh extracted test folder**, not personal documents. Scripts write
`oscheck.txt`, `nver.txt`, `ntests.txt`, `ncheck.txt` and replace their own `native.ok`
marker. Preserve failed logs. A marker alone is not proof: review the OS evidence,
version, all discovered fixtures and every test result together.

## OS evidence helper

`tools/native_platform_probe.c` builds a separate `osprobe.exe`; it is not a
second interpreter source file. With VC6 configured:

```bat
cl /nologo /TC /ML /O1 tools\native_platform_probe.c /Feosprobe.exe /link /SUBSYSTEM:CONSOLE,4.10
```

The probe records numeric OS API fields, detects Wine's exported implementation
entry point, and refuses Wine with exit 2. `--require-win98se` additionally needs
Win32-Windows platform ID and version 4.10 build 2222. A real Windows VM is an
acceptable target; a compatibility layer is not. Old API version reporting on
modern Windows can be affected by application compatibility, so also record the
actual OS/version from its own system information screen. The probe is evidence,
not cryptographic attestation or a substitute for inspecting a real target.

## Automated checks

Put the compiled probe beside the matching interpreter and the complete package.
For Windows 98 SE run [test98.bat](../test98.bat). For modern x64 Windows run
[testwin.bat](../testwin.bat) with the MinGW `claro.exe` build.
These batch scripts avoid modern CMD-only extensions and reject a wrong target
before writing a PASS marker. Review `ntests.txt`: every packaged golden fixture
must appear, with zero failures. `ncheck.txt` must show built-in validation passed.

## Manual target observations — leave blank until actually tested

- Artifact version/SHA-256 and OS/VM identity:
- `oscheck.txt` reviewed, Wine false, target version independently confirmed:
- All packaged fixtures discovered/passed:
- Keyboard input, editing and non-ASCII display observations:
- Save/read a text file in a writable folder:
- File paths containing spaces:
- Start/stop a loop and recover to the console:
- First-hour examples and quiz interaction:
- Missing input or failed command recovery:
- Tester/date, consent to retain anonymous notes, unresolved failures:

Transfer only consented technical logs, not passwords, personal files or medical
information. Do not change an unknown remote machine or install services just to
make a test pass. The native target remains **unverified** until these observations
and actual target logs exist. See [Windows 98 compilation](WINDOWS98.md).
