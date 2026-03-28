.PHONY: install dev test lint

install:
	uv sync --extra dev

dev:
	uv run uvicorn app.main:app --reload --port 8000

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run mypy app
