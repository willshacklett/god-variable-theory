# God Variable Theory — Hub Makefile
# Goal: make the ecosystem feel "one-click" by providing a single command entrypoint.

SHELL := /bin/bash

.PHONY: help demo status clone update clean

help:
	@echo ""
	@echo "God Variable Theory — Hub Commands"
	@echo "--------------------------------"
	@echo "make demo     # one-command walkthrough (prints links + optional local pulls)"
	@echo "make clone    # clones ecosystem repos into ./ecosystem/"
	@echo "make update   # git pull on each cloned repo"
	@echo "make status   # shows git status for each cloned repo"
	@echo "make clean    # removes ./ecosystem/"
	@echo ""

demo:
	@echo ""
	@echo "=============================="
	@echo " God Variable — One-Command Demo"
	@echo "=============================="
	@echo ""
	@echo "1) Drift Demo (fastest proof):"
	@echo "   https://github.com/willshacklett/gv-drift-demo"
	@echo ""
	@echo "2) GodScore CI (Action + dashboard):"
	@echo "   https://github.com/willshacklett/godscore-ci"
	@echo ""
	@echo "3) Runtime monitoring (GvAI Safety Systems):"
	@echo "   https://github.com/willshacklett/gvai-safety-systems"
	@echo ""
	@echo "Optional local setup:"
	@echo "  - Run: make clone"
	@echo "  - Then: make status"
	@echo ""
	@echo "Coherence Eternal ⭐"
	@echo ""

clone:
	@mkdir -p ecosystem
	@if [ -d "ecosystem/gv-drift-demo/.git" ]; then echo "✓ gv-drift-demo already cloned"; else git clone https://github.com/willshacklett/gv-drift-demo ecosystem/gv-drift-demo; fi
	@if [ -d "ecosystem/godscore-ci/.git" ]; then echo "✓ godscore-ci already cloned"; else git clone https://github.com/willshacklett/godscore-ci ecosystem/godscore-ci; fi
	@if [ -d "ecosystem/gvai-safety-systems/.git" ]; then echo "✓ gvai-safety-systems already cloned"; else git clone https://github.com/willshacklett/gvai-safety-systems ecosystem/gvai-safety-systems; fi
	@if [ -d "ecosystem/gv-engine/.git" ]; then echo "✓ gv-engine already cloned"; else git clone https://github.com/willshacklett/gv-engine ecosystem/gv-engine; fi
	@if [ -d "ecosystem/gv-watchdog/.git" ]; then echo "✓ gv-watchdog already cloned"; else git clone https://github.com/willshacklett/gv-watchdog ecosystem/gv-watchdog; fi
	@if [ -d "ecosystem/cft-cancer-sim/.git" ]; then echo "✓ cft-cancer-sim already cloned"; else git clone https://github.com/willshacklett/cft-cancer-sim ecosystem/cft-cancer-sim; fi
	@echo ""
	@echo "✓ Ecosystem cloned into ./ecosystem/"
	@echo "Next: make status"
	@echo ""

update:
	@if [ ! -d "ecosystem" ]; then echo "No ./ecosystem folder. Run: make clone"; exit 1; fi
	@for d in ecosystem/*; do \
		if [ -d "$$d/.git" ]; then \
			echo "---- $$d"; \
			( cd "$$d" && git pull --ff-only ) || true; \
		fi \
	done
	@echo ""
	@echo "✓ Update complete"
	@echo ""

status:
	@if [ ! -d "ecosystem" ]; then echo "No ./ecosystem folder. Run: make clone"; exit 1; fi
	@for d in ecosystem
