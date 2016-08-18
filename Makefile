.PHONY: build changelog clean editable pypi test

build:
	python setup.py sdist bdist_wheel

changelog:
	gitchangelog > docs/changelog.rst

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	rm -rf .tox

editable:
	pip install --editable .

pypi:
	rm -rf dist/
	python setup.py sdist bdist_wheel
	twine upload dist/*

test:
	tox
