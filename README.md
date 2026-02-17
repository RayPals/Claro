# Claro 1.0 - Release Candidate

Beginner-friendly programming for everyone.

Claro is a simple, readable programming language designed for:

- new programmers  
- classrooms  
- people with learning differences  

It uses clear, English-style commands and friendly error messages so you can focus on learning and creating.

---

## Repository

https://codeberg.org/RayPals/Claro

---

## Features

- Easy to read and write
- English-like syntax
- Friendly error messages
- Simple loops and decisions
- Reusable functions (`TEACH`, `CALL`, `RETURN`)
- Beginner game objects (sprites)
- Classroom-safe mode
- Portable — no installation required

---

## Running Claro

Interactive mode:

    claro

Run a program:

    claro program.claro

Classroom safe mode:

    claro --classroom program.claro

---

## Your First Program

Create a file called `hello.claro`

    SAY "Hello, world!"

Run it:

    claro examples/hello.claro

---

## Core Commands

SAY — show output  
ASK — get input  
SET — store data  
IF — make decisions  
DO — repeat  
WAIT — pause  

---

## Functions with TEACH

    TEACH add TAKES a, b
        RETURN a + b
    LEARNED

    CALL add WITH 2, 3
    SAY RESULT

---

## Sprites

    CREATE SPRITE player
    MOVE SPRITE player TO 10 5
    SHOW SPRITE player
    HIDE SPRITE player

---

## Building from Source

Linux / macOS:

    gcc src/claro.c -O2 -o claro

Windows (MinGW):

    gcc src/claro.c -O2 -o claro.exe

---

## Contributing

https://codeberg.org/RayPals/Claro/issues

---

## License

MIT
