
.DEFAULT_GOAL := build
.PHONY: build package test coverage lint clean
PROJ_SLUG = ml_review_assistant
PY_VERSION = 3.8
LINTER = flake8
FIXER = autopep8

build:
	pip install --editable .

package: clean docs
	python setup.py sdist

test:
	coverage run -m unittest

coverage:
	coverage report --include="ml_review_assistant/**"

lint:
	$(LINTER) $(PROJ_SLUG)

lintfix:
	$(FIXER) --in-place --aggressive --aggressive $(PROJ_SLUG)/**/**

clean :
	rm -rf dist \
	rm -rf docs/build \
	rm -rf htmlcov \
	rm -rf *.egg-info
	rm -fr **/__pycache__ \
	coverage erase
