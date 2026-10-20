# Classroom pilot checklist

**Status: ready for supervised learner testing, not classroom certification.**
Accessibility for learners with learning disabilities is a design goal and is
**not yet validated** by intended learners. Passing tests does not establish it.
Use [current status](CURRENT_STATUS.md) for scope, not older feature roadmaps.

## Before a session

- Use a build whose platform was actually tested; check `claro --version`.
  On the legacy Windows build the executable is `claro98.exe`.
- Run `claro test` and `claro validate` in the extracted project folder.
- Prepare a writable practice folder and explain how to stop/close a stuck run.
- Use only reviewed, trusted scripts. Claro is not a sandbox and runs with the
  learner's permissions; do not collect sensitive information in exercises.

## Observe the first hour

1. Run [hello](../lessons/01_hello.claro) and change its message.
2. Try [input](../lessons/02_ask_name.claro), variables and simple arithmetic.
3. Introduce one decision, then one small loop, at the learner's pace.
4. Follow the [ten lessons](../lessons/README.md) and [first-hour guide](FIRST_HOUR.md).
5. Try a small quiz; ask the learner to explain what changed and why.
6. Introduce a harmless mistake, run `claro check`, and observe whether the
   message identifies the right line and suggests an understandable repair.

Show one recommended spelling per concept. Do not introduce classes, typing,
packages, networking, concurrency or graphics as prerequisites to first programs.

## Record feedback

- Can the learner start, run, change and save a program without repeated coaching?
- Which instructions, words, prompts or errors cause confusion?
- Are examples short enough? Is the expected output obvious?
- Can the learner recover from a mistake and understand what a loop does?
- What presentation, pacing or assistive-technology adjustments help this person?

Record observations without claiming one design suits every disability. Get
consent before retaining feedback and avoid unnecessary personal/health data.
Make one small improvement, then repeat learner testing.

Platform checks, hosted release verification and accessibility feedback are
separate milestones. See [release status](RELEASE_STATUS.md).
