# Claro Roadmap

Claro is a **learning tool first**, not a race to add language features.
The [learning-first charter](LEARNING_FIRST.md) guides every change.

## Active priorities

1. **Make the first hour dependable.** Execute every lesson example and check its output, including input and simple functions.
2. **Keep the rules consistent.** Teach one recommended syntax per concept; preserve older forms without putting alternatives in the first lessons.
3. **Help learners recover.** Errors should identify the relevant line, explain the problem plainly, and show a small correction.
4. **Teach in small steps.** One concept at a time, short exercises, and useful console projects such as quizzes, lists, and text-file tools.
5. **Keep the core reliable.** Fix crashes and incorrect behavior with focused regression tests. Keep existing safety checks and compatibility tests.
6. **Learn from real learners.** Test with people with different learning needs; record feedback without claiming accessibility has already been validated.

## Out of scope without a new request

Advanced type systems, complex object models, concurrency, web frameworks,
remote package registries, and new graphics systems. Existing implementations
are preserved, not removed.

## How work lands

Make one small, tested improvement at a time. Update the relevant guide and
run the [contributor checks](../CONTRIBUTING.md). A passing syntax check alone
is not proof that a teaching example works.

See [current status](CURRENT_STATUS.md) for implementation details.
The [previous roadmap](history/ROADMAP_BEFORE_LEARNING_FIRST.md) is retained
as history, not an active development checklist.
