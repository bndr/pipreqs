.PHONY: clean-pyc clean-build docs clean

SHELL := /bin/bash
export PATH := $(PATH):$(HOME)/.local/bin/
ipynb_dir := dirname
ipynb_files := $(shell find $(ipynb_dir) -type f -name *.ipynb ! -name *checkpoint*)
temp_dir := .tempy

requirements:
	@which pipreqs || pip3 install --user pipreqs
	@which jupyter || pip3 install --user jupyter
	@[ -d $(temp_dir) ] || mkdir $(temp_dir)
	@num=210696 ; for each in $(ipynb_files) ; do \
		b=felipe$$num ; \
		jupyter nbconvert --output=$$b --output-dir=$(temp_dir) --to=python $$each ; \
		((num = num + 1)) ; \
	done
	@pipreqs --force --savepath requirements.txt $(temp_dir)
	@rm -rf $(temp_dir)

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 pipreqs tests

test:
	pip install -r requirements.txt
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source pipreqs setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/pipreqs.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ pipreqs
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist bdist_wheel upload -r pypi

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install
