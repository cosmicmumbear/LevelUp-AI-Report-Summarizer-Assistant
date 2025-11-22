import pytest
from unittest.mock import patch, MagicMock

from src.data_interpreter import interpret


# ---------------------------
# Test 1 — basic function invocation
# ---------------------------

def test_interpret_basic_runs():
    output = interpret("Sample OCR text")
    assert isinstance(output, str), "The function should return a string."

# ---------------------------
# Test 2 — output for empty imput
# ---------------------------

def test_interpret_empty_input():
    output = interpret("")
    assert isinstance(output, str)


# ---------------------------
# Test 3 — checking if all required sections appear in output
# ---------------------------

def test_interpret_output_structure():
    sample_ocr = "Q1 100, Q2 200"
    
    output = interpret(sample_ocr)

    required_sections = [
        "Name of chart:",
        "Source of chart:",
        "Type of chart:",
        "Variables",
        "Units:",
        "Topic of chart",
        "Trends",
        "Highest and lowest values",
        "Confidence"
    ]

    for section in required_sections:
        assert section in output, f"Missing section: {section}"


# ---------------------------
# Test 4 — Mocking Azure OpenAI
# ---------------------------

@patch("src.data_interpreter.AzureOpenAI")
def test_interpret_mock_api(mock_client):
    """
    This test checks whether the interpret() function correctly reads
    the mocked response from Azure OpenAI and returns it.
    """

    # create a mock AzureOpenAI instance
    mock_instance = MagicMock()
    mock_instance.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="MOCK_RESPONSE"))]
    )
    mock_client.return_value = mock_instance

    output = interpret("Fake OCR input")
    
    assert output == "MOCK_RESPONSE", "The function should return the response from the API."


# ---------------------------
# Test 5 — checking if garbage breaks the function
# ---------------------------

def test_interpret_handles_garbage_input():
    output = interpret("#### ??? 1234")
    assert isinstance(output, str)


# ---------------------------
# Test 6 — checking if model tries to guess missing info
# ---------------------------

def test_unknown_when_missing_info():
    output = interpret("no title no numbers nothing")
    assert "unknown" in output.lower()
