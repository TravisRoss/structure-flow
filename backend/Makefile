.PHONY: install dev test

install:
	uv sync --extra dev

dev:
	uv run uvicorn app.main:app --reload --port 8000

test:
	uv run pytest
