# Claro Formatter

Run:
```bash
claro fmt file.claro
claro fmt file.claro --inplace
```

## What it does (Beta18)
- Removes trailing whitespace
- Normalizes indentation for common block structures:
  - TEACH/LEARNED
  - IF/ELSE/ENDIF
  - FOR/DONE
  - TRY/CATCH/ENDTRY
  - DO/DONE
  - REPEAT/UNTIL
  - COMMENT/ENDCOMMENT

Indentation step is 4 spaces.

## What it does NOT do yet
- Reflow long lines
- Rename variables
- Enforce style beyond indentation and whitespace
