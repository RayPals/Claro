# Beginner pilot — observer kit

**Status: prepared, not learner-validated.** No participant feedback has been
collected by these automated checks. Do not infer accessibility from test passes.

Ask for willing participation and permission to keep anonymous notes. Explain
that we are testing the instructions, not the person. Collect no diagnosis,
medical history, real names or sensitive information. Let the learner decline,
ask for help, take breaks or stop. Use any assistive technology they prefer.

Use a platform-tested build, a fresh writable practice folder and reviewed scripts.
Show how to stop/close the interpreter before starting. Do not run downloaded
untrusted scripts. Explain that optional limits are not a sandbox.

Try the first three tasks at the learner's pace. Offer the rest only if wanted.
Let the learner predict, run and change the program. Observe before giving a
hint; never leave someone distressed just to measure independence. Record help
without judging it. Answers/output for observers are in `tests/learner_pilot.json`.

## Say hello

Run this once. Change the message to something you choose and run it again.

```claro
SAY "Hello!"
```

## Ask a name

Run it and type a pretend name. Explain where that name is remembered.

```claro
ASK "Name? " name
SAY "Hello " + name
```

## Change a number

Predict the result, run it, then change 2 to another small number.

```claro
SET score 2
SAY score + 1
```

## Make a choice

Optional: change score to 0. Predict which message appears.

```claro
SET score 2
IF score > 1
    SAY "More than one"
ELSE
    SAY "One or less"
END
```

## Repeat

Optional: change how many times the message appears. Ask how to stop a stuck run.

```claro
DO 3 TIMES
    SAY "Again"
END
```

## Save a file

Optional: use a new writable practice folder. Find the file after running it.

```claro
WRITE FILE "practice.txt" WITH "My first file"
READ FILE "practice.txt" AS text
SAY text
```

## Gentle mistake and recovery

In the hello task, replace SAY with PRNT, run `claro check practice.claro`, and
ask what the message suggests. Restore SAY and rerun. This mistake is optional;
skip it if it adds stress. Do not teach alternative compatibility spellings here.

## Debrief and next change

Ask: What was clear? What was confusing? What would you change? Observe whether
the person can start/run/save, predict a result and use a repair hint. Do not
calculate a disability score or call one session proof of universal accessibility.
Use [the blank feedback form](LEARNER_FEEDBACK_TEMPLATE.md); keep only consented,
anonymous notes, record the exact build/platform, and choose one small improvement.
The [classroom checklist](CLASSROOM_READINESS.md) is a pilot guide, not certification.
