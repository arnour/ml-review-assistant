
.DEFAULT_GOAL := build
.PHONY: build package test lint clean
PROJ_SLUG = ml_review_assistant
PY_VERSION = 3.8
LINTER = flake8

build:
	pip install --editable .

package: clean docs
	python setup.py sdist

test:
	pytest --cov=$(PROJ_SLUG) --cov-report=html tests/

lint:
	$(LINTER) $(PROJ_SLUG)

clean :
	rm -rf dist \
	rm -rf docs/build \
	rm -rf htmlcov \
	rm -rf *.egg-info
	rm -fr **/__pycache__ \
	coverage erase
