.PHONY: install dev lint test

install:
 	make -C backend install
	make -C frontend install

dev:
	make -C backend dev & make -C frontend dev; wait

lint:
	make -C backend lint
	make -C frontend lint

test:
	make -C backend test
	make -C frontend test
	make -C frontend e2e
