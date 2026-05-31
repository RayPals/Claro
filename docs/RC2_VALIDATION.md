# Claro RC2 Validation

Validated commands:

```bash
gcc -std=c99 src/claro.c -O0 -o claro -lm
./claro --version
./claro test
```

Expected result:

```text
Claro RC2
PASS: 0 failure(s)
```

Manual Windows equivalent:

```powershell
gcc -std=c99 src\claro.c -O0 -o claro.exe -lm
.\claro.exe --version
.\claro.exe test
```

Interactive smoke test:

```powershell
.\claro.exe examples\quiz.claro
```

Use answers like:

```text
Johnathan
4
10
```

Expected final score:

```text
2
Great job!
```
