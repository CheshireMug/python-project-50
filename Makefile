install:
	uv sync

build:
	uv build

package-install:
	uv tool install --force dist/*.whl

lint:
	uv run ruff check gendiff

check:
	uv run ruff check gendiff
	uv run pytest

test-coverage:
	uv run pytest --cov=gendiff --cov-report xml gendiff
