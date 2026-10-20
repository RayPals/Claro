# Claro's beginner syntax

Learn one spelling for each action. Use these same forms in the Quick Start,
First Hour, numbered lessons, and introductory examples.

- Show text: `SAY "Hello!"`
- Ask for input: `ASK "What is your name?" name`
- Store a value: `SET score 0`
- Change a value: `SET score score + 1`
- Make a list: `SET items LIST`
- Add an item: `ADD "milk" TO items`
- Make a choice: `IF condition`, optional `ELSE`, then `END`.
- Repeat a fixed number of times: `DO 3 TIMES`, then `END`.
- Visit list items: `FOR EACH item IN items`, then `END`.
- Define an action: `TEACH greet name`, then `END`.
- Run an action: `DO greet "Ada"`.
- Return an answer from an action: `RETURN value`; read it as `RESULT` after `DO`.
- Save text: `WRITE FILE "note.txt" WITH "Hello"`.
- Read text: `READ FILE "note.txt" AS note`.

## Small rules

1. Put one command on each line. Write keywords in uppercase in lessons to make
   them easy to spot; the interpreter also accepts lowercase keywords.
2. Put literal text in double quotes. Do not quote a variable when you want its value.
3. Use a simple name such as `score`, `name`, or `items` consistently.
4. Indent the body of a choice, loop, or action by four spaces for readability.
5. Close introductory `IF`, `DO ... TIMES`, `FOR`, and `TEACH` blocks with `END`.
6. Separate function parameters and simple call arguments with spaces.

`AS` is still part of commands that name a result, such as `READ FILE`.
`TO` is still part of `ADD item TO list`. The short forms above do not mean
removing those words from every command.

The optional `REPEAT` loop finishes with `UNTIL condition`, not `END`;
learn it after the introductory loops. Other advanced commands are outside this
first learning path.

Follow [First Hour](FIRST_HOUR.md) for complete programs and the
[numbered lessons](../lessons/README.md) for practice. Older spellings still run;
[compatibility syntax](COMPATIBILITY.md) is only needed when reading older programs.
