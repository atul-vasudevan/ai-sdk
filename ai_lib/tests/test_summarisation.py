from ai_lib.models.summarisation import SimpleTextSummariser, get_text_summariser


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


def test_get_text_summariser_returns_simple_by_default():
    summariser = get_text_summariser()
    assert isinstance(summariser, SimpleTextSummariser)
