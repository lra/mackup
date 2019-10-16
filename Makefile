develop:
	pipenv run python setup.py develop

undevelop:
	pipenv run python setup.py develop --uninstall

lint:
	# Install mdl with "gem install mdl"
	mdl .

test:
	pipenv run nosetests --with-coverage --cover-tests --cover-inclusive --cover-branches --cover-package=mackup

clean:
	rm -rf dist/
	rm -rf Mackup.egg-info/

release: clean
	pipenv run python setup.py sdist
	pipenv run twine upload dist/*

black:
	black --target-version py27 .
