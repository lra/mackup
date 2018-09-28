develop:
	python setup.py develop

undevelop:
	python setup.py develop --uninstall

lint:
	# Install mdl with "gem install mdl"
	mdl .
	flake8

test:
	nosetests --with-coverage --cover-tests --cover-inclusive --cover-branches --cover-package=mackup

clean:
	rm -rf dist/
	rm -rf Mackup.egg-info/

release: clean
	python setup.py sdist
	twine upload dist/*
