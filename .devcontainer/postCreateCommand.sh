#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "========================================"
echo " God Variable Theory — Codespaces Ready"
echo "========================================"
echo ""

# Ensure make exists (usually does). If not, install it.
if ! command -v make >/dev/null 2>&1; then
  echo "Installing make..."
  sudo apt-get update -y
  sudo apt-get install -y make
fi

echo "Cloning ecosystem repos (if not already present)..."
make clone || true

echo ""
echo "----------------------------------------"
echo "Next step:"
echo "  make demo"
echo "----------------------------------------"
echo ""
echo "Coherence Eternal ⭐"
echo ""
