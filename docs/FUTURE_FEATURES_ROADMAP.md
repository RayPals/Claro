# Claro Future Features Roadmap

Current status: **historical implementation plan plus remaining ideas**.

This file began as a task-by-task plan. Some early slices have since been completed or moved into current feature docs. For the current learner-facing truth, start with `CURRENT_STATUS.md`, `ROADMAP.md`, and `COMPLETE_PLATFORM_ROADMAP.md`.

Already moved into current foundations:

- typed list/map checking and clearer type mismatch diagnostics
- IDE metadata and the command-based diagnostics helper
- deterministic cooperative task commands
- HTTP client safety with offline `claro://` test URLs
- local project/package manifest and lockfile hardening

Still planned or experimental:

- real web server API
- remote package registry/install flow
- full editor extension/LSP experience
- optional SDL graphics backend
- optimization work backed by benchmarks

**Goal:** Grow Claro from a beginner scripting language into a stable accessible platform without breaking the learning-friendly core.

**Architecture:** Keep the interpreter small and stable. Add major systems behind explicit commands, feature flags, and testable layers. Prefer beginner-readable commands first, then deeper professional tooling around them.

**Tech Stack:** C99 interpreter, `.claro` tests/golden outputs, optional helper tools in Python, optional platform libraries such as SDL only after isolated build support exists.

---

> Current note: this is not the beginner starting path. Use it for remaining implementation ideas only after checking `CURRENT_STATUS.md`.

## Priority order

1. **Advanced static typing foundation** — safest immediate win; improves learner feedback and catches mistakes before running.
2. **Professional IDE foundations** — language metadata, diagnostics, formatter, LSP/documentation support.
3. **Concurrency as real runtime feature** — cooperative tasks first; avoid native threads until semantics are clear.
4. **Production-grade web programming** — HTTP primitives, JSON, routing/server design after safety model.
5. **GUI/game engine features** — separate stable placeholder graphics from real optional SDL/GUI backends.
6. **Online package registry** — design package metadata/security before network install.
7. **Advanced compiler optimization** — only after semantics stabilize; start with bytecode/AST planning, not premature optimization.

---

## Track A: Advanced Static Typing

### Task A1: Add typed LIST and MAP declarations

**Objective:** Accept and check beginner-readable container type declarations such as `SET names LIST OF TEXT` and `SET scores MAP OF NUMBER`.

**Files:**
- Modify: `src/claro.c`
- Test: `tests/40_static_container_good.claro`
- Test: `tests/40_static_container_good.out`
- Test: `tests/typecheck_container_bad.claro`

**Steps:**
1. Add a failing good test with `LIST OF TEXT` and `MAP OF NUMBER` declarations.
2. Add a failing bad typecheck test where a `LIST OF NUMBER` receives text.
3. Teach `claro_is_type_word`, `claro_type_matches`, and the typecheck parser to preserve simple container annotations.
4. Verify `claro test` and `claro typecheck tests/typecheck_container_bad.claro`.

### Task A2: Add clearer type mismatch messages

**Objective:** Make type errors explain the variable, expected type, actual value kind, and line number in plain language.

**Files:**
- Modify: `src/claro.c`
- Test: `tests/typecheck_bad.claro`

**Steps:**
1. Capture current bad output.
2. Improve wording without changing successful behavior.
3. Update tests/docs only after verifying the new wording is clearer.

---

## Track B: Professional IDE Foundations

### Task B1: Expand `claro ide` JSON

**Objective:** Output commands, snippets, type names, and file extension metadata for editor plugins.

**Files:**
- Modify: `src/claro.c`
- Test: `tests/41_ide_metadata.claro` or a CLI validation script.

**Steps:**
1. Add expected JSON fields: `commands`, `snippets`, `diagnostics`, `version`.
2. Validate with Python `json.loads`.
3. Document in `docs/IDE.md`.

### Task B2: Build minimal LSP helper

**Objective:** Provide a Python helper that reads Claro files and returns diagnostics using `claro check`/`typecheck`.

**Files:**
- Create/modify: `support/lsp/claro_lsp_stub.py`
- Create: `docs/IDE.md`

---

## Track C: Real Concurrency

### Task C1: Define cooperative task semantics

**Objective:** Document `START TASK`, `YIELD`, `WAIT TASK`, and `TASK STATUS` without native threads.

**Files:**
- Create: `docs/CONCURRENCY.md`
- Test: future `tests/42_tasks_cooperative.claro`

**Rule:** Start cooperative scheduling before OS threads. This keeps beginner programs deterministic.

---

## Track D: Web Programming

### Task D1: Stabilize HTTP client commands

**Objective:** Keep `HTTP CHECK`, `HTTP GET`, and `HTTP SAVE` predictable and testable with `claro://` URLs.

**Files:**
- Modify: `docs/WEB_SERVER_PLAN.md`
- Tests: existing networking tests

### Task D2: Design local web server syntax

**Objective:** Propose beginner-friendly server syntax, but do not implement sockets until parser/runtime tests are ready.

Example future shape:

```claro
WEB SERVER 8080
WEB GET "/" DO home
TEACH home request
    RETURN "Hello"
END
WEB START
```

---

## Track E: GUI/Game Engine

### Task E1: Separate placeholder graphics from real SDL

**Objective:** Keep stable no-op graphics commands documented separately from optional SDL backends.

**Files:**
- Modify: `docs/SDL12.md`
- Create: `docs/GRAPHICS.md`

### Task E2: Optional SDL prototype branch

**Objective:** Only after build scripts can find SDL 1.2 reliably, add `CLARO_WITH_SDL12` support behind a compile flag.

---

## Track F: Online Package Registry

### Task F1: Define package manifest and lock security

**Objective:** Design package metadata, versions, hashes, and allowed sources before downloads.

**Files:**
- Create: `docs/PACKAGE_REGISTRY.md`

**Rule:** No online package install until hash verification and safe paths are implemented.

---

## Track G: Optimization

### Task G1: Add timing benchmark command

**Objective:** Measure before optimizing.

**Files:**
- Create: `tests/benchmarks/`
- Create: `docs/PERFORMANCE.md`

**Rule:** No optimizer work without benchmarks.
