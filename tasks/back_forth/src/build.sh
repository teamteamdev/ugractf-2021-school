#!/bin/sh

gcc -fPIC -Wall -c -o main.o main.c && gcc -fPIC -Wall -c -o flag.o flag.c && gcc -static -o main flag.o main.o
