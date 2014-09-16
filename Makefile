develop:
	python setup.py develop

undevelop:
	python setup.py develop --uninstall

test:
	nosetests

clean:
	rm -rf dist/
	rm -rf Mackup.egg-info/

release: clean
	python setup.py sdist
	twine upload dist/*
