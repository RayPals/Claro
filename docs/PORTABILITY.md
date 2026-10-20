# Distribution and portability

See the dated [release ledger](RELEASE_STATUS.md) for exact verified archive
versions and publication status. A development stamp is not a hosted release.

## Supported verification targets

- **Source:** one C89 implementation file, `src/claro.c`. The distribution checker
  compiles a copy in isolation, without the rest of the project, then builds and
  validates the full extracted source package.
- **Linux x86-64:** a statically linked musl executable named `claro`. It does not
  depend on the build host's glibc or a separately installed musl shared library.
- **Windows x86-64:** a genuine PE executable named `claro.exe`, built with MinGW.
  Current execution verification uses Wine on Linux, not a native Windows machine.

The Linux and Windows archives include lessons, examples, documentation, regression
fixtures, source and tooling. No compiler or Python is required merely to run the
included executable and lessons. Developer checks require Python and build tools.

## Build archives

From the repository root on the tested Debian/Ubuntu x86-64 build host:

```bash
python3 tools/build_distribution.py --target source --output /path/to/releases
python3 tools/build_distribution.py --target linux-x86_64 --output /path/to/releases
python3 tools/build_distribution.py --target windows-x86_64 --output /path/to/releases
```

Binary builds require `musl-tools` or the x64 MinGW cross-compiler respectively.
The helper also includes installed toolchain copyright notices; its notice paths
currently match the tested Debian/Ubuntu packages. It refuses to overwrite an archive.

Each archive has:

- `START_HERE.txt` with target-specific instructions.
- `DISTRIBUTION.json` identifying the target, compiler, command and source hash.
- `MANIFEST.json` listing SHA-256 hashes for every other packaged file.
- The project license and, for binaries, third-party runtime notices.

A checksum detects changes; it is not a digital signature or proof of publisher identity.
Generated executables/caches from the development tree are not copied into releases.
In particular, the Linux archive does not contain a misleading Linux `claro.exe`.

## Windows 98 SE / MSVC6 compilation

Use the dedicated [Windows 98 build guide](WINDOWS98.md) and `build98.bat`.
This is a separate x86 build, not the MinGW x64 archive target. Compiler and
Wine verification are distinct from native Windows 98 SE acceptance. The separately
verified VC6 build ZIP carries its own checksum manifest/report; it is not a
target accepted by the generic builder or distribution checker below.

## Windows stack reserve

The default MinGW PE stack reserve was too small for the existing 256-call
recursion limit: the initial Windows test crashed before reaching Claro's guard.
A 16 MiB stack reserve allowed the call-depth regression and full golden suite
to complete under Wine. Windows build scripts and the archive builder now set:

```text
-Wl,--stack,16777216
```

This reserves address space; pages are committed as needed. Use the Windows build
scripts, or include this setting when cross-compiling directly. It is a linker
requirement, not a claim that C89 source alone establishes OS portability.

## Verify the actual archives

```bash
python3 tools/validate_distribution.py /path/to/archive.zip --report /path/to/report.json
```

For Windows execution from Linux, first initialize a separate Wine prefix and supply
`--wine-prefix /path/to/isolated-prefix`. The checker will not silently use the default
Wine profile. Reports must have a new filename.

The checker extracts into a directory containing spaces, verifies every manifest
entry, checks executable format (including the Windows stack reserve), and executes:

- The executable alone, with a tiny script and no project files.
- `--version`, `doctor`, all packaged golden fixtures, and built-in validation.
- The exact introductory learning path and all nine First Hour examples.
- Full Python release validation for the source archive.

Source archive validation rebuilds within the extracted copy; it does not rely on
the development checkout's executable. Binary tests run the shipped binaries.

## Limits of the evidence

Wine verifies Windows executable/CRT behavior in a compatibility environment. It
is not native Windows acceptance, Windows 98/XP support, or an installer test.
The PE header's minimum subsystem version does not establish compatibility.

Likewise, static Linux linking removes a glibc-version dependency but does not prove
operation on every distribution, old kernel, CPU or architecture. ARM, 32-bit Linux, macOS, DOS and real older Windows systems require separate
builds and tests. The separate x86 MSVC6 compilation path does not establish
Windows 98 SE execution.

Real HTTP still requires curl. Offline networking fixtures need no Internet access.
Claro remains a trusted-script runtime, not a sandbox. Full validation is evidence
for the exercised behavior, not a claim that every possible script is correct.
