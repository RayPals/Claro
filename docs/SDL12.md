# SDL 1.2 Support (Optional)

Claro can be built with optional SDL 1.2 support for simple 2D graphics and input.

## Build (MinGW example)

Install SDL 1.2 development files, then compile with:

```sh
gcc -DCLARO_WITH_SDL12=1 -I<SDL_INCLUDE_DIR> src/claro.c -L<SDL_LIB_DIR> -lSDL -mwindows -O2 -o claro.exe
```

On some setups you may need `-lSDLmain` too.

## Commands

All SDL commands are grouped under `SDL ...`:

- `SDL OPEN <w> <h> <title>`
- `SDL CLEAR <r> <g> <b>`
- `SDL RECT <x> <y> <w> <h> <r> <g> <b>` (filled rectangle)
- `SDL PRESENT`
- `SDL POLL` (updates variables `SDLEVENT` and `SDLKEY`)
- `SDL DELAY <ms>`
- `SDL CLOSE`

### Event variables

After `SDL POLL`, Claro variables update:

- `SDLEVENT` = `"NONE" | "QUIT" | "KEYDOWN" | "KEYUP" | "OTHER"`
- `SDLKEY` = key code number (SDLKey) for KEYDOWN/KEYUP, otherwise `0`

## Sprite / bitmap support

- `SDL LOADBMP <path> AS var` → loads a BMP and stores a numeric handle in `var`
- `SDL BLIT <handle> AT x y` → draws the loaded bitmap at x,y
- `SDL KEYDOWN <keycode> AS var` → sets var to 1/0 based on current key state

- `SDL BLITCLIP <handle> SRC sx sy sw sh AT x y` → blit part of a surface (sprite-sheet)
- `SDL MOUSE AS mx my mb` → writes mouse x/y and button bitmask
