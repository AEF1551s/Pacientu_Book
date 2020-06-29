.ONESHELL:

PYTHON := python3
PIP := pip

.PHONY: venv install

venv:
	$(PYTHON) -m venv .venv

install: venv
	. .venv/bin/activate && $(PIP) install -r requirements.txt

run: install
	$(PYTHON) -m appointments
