# Claro RC2 Notes

> Historical note: this file is kept for release history. The current package is Claro v1.18.26; use `CURRENT_STATUS.md`, `ROADMAP.md`, and the current feature docs for up-to-date beginner guidance.


RC2 is the Beginner Polish Release.

## Main changes

### Natural ASK prompts

RC1 could read input, but examples often used a separate `SAY` line before `ASK`.

RC2 supports the natural beginner form:

```claro
ASK "What is your name?" AS name
```

### Easier number input

User input is still stored as text, but RC2 treats number-looking text naturally in simple comparisons and basic math:

```claro
ASK "What is 2 + 2?" AS answer

IF answer = 4
    SAY "Correct!"
ENDIF
```

```claro
SET a TO "4"
SET b TO "6"
SAY a + b
```

prints:

```text
10
```

### More beginner examples

The examples folder now includes a clearer first path for learners:

- `hello.claro`
- `name_input.claro`
- `quiz.claro`
- `guessing_game.claro`
- `shopping_list.claro`
- `save_and_load_file.claro`
- `functions_example.claro`

## Still not final 1.0

RC2 is for testing and feedback. The next milestone should focus on documentation polish, fuller checker coverage, and final package cleanup.
