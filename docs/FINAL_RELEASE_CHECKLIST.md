# Claro Final Release Checklist

Before publishing `Claro v1.10.26` as the first stable release:

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

Large features such as SDL, classes, packages, networking, threads, strong static types, and IDE tooling should come after the first stable v1 foundation.
