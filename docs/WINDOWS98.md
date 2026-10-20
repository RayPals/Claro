# Windows 98 SE compilation (Visual C++ 6.0)

Claro has a dedicated **32-bit x86, MSVC6** build. It keeps the runtime in the
single `src/claro.c` file. This is separate from the modern MinGW x64 download.

## Build on a configured VC6 system

1. Extract the project to a short path such as `C:\CLARO`.
2. Open the compiler environment installed with Visual C++ 6.0, or run that
   installation's original `VCVARS32.BAT`. Check `cl` reports compiler 12.00.
   Compiler, include and library paths remain installation-specific; the project
   does not bundle Microsoft's toolchain.
3. Change to the Claro folder and run:

```bat
build98.bat
```

The output is `claro98.exe`. Try:

```bat
claro98.exe --version
claro98.exe lessons\01_hello.claro
claro98.exe test
```

`build98.bat` and `build98.rsp` use 8.3-compatible names. The batch file uses no
`SETLOCAL`, `%~dp0`, `EXIT /B`, `WHERE`, or command-chaining extensions. Compiler
options live in a response file to avoid COMMAND.COM's short command-line limit.
Both files use CRLF line endings. Modernized toolchain environment wrappers may
use CMD-only syntax; use the VC6 environment appropriate to the actual host.

## Target settings

- `/TC /W3`: compile as C with normal warnings.
- `/ML /O1`: VC6 static single-threaded CRT, optimized for size. No newer Visual
  C++ runtime DLL needs to be installed for this build.
- `WINVER=0x0410`, `_WIN32_WINDOWS=0x0410`: Windows 98 header target selection.
- `/MACHINE:I386 /SUBSYSTEM:CONSOLE,4.10`: 32-bit x86 console executable with a
  Windows 98-era subsystem version.
- `/STACK:16777216`: 16 MiB reserve so nested calls reach Claro's existing
  recursion guard instead of overflowing the default Windows stack first.

The source selects `long` for `_findfirst` handles on pre-VC7 MSVC, matching the
VC6 CRT declaration. Modern compilers retain their pointer-sized handle type.
No `/Dintptr_t=long` workaround is used.

## Verification boundary

The build is exercised with the actual MSVC600 compiler and linker under Wine.
The source/build-policy check is `python3 tools/validate_msvc6_source.py`, also
included in full release validation and CI. It does not replace the actual VC6
compiler test.

A PE header and a successful Wine test are not proof of execution on Windows
98 SE. Native Win98 SE loader/CRT, filesystem, console, shell, encoding and device
behavior still need testing on that OS or a faithful emulator. Some static VC6
CRT imports include Wide-character API entry points and fallback paths; their
presence must not be mistaken for a modern-NT-only requirement or for proof of
Win98 correctness without a real target test.

Real HTTP requires a separately compatible curl executable. No modern TLS stack,
GUI installer, Microsoft SDK or runtime DLL bundle is supplied. Run only trusted
scripts. See [portability](PORTABILITY.md) and [runtime limits](RUNTIME_LIMITS.md).
