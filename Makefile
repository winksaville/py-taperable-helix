.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

format_srcs=setup.py taperable_helix/ tests/ examples/ docs/

.PHONY:
help: ## help
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)


.PHONY: clean
clean: clean-no-docs clean-docs ## remove all build, test, coverage and Python artifacts

.PHONY: clean-no-docs
clean-no-docs: clean-build clean-pyc clean-test ## remove all EXCEPT docs

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	find . -name '.mypy_cache' -exec rm -fr {} +

.PHONY: clean-docs
clean-docs: ## remove doc artifacts
	$(MAKE) -C docs clean

.PHONY: t
t: test ## same as `test`

.PHONY: test-generate
test-generate: ## run tests creating data
	pytest --generate

.PHONY: test-view
test-view: ## run tests generating the view pages
	pytest --view

.PHONY: test
test: ## run tests quickly with the default Python
	pytest

.PHONY: test-all
test-all: ## run tests on every Python version with tox
	tox

.PHONY: f, format
f: format ## format
format: ## format, lint py files with isort, black and flake8
	isort ${format_srcs}
	black ${format_srcs}
	flake8 ${format_srcs}

.PHONY: mypy
mypy: ## Run mypy over ${format_srcs}
	mypy ${format_srcs}

.PHONY: coverage
coverage: ## check code coverage quickly with the default Python
	coverage run --source taperable_helix -m pytest
	coverage report -m
	# coverage html
	# $(BROWSER) htmlcov/index.html

# Currently this isn't used
.PHONY: apidocs
apidocs:
	rm -f docs/taperable_helix.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ taperable_helix

.PHONY: docs
docs: clean-docs ## generate Sphinx HTML documentation, including API docs
	$(MAKE) -C docs html

.PHONY: showdocs
showdocs: ## Use the browser to show the docs
	$(BROWSER) docs/_build/html/index.html

.PHONY: servedocs
servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

.PHONY: release
release: dist ## package and upload a release
	twine upload dist/*

.PHONY: release-testpypi
release-testpypi: dist ## package and upload a release
	twine upload --repository testpypi dist/*

.PHONY: push-with-tags
push-tags: ## Push origin master with tags with zipped srcs on github
	git push origin master --tags

.PHONY: bumpver-patch
bumpver-patch: ## Bump patch field of current_version
	bump2version patch

.PHONY: bumpver-minor
.PHONY:
bumpver-minor: ## Bump minor field of current_version
	bump2version minor

.PHONY: bumpver-major
bumpver-major: ## Bump major field of current_version
	bump2version major

.PHONY: dist
dist: clean docs ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

.PHONY: install
install: clean ## Install from pypi.org
	pip install taperable-helix

.PHONY: install-test
install-test: clean ## Install from test.pypi.org
	pip install taperable-helix

.PHONY: install-dev
install-dev: ## Install from the sources for developemeent
	#pip install -e .
	pip install -e . -r dev-requirements.txt


# Update dependencies, used by update
# Note: You can not use --generate-hashes parameter with editable installs
.PHONY: update-deps
update-deps:
	# No requirements in setup.py so skip
	# pip-compile --upgrade --allow-unsafe --output-file requirments.txt
	# pip install --upgrade -r requirements.txt
	pip-compile --upgrade --allow-unsafe --output-file dev-requirements.txt dev-requirements.in
	pip install --upgrade -r dev-requirements.txt

# Besure pip-tools is installed, used by update
.PHONY: update-init
update-init:
	pip install pip-tools

# Invoke update when you want to update the dev-requirments.
# See: https://stackoverflow.com/a/33685899
#
.PHONY: update-dev
update-dev: clean-no-docs update-init update-deps install-dev ## Update dev-requirements
