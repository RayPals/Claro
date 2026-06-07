# Claro RC3 Notes

> Historical note: this file is kept for release history. The current package is Claro v1.18.26; use `CURRENT_STATUS.md`, `ROADMAP.md`, and the current feature docs for up-to-date beginner guidance.


Claro RC3 is the **Classroom Readiness Release**.

RC3 does not try to make Claro bigger. It makes the existing beginner language easier to teach, test, and package.

## New in RC3

- Version now reports `Claro RC3`.
- Added a `lessons/` folder with a first-hour learning path.
- Added `build.bat` and `run_tests.bat` for Windows users who do not want to use PowerShell scripts.
- Updated `build.ps1` for RC3.
- Improved `claro check` diagnostics:
  - better command typo suggestions, such as `PRNT` -> `SAY`
  - missing block messages point back to the line where the block started
  - `ELSE` without `IF` and `CATCH` without `TRY` are reported
  - `TEACH` parameters are understood by the checker
  - `FOR` loop variables and `FOR EACH` variables are understood by the checker
  - `GET`, `COUNT`, `ASK`, file/JSON commands with `AS` are tracked as variables
- Added more beginner example programs.
- Added `tools/validate_rc3.py` for release validation.

## RC3 focus

RC3 is meant for learners, teachers, parents, and testers to try Claro without running into avoidable setup and beginner-error problems.

## Still not final 1.0

- SDL graphics remain experimental only.
- No package manager yet.
- No IDE extension yet.
- The checker is helpful but not a complete static analyzer.
