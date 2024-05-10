# This is a simple makefile

	CC=gcc
	CFLAGS=-g -Wall

ush: ush.o expand.o builtin.o
	$(CC) $(CFLAGS) -o ush ush.o expand.o builtin.o

ush.o: ush.c builtin.h
	$(CC) $(CFLAGS) -c ush.c

expand.o: expand.c builtin.h
	$(CC) $(CFLAGS) -c expand.c

builtin.o: builtin.c builtin.h
	$(CC) $(CFLAGS) -c builtin.c

clean:
	rm -f ush ush.o expand.o builtin.o
