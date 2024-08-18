SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON = python3.10
PROJECT = beistats_core
isort = isort $(PROJECT) tests
black = black -S -l 79 --target-version py310 $(PROJECT) tests
flake = flake8 $(PROJECT) tests
mypy =  mypy $(PROJECT) tests

.PHONY: all
all: test

venv:
	$(PYTHON) -m venv --prompt $(PROJECT) venv
	pip install -qU pip

.PHONY: install
install:
	pip install -qU -r requirements.txt

.PHONY: install-test
install-test: install
	pip install -qU -r requirements-test.txt

.PHONY: test
test: clean install-test lint
	pytest --cov-report term-missing --cov=$(PROJECT) tests/ -p no:warnings

.PHONY: pytest
pytest:
	pytest --cov-report term-missing --cov=$(PROJECT) tests/ -p no:warnings

.PHONY: format
format:
	$(isort)
	$(black)

.PHONY: lint
lint:
	$(flake)
	$(isort) --check-only
	$(black) --check
	$(mypy)

.PHONY: docker-run
docker-run:
	docker build -t $(PROJECT) .
	docker run -dp 127.0.0.1:80:80 $(PROJECT)


.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -f .coverage*
	rm -rf build
	rm -rf dist
