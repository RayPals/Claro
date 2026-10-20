# Compatibility syntax

You do not need these spellings for your first programs. Learn the
[recommended beginner syntax](SYNTAX.md) first. These older forms remain
supported so existing scripts do not break.

- Older `SET score TO 8` means the same as `SET score 8`.
- Older `ASK "Number?" AS answer` means the same as `ASK "Number?" answer`.
- Older `ENDIF`, `DONE`, and `LEARNED` close choices, loops, and functions;
  the beginner path uses `END` for all three.
- Older `TEACH add TAKES a, b` and `CALL add WITH 2, 3` correspond to
  `TEACH add a b` and `DO add 2 3`.

This complete older-style program is covered by an executable compatibility test:

```claro
TEACH add TAKES a, b
    RETURN a + b
LEARNED
CALL add WITH 2, 3
SAY RESULT
SET score TO 8
ASK "Number?" AS answer
IF answer = 4
    DO 2 TIMES
        SAY score
    DONE
ELSE
    SAY "no"
ENDIF
```

Enter `4`. It prints `5`, asks `Number?`, then prints `8` twice.

Do not automatically replace every `AS` or `TO`: commands such as
`READ FILE "note.txt" AS note` and `ADD "milk" TO items` still need those words.
