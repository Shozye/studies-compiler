#!/bin/bash

lexe=./ex.l
cexe=./ex.c
exe=./ex.out

test_dir=./tests
test=$test_dir"/test.py"

parsed=$test_dir"/parsed_test.py"
output=$test_dir"/parsed_execute.txt"

lex -o $cexe $lexe
gcc $cexe -o $exe
cat $test | ./ex.out > $parsed
python $parsed > $output
rm $cexe $exe
