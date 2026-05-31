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

Validate an RC3 package after building:

```bash
python tools/validate_rc3.py
```

On Windows, after `build.bat` or `build.ps1`:

```powershell
python toolsalidate_rc3.py
```
