CC = gcc
CFLAGS = -Wall -Iinclude
OBJ = obj/main.o obj/vector.o obj/translate.o

all:bin/main

bin/main: $(OBJ)
	mkdir -p bin
	$(CC) $(CFLAGS) -o bin/main $(OBJ)

obj/main.o: src/main.c include/learn_english.h
	mkdir -p obj
	$(CC) $(CFLAGS) -c src/main.c -o obj/main.o

obj/vector.o: src/vector.c include/learn_english.h
	mkdir -p obj
	$(CC) $(CFLAGS) -c src/vector.c -o obj/vector.o

obj/translate.o: src/translate.c include/learn_english.h
	mkdir -p obj
	$(CC) $(CFLAGS) -c src/translate.c -o obj/translate.o


.PHONY: clean run

clean:
	rm -f obj/*.o bin/main

run: bin/main
	./bin/main $(FILE)