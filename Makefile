# vim: set noet
VENV=venv
PYTHON=python3
VENV=venv
PIP=$(VENV)/bin/pip

help:
	@echo "Targets:"
	@echo "venv: Create virtualenv for development"
	@echo "test: Run unit tests"
	@echo "build: Build docker image"
	@echo "deploy: Deploy to production"

$(PIP):
	$(PYTHON) -m venv $(VENV)

venv: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(PIP) install -Ur requirements.txt

test:
	$(PYTHON) -m unittest discover -v --start-directory=tests/ --pattern=*_test.py
