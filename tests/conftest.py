import os
import sys

# Ensure repo root is on sys.path so `import src...` works reliably in Codespaces/CI.
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
