# Claro Final Release Checklist

Before publishing `Claro v1.18.26` as the current stable release:

- Build from a clean unzip on Windows.
- Build from a clean unzip on Linux or macOS.
- Run `claro --version`.
- Run `claro test`.
- Run `claro validate`.
- Run every lesson that does not require user input.
- Manually test `examples/quiz.claro`.
- Manually test `examples/simple_functions.claro`.
- Manually test `examples/text_polish.claro`.
- Confirm the README shows the Claro logo.
- Confirm docs use the `v1.xx.yy` version format.
- Confirm beginner docs teach simple syntax first.
- Do not add large new systems before stable v1.

Avoid adding large new systems during a stability release; prioritize buildability, tests, documentation consistency, and beginner safety.
