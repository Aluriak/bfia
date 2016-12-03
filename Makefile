
GCC_OPTIONS=-fsigned-char -Wall -Werror -O3 -flto

all: compile
	python __main__.py

compile: bfinterp.c bfinterp.h compare_str.c
	# build the so's
	gcc -shared -o bfinterp.so -fPIC bfinterp.c $(GCC_OPTIONS)
	gcc -shared -o compare_str.so -fPIC compare_str.c $(GCC_OPTIONS)
	# build the standalone module
	gcc -o bfinterp -fPIC main.c bfinterp.c $(GCC_OPTIONS)

t: test
test: compile
	pytest test_*.py --doctest-modules --ignore=venv
