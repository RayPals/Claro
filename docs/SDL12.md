# SDL 1.2 Support Status

SDL 1.2 support is **not included in the current stable executable**.

The `examples/experimental_sdl/` files are design experiments / future examples only. In Claro v1.18.26, running them with the included `claro.exe` will fail with:

```text
Unknown command: SDL
```

## Current graphics status

The stable interpreter only accepts placeholder graphics-style commands such as `OPEN`, `CLEAR`, `DRAW`, `UPDATE`, and `CLOSE`. These do **not** open a real SDL window; they only mark graphics commands as accepted for beginner script compatibility.

## Planned SDL command shape

If SDL support is implemented later, the intended commands are:

- `SDL OPEN <w> <h> <title>`
- `SDL CLEAR <r> <g> <b>`
- `SDL RECT <x> <y> <w> <h> <r> <g> <b>`
- `SDL PRESENT`
- `SDL POLL`
- `SDL DELAY <ms>`
- `SDL CLOSE`
- `SDL LOADBMP <path> AS var`
- `SDL BLIT <handle> AT x y`
- `SDL BLITCLIP <handle> SRC sx sy sw sh AT x y`
- `SDL KEYDOWN <keycode> AS var`
- `SDL MOUSE AS mx my mb`

These are **planned/experimental**, not stable features yet.
