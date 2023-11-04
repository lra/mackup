lint:
	# Install mdl with "gem install mdl"
	mdl .

test:
	poetry install --with dev
	poetry run nosetests --with-coverage --cover-branches --cover-package=mackup

clean:
	rm -rf __pycache__
	rm -rf dist/
	rm -rf Mackup.egg-info/

release: clean
	poetry build
	poetry publish

black:
	black --target-version py310 .
