# Classroom Readiness Checklist

Claro v1.18.26 is suitable for beginner classroom-style testing of the stable console-language foundation. Advanced platform features should still be introduced carefully and only after the basics are comfortable.

## Ready to test

- Beginner console programs
- Interactive examples
- Variables, math, choices, loops, lists, maps, functions
- Simple files and JSON
- Friendly `check` command
- Windows and Linux/macOS build paths
- Local project/package workflow basics
- Offline networking lessons with `claro://` URLs

## Use with caution

- Advanced scripts
- Large programs
- Graphics/game examples
- Remote networking examples
- Package registry or publishing workflows
- Concurrency examples beyond documented safe task patterns

## Recommended testing session

1. Build Claro or use the included executable.
2. Run `claro --version` and confirm `Claro v1.18.26`.
3. Run `claro test`.
4. Run `claro validate`.
5. Run `lessons/01_hello.claro`.
6. Run `lessons/02_ask_name.claro`.
7. Run `examples/quiz.claro`.
8. Deliberately mistype `SAY` as `PRNT` and run `claro check`.
9. Try one foundation feature example, such as `examples/objects_classes.claro` or `examples/networking.claro`.
