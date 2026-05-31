# Imports in Claro

## Basic
```claro
IMPORT "lib/text.claro" AS text
```

## How paths resolve
When you write `IMPORT "something.claro"` Claro searches in this order:

1. Relative to the importing file’s folder  
2. Each folder listed in the `CLARO_PATH` environment variable  
   - separate entries with `;` or `:`  
3. The current working directory

## CLARO_PATH example

### Windows
```bat
set CLARO_PATH=C:\claro\lib;C:\mygame\scripts
```

### Linux/macOS
```sh
export CLARO_PATH=/opt/claro/lib:/home/me/project/scripts
```
