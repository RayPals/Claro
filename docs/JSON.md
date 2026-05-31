# JSON in Claro

## Parse JSON text
```claro
PARSE JSON myText AS value
```

If JSON is invalid, Claro reports the character offset and a short snippet near the error.

## Make JSON text
```claro
MAKE JSON value AS text
```

### Pretty JSON
```claro
MAKE JSON PRETTY value AS text
```

Pretty output is easier to read for config files and debugging.
