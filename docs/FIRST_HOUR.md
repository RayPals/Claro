# Claro First Hour

This is a simple first-hour lesson path for new learners. Keep each lesson short. Let the learner run the program after every change.

## 1. Say hello

```claro
SAY "Hello!"
```

## 2. Ask a question

```claro
ASK "What is your name?" name
SAY "Hello " + name
```

Older examples may use `ASK "What is your name?" AS name`; that still works, but the shorter form is easier for new learners.

## 3. Store a variable

```claro
SET score 0
SAY score
```

## 4. Do simple math

```claro
SET score 0
SET score score + 1
SAY score
```

## 5. Make a decision

```claro
ASK "What is 2 + 2?" answer

IF answer = 4
    SAY "Correct!"
ELSE
    SAY "The answer is 4."
END
```

Simple number-looking input can compare naturally with numbers.

## 6. Repeat something

```claro
DO 3 TIMES
    SAY "Practice helps"
END
```

Older examples may use `DONE` for loop endings; that compatibility form still works.

## 7. Use a list

```claro
SET items LIST
ADD "milk" TO items
ADD "bread" TO items

FOR EACH item IN items
    SAY item
END
```

## 8. Teach a function

```claro
TEACH add a b
    RETURN a + b
END

DO add 2 3
SAY RESULT
```

Older examples may use `TEACH add TAKES a, b`, `LEARNED`, and `CALL add WITH 2, 3`; those forms still work.

## 9. Save and load text

```claro
WRITE FILE "note.txt" WITH "Hello"
READ FILE "note.txt" AS text
SAY text
```

## 10. Build a tiny quiz

Try `examples/quiz.claro`.
