lint:
	markdownlint -c .markdownlint.yaml '**/*.md'

test:
	poetry install --with dev
	poetry run pytest

clean:
	rm -rf mackup/__pycache__
	rm -rf tests/__pycache__
	rm -rf dist/

release: clean
	poetry build
	poetry publish

ruff:
	ruff check .
