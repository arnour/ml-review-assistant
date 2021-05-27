
.DEFAULT_GOAL := build
.PHONY: install build test coverage lint clean
PROJ_SLUG = ml_text_assistant
PY_VERSION = 3.8
LINTER = flake8
FIXER = autopep8

install:
	pipenv install --dev && pipenv shell

build:
	pip install --editable .

test:
	coverage run -m unittest

coverage:
	coverage report --include="ml_text_assistant/**" && coverage html --include="ml_text_assistant/**"

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
