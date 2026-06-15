lint:
	uv run rumdl check .

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

# Cut a release in one command. Bumps the version, syncs the lockfile, then
# commits, tags and pushes. The release workflow takes over from the tag push.
# Bump level defaults to patch: `make release BUMP=minor` / `BUMP=major`,
# or pin a version with `make release VERSION=1.2.3`.
BUMP ?= patch

release: check
	@if [ -n "$(VERSION)" ]; then uv version "$(VERSION)"; else uv version --bump $(BUMP); fi
	uv sync -U
	@V=$$(uv version --short); \
	git commit -am "Mackup $$V" && \
	git tag "$$V" && \
	git push && \
	git push --tags && \
	echo "Released $$V"
