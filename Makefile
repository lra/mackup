MDL_PATH := $(shell command -v markdownlint 2> /dev/null)

lint:
ifdef MDL_PATH
	markdownlint -c .markdownlint.yaml '**/*.md'
else
	$(warning "[WARN] No 'markdownlint' utility in PATH. Consider installing it from your package manager.")
	$(warning "[WARN] Markdown linting has been skipped.")
endif

ruff:
	uv run ruff check .

ty:
	uv run ty check

test:
	uv run pytest

coverage:
	uv run pytest --cov=mackup --cov-report=term --cov-report=html --cov-report=xml

coverage-report:
	uv run coverage report

mypy:
	uv run mypy src/mackup/

check: lint ruff mypy ty test
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
