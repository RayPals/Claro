# Claro First Hour

This is a simple first-hour lesson path for new learners. Keep each lesson short. Let the learner run the program after every change.

## 1. Say hello

```claro
SAY "Hello!"
```

## 2. Ask a question

```claro
ASK "What is your name?" AS name
SAY "Hello " + name
```

## 3. Store a variable

```claro
SET score TO 0
SAY score
```

## 4. Do simple math

```claro
SET score TO 0
SET score TO score + 1
SAY score
```

## 5. Make a decision

```claro
ASK "What is 2 + 2?" AS answer

IF answer = 4
    SAY "Correct!"
ELSE
    SAY "The answer is 4."
ENDIF
```

In RC2, simple number-looking input can compare naturally with numbers.

## 6. Repeat something

```claro
DO 3 TIMES
    SAY "Practice helps"
DONE
```

## 7. Use a list

```claro
SET items TO LIST
ADD "milk" TO items
ADD "bread" TO items

FOR EACH item IN items
    SAY item
DONE
```

## 8. Teach a function

```claro
TEACH add TAKES a, b
    RETURN a + b
LEARNED

CALL add WITH 2, 3
SAY RESULT
```

## 9. Save and load text

```claro
WRITE FILE "note.txt" WITH "Hello"
READ FILE "note.txt" AS text
SAY text
```

## 10. Build a tiny quiz

Try `examples/quiz.claro`.
