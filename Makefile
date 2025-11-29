lint:
	markdownlint -c .markdownlint.yaml '**/*.md'

ruff:
	ruff check .

test:
	uv run pytest

coverage:
	uv run pytest --cov=mackup --cov-report=term --cov-report=html --cov-report=xml

coverage-report:
	uv run coverage report

mypy:
	uv run mypy src/mackup/

check: lint ruff mypy test
	@echo "All checks passed!"

clean:
	rm -rf src/mackup/__pycache__
	rm -rf tests/__pycache__
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml

release: clean
	uv build
	uv publish
