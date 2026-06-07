# Claro Cooperative Concurrency

Claro's first concurrency foundation is intentionally small, beginner-friendly, and deterministic.

## Design goals

- **Cooperative**, not preemptive: a task only gives control back at clear points such as `YIELD`, `WAIT TASK`, or the end of the task block.
- **Deterministic**: the same program should run in the same order every time while Claro grows toward richer scheduling.
- **No native threads** yet: this foundation does not use operating-system threads, shared-memory races, locks, or parallel CPU execution.
- **Easy status checks**: learners can ask whether a task is `DONE` or still `PENDING` without learning low-level threading concepts.

## Current syntax

```claro
START TASK helloTask
    SAY "Inside task"
    YIELD
ENDTASK

TASK STATUS helloTask AS status
SAY status

WAIT TASK helloTask
```

## Commands

- `START TASK name ... ENDTASK` starts a named cooperative task block. In this foundation, the block runs deterministically and marks the task as done when it finishes.
- `YIELD` is accepted as an explicit cooperative scheduling point. It is currently a safe no-op, reserved for future round-robin scheduling.
- `TASK STATUS name AS variable` stores `DONE` when the named task has completed, otherwise `PENDING`.
- `WAIT TASK name` is accepted as the beginner-friendly wait command. It is currently deterministic because the task has already run by the time the line is reached.

## Why not real threads yet?

Real native threads add race conditions, locks, deadlocks, timing bugs, and platform differences. Claro is designed for beginners, including people with learning disabilities, so the first stable slice focuses on readable syntax, validation, documentation, and predictable behavior before adding true parallelism.

Future slices can build on this foundation with a real cooperative task queue, cancellation, timeouts, and safe message passing.
