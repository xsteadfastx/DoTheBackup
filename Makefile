.PHONY: build clean editable pypi test

build:
	python setup.py sdist bdist_wheel

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -rf .tox

editable:
	pip install --editable .

pypi:
	python setup.py register -r pypi
	python setup.py sdist bdist_wheel upload -r pypi

test:
	tox
