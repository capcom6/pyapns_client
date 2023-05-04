# Makefile for Python library project

# Variables
PYTHON = python
PIP = $(PYTHON) -m pip
PACKAGE_NAME = pyapns_client

# Default target
.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  install        Install package and dependencies"
	@echo "  test           Run tests"
	@echo "  lint           Lint code"
	@echo "  clean          Clean up project"
	@echo "  dist           Build distribution package"
	@echo "  upload         Upload distribution package to PyPI"
	@echo "  help           Show this help message"

# Install package and dependencies
.PHONY: install
install:
	$(PIP) install -U pip
	$(PIP) install -e .[dev]

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest tests/

# Lint code
.PHONY: lint
lint:
	$(PYTHON) -m flake8 $(PACKAGE_NAME)
	$(PYTHON) -m black --check $(PACKAGE_NAME)
	$(PYTHON) -m isort --check $(PACKAGE_NAME)

# Clean up project
.PHONY: clean
clean:
	$(PYTHON) setup.py clean --all
	rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/

# Build distribution package
.PHONY: dist
dist:
	$(PYTHON) setup.py sdist bdist_wheel

# Upload distribution package to PyPI
.PHONY: upload
upload:
	$(PYTHON) -m twine upload dist/*

# .DEFAULT_GOAL is the target that make will run if no target is specified
.DEFAULT_GOAL := help