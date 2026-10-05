#!/usr/bin/env bash
set -euo pipefail

echo "God Variable independent research workspace"
echo "No product repositories are cloned or modified automatically."
echo "Setup: python3 -m venv .venv"
echo "Then: source .venv/bin/activate"
echo "Install: python -m pip install -r requirements-research-lock.txt"
echo "Verify: make test && make reproduce-smoke"
