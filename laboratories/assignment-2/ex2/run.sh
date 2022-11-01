#!/bin/bash

lex -o ex.c ex.l
gcc ex.c -o ex.out
cat ./test_file.py | ./ex.out 