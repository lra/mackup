develop:
	python setup.py develop

undevelop:
	python setup.py develop --uninstall

test:
	flake8 mackup
	nosetests --with-coverage --cover-tests --cover-inclusive --cover-branches --cover-package=mackup

clean:
	rm -rf dist/
	rm -rf Mackup.egg-info/

release: clean
	python setup.py sdist
	twine upload dist/*
