# Testing Claro

Run the built-in regression suite:

```bash
./claro test
```

Expected result:

```text
PASS: 0 failure(s)
```

Check a lesson:

```bash
./claro check lessons/01_hello.claro
```

Validate the current v1.18.26 package after building:

```bash
./claro validate
python tools/validate_typecheck_diagnostics.py
python tools/validate_version_convention.py
```

Useful focused validation scripts:

```bash
python tools/validate_v1_17.py
python tools/validate_v1_16.py
python tools/validate_v1_15.py
python tools/validate_v1_14.py
python tools/validate_concurrency.py
python tools/validate_ide_metadata.py
python tools/validate_lsp_helper.py
python tools/validate_package_security.py
```

Older `validate_rc*.py` scripts are kept for historical release notes. They are not the recommended current package validation path.

On Windows, after `build.bat` or `build.ps1`, run the same Python commands from the project root.
