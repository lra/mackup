lint:
	# Install mdl with "gem install mdl"
	mdl .

test:
	poetry install --with dev
	poetry run pytest

clean:
	rm -rf __pycache__
	rm -rf mackup/__pycache__
	rm -rf tests/__pycache__
	rm -rf dist/

release: clean
	poetry build
	poetry publish

ruff:
	ruff check .
