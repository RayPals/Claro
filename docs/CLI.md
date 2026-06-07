# Claro Command Line

Claro v1.18.26 supports these main commands:

```bash
claro file.claro
claro run
claro test
claro check file.claro
claro fmt file.claro
claro repl
claro new MyProject
claro examples
claro doctor
claro validate
claro package init|add|remove|list|doctor|lock
claro ide
claro --version
claro help
```

## Run a file

```bash
claro examples/hello.claro
```

## Run a project

If the current folder has `claro.project`, `claro run` uses its `main:` setting. Otherwise it tries `main.claro`:

```bash
claro run
```

## Test the package

```bash
claro test
```

## Stable package validation

```bash
claro validate
```

This runs package health checks, built-in tests, and checker passes over the lessons and main examples.

## Package starter

```bash
claro package init
claro package add text
claro package remove text
claro package list
claro package doctor
claro package lock
```

The v1.18.26 package command is a safer local project-file helper. It creates `claro.project`, `claro.lock`, and local folders under `packages/`. It is not yet an online package registry.

## IDE metadata

```bash
claro ide
```

This prints simple keyword/type metadata that future editor plugins can use.

## Type checking

```bash
claro typecheck my_script.claro
```

Checks simple typed variables such as `SET score NUMBER 10` before running the script.
