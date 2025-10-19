lint:
	markdownlint -c .markdownlint.yaml '**/*.md'

test:
	uv run pytest

clean:
	rm -rf mackup/__pycache__
	rm -rf tests/__pycache__
	rm -rf dist/

release: clean
	uv build
	uv publish

ruff:
	ruff check .
