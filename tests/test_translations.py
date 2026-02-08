"""
Tests for dictionary translation backend.
Verifies that built-in mappings match expected Swedish and Norwegian strings.
"""

import pytest

# conftest adds src to path
from translator import IFSTranslator


# Expected mappings from translator.py dictionary (used in reference .trs files)
EXPECTED_SWEDISH = {
    "C Actual Cost": "Verklig kostnad",
    "C Actual Revenue": "Verklig intäkt",
    "Actual Cost": "Verklig kostnad",
    "Actual Revenue": "Verklig intäkt",
}

EXPECTED_NORWEGIAN = {
    "C Actual Cost": "Faktisk kostnad",
    "C Actual Revenue": "Faktisk inntekt",
    "Actual Cost": "Faktisk kostnad",
    "Actual Revenue": "Faktisk inntekt",
}


@pytest.fixture
def translator():
    return IFSTranslator(backend="dictionary")


def test_dictionary_translations_swedish(translator):
    """Dictionary returns correct Swedish translations for known labels."""
    labels = list(EXPECTED_SWEDISH.keys())
    result = translator.translate_batch(labels, "sv-SE")
    for eng, expected in EXPECTED_SWEDISH.items():
        assert result.get(eng) == expected, f"sv-SE: {eng!r} -> {result.get(eng)!r}"


def test_dictionary_translations_norwegian(translator):
    """Dictionary returns correct Norwegian translations for known labels."""
    labels = list(EXPECTED_NORWEGIAN.keys())
    result = translator.translate_batch(labels, "nb-NO")
    for eng, expected in EXPECTED_NORWEGIAN.items():
        assert result.get(eng) == expected, f"nb-NO: {eng!r} -> {result.get(eng)!r}"


def test_dictionary_unknown_label_returns_original(translator):
    """Labels not in dictionary are returned unchanged (fallback)."""
    result = translator.translate_batch(["Unknown Label XYZ"], "sv-SE")
    assert result["Unknown Label XYZ"] == "Unknown Label XYZ"
    result_nb = translator.translate_batch(["Unknown Label XYZ"], "nb-NO")
    assert result_nb["Unknown Label XYZ"] == "Unknown Label XYZ"


def test_dictionary_batch_includes_all_inputs(translator):
    """translate_batch returns one entry per input."""
    labels = ["C Actual Cost", "C Actual Revenue", "Some Other Label"]
    result = translator.translate_batch(labels, "sv-SE")
    assert len(result) == len(labels)
    assert set(result.keys()) == set(labels)
