# Claro Standard Library (Commands)

Claro’s “stdlib” is exposed as readable commands.

## TEXT

### Split
```claro
TEXT SPLIT "a,b,c" BY "," AS parts
```

### Join
```claro
TEXT JOIN parts BY "-" AS out
```

### Replace all
```claro
TEXT REPLACE "one two two" FROM "two" TO "three" AS out
```

## PATH

### Dirname
```claro
PATH DIRNAME "C:/games/save/file.txt" AS dir
```

### Normalize
Unifies slashes and removes `.` / `..` where possible:
```claro
PATH NORMALIZE "../data/./levels/../sprites" AS clean
```

### Is absolute
```claro
PATH ISABS "/home/me/file.txt" AS isAbs
```

### Exists
Checks if a file exists at the path:
```claro
PATH EXISTS "config.json" AS ok
```

## TIME

### Unix seconds
```claro
TIME NOW AS t
```

### Unix milliseconds (coarse)
```claro
TIME NOWMS AS ms
```
