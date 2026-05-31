# Claro RC1 Validation

Validation performed for this package:

```text
gcc -std=c99 src/claro.c -O0 -o claro -lm
./claro --version
Claro RC1

./claro test
PASS: 0 failure(s)
```

The regression suite covers:

- output
- expressions
- variables
- functions
- imports
- namespaced imports
- exports
- lists
- maps
- loops
- file read/write/delete/exists
- JSON parsing
- JSON pretty output
- TRY/CATCH
- RAISE
- import cycle errors
- text/math/random/CSV stdlib behavior
- no-op sprite teaching commands
