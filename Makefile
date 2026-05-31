CC = gcc
CFLAGS = -std=c99 -O0
LDFLAGS = -lm

all: claro

claro: src/claro.c
	$(CC) $(CFLAGS) -o claro src/claro.c $(LDFLAGS)

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
