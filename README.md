# Claro

<img src="assets/Claro_Logo.jpg" alt="Claro logo" width="160">

**Claro** is a small, readable scripting language for beginners. It is designed to make programming approachable without requiring punctuation-heavy syntax, while still providing a path toward functions, types, objects, files, packages, and networking.

Current release: **v1.18.26**

## Quick start

Build Claro with a C99 compiler and `make`:

```bash
make
```

Run a script:

```bash
./claro lessons/01_hello.claro
./claro examples/quiz.claro
```

Check a script without running it:

```bash
./claro check examples/quiz.claro
```

Run the built-in test suite and validation checks:

```bash
./claro test
./claro validate
```

Useful commands:

```text
claro help
claro --version
claro doctor
claro examples
claro repl
claro new MyProject
claro run
claro fmt file.claro
claro typecheck file.claro
```

## First Claro program

```claro
SAY "Hello from Claro!"

ASK "What is your name?" name
SAY "Hello " + name
```

Claro accepts both the short beginner-friendly form and older compatibility forms. For example, these are both valid:

```claro
SET name "Jon"
SET name TO "Jon"
```

## Core language features

### Decisions and loops

```claro
SET score 10

IF score >= 5
    SAY "Good job!"
ELSE
    SAY "Try again."
END

DO 3 TIMES
    SAY "Practice"
DONE
```

### Lists and maps

```claro
SET names AS LIST OF TEXT TO LIST
ADD "Ada" TO names
ADD "Grace" TO names

FOR EACH name IN names
    SAY name
DONE
```

### Functions

```claro
TEACH greet name
    SAY "Hello " + name
END

DO greet "Jon"
```

The older compatibility syntax remains supported:

```claro
TEACH greet TAKES name
    RETURN "Hello " + name
LEARNED

CALL greet WITH "Jon"
SAY RESULT
```

### Objects and classes

```claro
CLASS Player
    HAS name TEXT
    HAS score NUMBER

    TEACH add points
        SET score score + points
    END
END

NEW Player player
SET player.name "Jon"
SET player.score 10
DO player.add 5
SAY player.score
```

### Type checking

Type annotations are optional for beginners:

```claro
SET score NUMBER 10
SET name TEXT "Jon"
SET ready YESNO YES
CHECK TYPE score IS NUMBER
```

Run static checks with:

```bash
./claro typecheck examples/type_hardening.claro
```

Claro provides learner-facing diagnostics for many incorrect variable, function, method, and object-field types. For an explicitly typed object field, the separated form needs both `AS TYPE TO value`, so `SET player.score AS NUMBER` explains how to add `TO` and a value. Type checking is still a focused foundation rather than a complete static type system.

## Files, JSON, and standard helpers

Claro includes commands and libraries for practical scripts:

```claro
WRITE FILE "note.txt" WITH "Hello from Claro"
READ FILE "note.txt" AS note
SAY note
```

Standard-library modules include path and collection helpers:

```claro
IMPORT "lib/path.claro" AS path
CALL path.join WITH "notes", "today.txt"
SAY RESULT
```

See `docs/STDLIB.md` for the current helper API.

## Projects and packages

Create a project:

```bash
claro new MyProject
cd MyProject
claro run
```

Manage local project packages:

```bash
claro package init
claro package add text
claro package list
claro package doctor
claro package lock
```

Project metadata is stored in:

```text
claro.project
claro.lock
packages/
```

The current package system is local and foundational. Remote registries, publishing, version constraints, and package signature verification are not yet stable features.

## Networking

Claro supports beginner-oriented HTTP commands and offline `claro://` test URLs:

```claro
HTTP GET "claro://hello" AS page STATUS status
SAY page
SAY status
```

Real HTTP and HTTPS requests use `curl` when available. The offline URLs make networking lessons and tests deterministic.

## Current status

### Stable foundation

- Variables, output, input, expressions, and control flow
- Loops, lists, maps, text, JSON, and file operations
- Functions and compatibility syntax
- Friendly errors and script checking
- Path and collection helpers
- Offline networking examples

### Foundation present

- Static type checking
- Objects and classes
- Local projects and packages
- Networking beyond the offline test layer
- Cooperative tasks/concurrency helpers
- IDE metadata and completion helpers

These areas work in focused scenarios but still need broader coverage and polish.

### Experimental or planned

- Real SDL graphics and game-oriented graphics support
- Web-server syntax and routes
- Remote package registry
- Full editor extension/LSP support
- A complete concurrency scheduler

Do not treat experimental graphics as a stable cross-platform game runtime yet.

## Documentation map

Recommended reading order for new learners:

1. `docs/QUICK_START.md`
2. `docs/FIRST_HOUR.md`
3. `lessons/README.md`
4. `docs/CLI.md`
5. `docs/SPEC.md`
6. `docs/CURRENT_STATUS.md`

Useful references:

- `docs/ERRORS.md` — friendly diagnostics
- `docs/SIMPLE_FUNCTIONS.md` — function syntax
- `docs/STDLIB.md` — standard helpers
- `docs/TESTING.md` — test and validation workflow
- `docs/FORMATTER.md` — formatting scripts
- `docs/IDE.md` — editor metadata and helper support
- `docs/ROADMAP.md` — current development direction

Historical release notes are kept under `docs/RC*_*.md` and older `docs/V1_*_VALIDATION.md` files. They describe project history rather than the current beginner path.

## Development

The interpreter is implemented in `src/claro.c` and currently builds as a C99 program:

```bash
make
make test
make check
```

The repository includes examples, lessons, validation tools, and a test suite. Before submitting changes, run:

```bash
./claro test
./claro validate
```

## License

See [`LICENSE`](LICENSE) for the project license.
