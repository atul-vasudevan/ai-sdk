from __future__ import annotations

from typing import Any, Dict, Optional

from .models.summarisation import get_text_summariser, TextSummariser


class AIClient:
    """
    High-level entry point for AI-related operations.

    Capability:

    - summarise_text(text): generic text summarisation

    Internally it uses a pluggable summariser implementation
    """

    def __init__(self, app_name: str | None = None):
        self.app_name = app_name or "unknown_app"
        self._summariser: TextSummariser = get_text_summariser()

    def health(self) -> Dict[str, Any]:
        """Simple health check useful in tests and examples."""
        return {"status": "ok", "app_name": self.app_name}

    def summarise_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Summarise the given text into a shorter, human-readable form.

        :param text: Input text to be summarised.
        :param metadata: Optional metadata dictionary;
        :return: A summary string.
        """
        return self._summariser.summarise(text)