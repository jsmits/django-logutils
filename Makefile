.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove python file artifacts"
	@echo "clean - run clean-build and clean-pyc"
	@echo "lint - check style with flake8 and pylint"
	@echo "test - run tests quickly with the default python"
	@echo "test-all - run tests on every python version with tox"
	@echo "coverage - check code coverage quickly with the default python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - make a release with zest.releaser's fullrelease"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 django_logutils tests --exit-zero
	pylint --load-plugins pylint_django -f colorized --rcfile=.pylint.cfg --disable=I0011 -j 4 -r n django_logutils/ tests/

test:
	coverage run --source django_logutils -m py.test -v
	coverage report -m

test-all:
	tox

coverage: test
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/django-logutils.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ django_logutils
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release:
	fullrelease
