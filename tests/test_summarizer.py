import os
import logging
import pytest

openai = pytest.importorskip("openai")

from src.summarizer import Summarizer


def test_summarizer_ooda_structure(caplog):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("Set OPENAI_API_KEY to run this test")

    caplog.set_level(logging.INFO)

    input_data = {
        "text": "Temperature sensor A1 reads 100\u00b0C, which exceeds normal range.",
        "context": "Monitoring system alert",
    }
    summ = Summarizer(api_key=api_key)
    summary = summ.summarize(input_data)

    assert isinstance(summary, dict)
    expected_keys = {"Observe", "Orient", "Decide", "Act"}
    assert set(summary.keys()) == expected_keys
    for key, value in summary.items():
        assert isinstance(value, str)
        assert value.strip() != ""
    assert "Input JSON" in caplog.text or "Summary:" in caplog.text


def test_summarizer_error_handling(caplog):
    caplog.set_level(logging.ERROR)
    bad_summ = Summarizer(api_key="INVALID_KEY")
    with pytest.raises(Exception):
        bad_summ.summarize({"dummy": "data"})
    assert "OpenAI API error" in caplog.text or "OpenAI library not available" in caplog.text

