from ai_lib import AIClient
from ai_lib.models.summarisation import SimpleTextSummariser


def test_ai_client_health_returns_expected_structure():
    client = AIClient(app_name="test-app")
    health = client.health()

    assert isinstance(health, dict)
    assert health["status"] == "ok"
    assert health["app_name"] == "test-app"


def test_ai_client_summarise_text_returns_non_empty_summary():
    client = AIClient()
    text = (
        "This is an example paragraph that we would like to summarise. "
        "It demonstrates how the AIClient delegates to an internal summariser."
    )

    summary = client.summarise_text(text)

    assert isinstance(summary, str)
    assert len(summary) > 0
    assert len(summary) <= len(text)


def test_ai_client_uses_underlying_summariser(monkeypatch):
    """
    Ensure AIClient.summarise_text delegates to the summariser implementation.

    We monkeypatch the summariser to a fake that returns a known value.
    """

    class FakeSummariser(SimpleTextSummariser):
        def summarise(self, text: str) -> str:
            return "FAKE SUMMARY"

    client = AIClient()

    client._summariser = FakeSummariser()  # type: ignore[attr-defined]

    summary = client.summarise_text("some input text")

    assert summary == "FAKE SUMMARY"
