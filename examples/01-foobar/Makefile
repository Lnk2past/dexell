CC:=g++
CFLAGS:=-rdynamic

PYTHON:=python
DEXELL:=../../dexell.py

main.exe: main.cpp
	$(CC) $(CFLAGS) $< -o $@

test: main.exe
	$(PYTHON) $(DEXELL) $< "foo"
	$(PYTHON) $(DEXELL) $< "bar()"

clean:
	rm -rf main.exe

.PHONY: test clean
