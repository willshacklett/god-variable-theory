SHELL := /bin/bash
PYTHON ?= python

.PHONY: help test reproduce-smoke reproduce-benchmarks reproduce-legacy

help:
	@echo "God Variable public research commands"
	@echo "make test                 Run software and evidence/document tests"
	@echo "make reproduce-smoke      Run synthetic protocol and CI-output checks"
	@echo "make reproduce-benchmarks Run all five frozen fluid benchmarks"
	@echo "make reproduce-legacy     Run the unverified historical cosmology toy"

test:
	$(PYTHON) -m pytest -q

reproduce-smoke:
	$(PYTHON) scripts/reproduce_research.py --smoke

reproduce-benchmarks:
	$(PYTHON) scripts/reproduce_research.py --benchmarks

reproduce-legacy:
	$(PYTHON) scripts/reproduce_research.py --legacy