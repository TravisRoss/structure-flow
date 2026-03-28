.PHONY: install dev lint

install:
	make -C backend install
	make -C frontend install

dev:
	make -C backend dev & make -C frontend dev; wait

lint:
	make -C backend lint
	make -C frontend lint
