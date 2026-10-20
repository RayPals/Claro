CC = gcc
CFLAGS = -std=c89 -pedantic-errors -Werror=implicit-function-declaration -O0
LDFLAGS = -lm
ifeq ($(OS),Windows_NT)
LDFLAGS += -Wl,--stack,16777216
endif

all: claro claro.exe

claro: src/claro.c
	$(CC) $(CFLAGS) -o claro src/claro.c $(LDFLAGS)

claro.exe: src/claro.c
	$(CC) $(CFLAGS) -o claro.exe src/claro.c $(LDFLAGS)

test: claro
	./claro test

check: claro
	./claro check examples/quiz.claro
	./claro check lessons/01_hello.claro
	./claro check lessons/03_variables.claro
	./claro check lessons/08_functions.claro

fmt: claro
	./claro fmt tests/22_fmt_input.claro

clean:
	rm -f claro claro.exe
