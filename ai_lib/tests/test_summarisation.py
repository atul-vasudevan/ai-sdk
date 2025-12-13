import os
from ai_lib.models.summarisation import (
    SimpleTextSummariser,
    HFTextSummariser,
    get_text_summariser,
)

def test_simple_summariser_returns_non_empty_summary():
    summariser = SimpleTextSummariser()
    text = (
        "This is a long example of text intended to be summarised. "
        "It contains multiple sentences so we can test summarisation behaviour."
    )

    summary = summariser.summarise(text)

    assert isinstance(summary, str)
    assert len(summary) > 0
    assert len(summary) <= len(text)


def test_simple_summariser_handles_empty_input():
    summariser = SimpleTextSummariser()
    summary = summariser.summarise("")
    assert "No content" in summary


def test_get_text_summariser_returns_simple_by_default(monkeypatch):
    monkeypatch.setenv("AI_LIB_SUMMARISATION_BACKEND", "simple")
    summariser = get_text_summariser()
    assert isinstance(summariser, SimpleTextSummariser)


def test_factory_returns_hf_summariser_when_env_set(monkeypatch):
    monkeypatch.setenv("AI_LIB_SUMMARISATION_BACKEND", "hf")

    monkeypatch.setattr(
        "ai_lib.models.summarisation.pipeline",
        lambda *args, **kwargs: lambda t, **kw: [{"summary_text": "mock"}],
    )

    summariser = get_text_summariser()
    assert isinstance(summariser, HFTextSummariser)
