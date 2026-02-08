"""
Bulk tests: run tool on all test XMLs, validate outputs, and compare to expected files.
"""

import sys
from pathlib import Path

import pytest

# conftest adds src to path
from main import IFSLanguageAutomation
from validator import IFSValidator

from .conftest import REPO_ROOT, TEST_DIR, TEST_OUT_DIR


def _normalize_content(content: str) -> str:
    """Normalize line endings and trailing newlines for comparison."""
    return content.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"


def _read_normalized(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return _normalize_content(f.read())


@pytest.fixture(scope="module")
def test_out_dir():
    """Output directory for generated files; created once per test module run."""
    TEST_OUT_DIR.mkdir(parents=True, exist_ok=True)
    yield TEST_OUT_DIR
    # Optional: leave files for inspection; .gitignore excludes test/out/


def discover_xml_fixtures():
    """Paths to all translationDb_*.xml in test/."""
    if not TEST_DIR.exists():
        return []
    return sorted(TEST_DIR.glob("translationDb_*.xml"))


@pytest.mark.parametrize("xml_path", discover_xml_fixtures(), ids=lambda p: p.name)
def test_bulk_run_and_validate(xml_path, test_out_dir):
    """Run automation on each test XML and validate all generated .lng and .trs files."""
    automation = IFSLanguageAutomation(
        xml_path=str(xml_path),
        output_dir=str(test_out_dir),
        languages=["sv-SE", "nb-NO"],
        translation_backend="dictionary",
    )
    automation.run()

    # Validate every generated .lng and .trs in output dir
    validator = IFSValidator()
    for ext in (".lng", ".trs"):
        for path in test_out_dir.glob(f"*{ext}"):
            is_valid, errors, _ = validator.validate_file(str(path))
            assert is_valid, f"{path.name}: {errors}"


# Expected output files for ActivityEstimate (PROJ/Cust) – only case with fixtures
ACTIVITY_ESTIMATE_EXPECTED = [
    "Proj_LU_LogicalUnit-Cust.lng",
    "Proj_LU_LogicalUnit-Cust-sv.trs",
    "Proj_LU_LogicalUnit-Cust-no.trs",
]


def test_activity_estimate_output_matches_expected(test_out_dir):
    """
    Run tool explicitly on ActivityEstimate XML and compare to reference fixtures.
    This test is self-contained (does not rely on parametrized run order).
    """
    xml_path = TEST_DIR / "translationDb_ActivityEstimate-Cust.xml"
    if not xml_path.exists():
        pytest.skip("translationDb_ActivityEstimate-Cust.xml not found")

    automation = IFSLanguageAutomation(
        xml_path=str(xml_path),
        output_dir=str(test_out_dir),
        languages=["sv-SE", "nb-NO"],
        translation_backend="dictionary",
    )
    automation.run()

    for basename in ACTIVITY_ESTIMATE_EXPECTED:
        expected_path = TEST_DIR / basename
        generated_path = test_out_dir / basename
        if not expected_path.exists():
            pytest.skip(f"Expected fixture missing: {expected_path}")
        assert generated_path.exists(), f"Generated file missing: {generated_path}"

        expected_content = _read_normalized(expected_path)
        generated_content = _read_normalized(generated_path)
        assert generated_content == expected_content, (
            f"Content mismatch for {basename}"
        )
