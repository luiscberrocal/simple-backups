sources = simple_backups

.PHONY: test format lint unittest coverage pre-commit clean
test: format lint unittest

format:
	isort $(sources) tests
	black $(sources) tests

lint:
	flake8 $(sources) tests

unittest:
	pytest

cov:
	pytest --cov=$(sources) --cov-branch --cov-report=term-missing --cov-fail-under=100 tests

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf .mypy_cache .pytest_cache
	rm -rf *.egg-info
	rm -rf .tox dist site
	rm -rf coverage.xml .coverage
	rm -rf ./output/*
	rm -rf ./dist

dist: clean
	poetry build

release: dist ## package and upload a release
	twine upload dist/*
