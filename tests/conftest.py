"""
Pytest configuration and shared fixtures for IFS Translator tests.
Adds src to sys.path so modules can be imported.
"""

import sys
from pathlib import Path

# Project root (parent of tests/)
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"

# Ensure src is importable when running tests from repo root
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


def pytest_configure(config):
    """Register path fixtures at collection time."""
    pass


# Shared paths
TEST_DIR = REPO_ROOT / "test"
TEST_OUT_DIR = TEST_DIR / "out"
