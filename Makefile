.PHONY: init build changelog clean editable pypi test

init:
	pipenv install --python 3.6.3 --dev

build:
	python setup.py sdist bdist_wheel

changelog:
	gitchangelog > docs/changelog.rst

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
	rm -rf .tox

editable:
	pip install --editable .

pypi:
	rm -rf dist/
	python setup.py sdist bdist_wheel
	twine upload dist/*

test:
	pipenv run tox
