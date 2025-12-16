from __future__ import annotations

from typing import Any

from ai_lib.tracing import traced_operation

from .models.summarisation import TextSummariser, get_text_summariser


class AIClient:
    """
    High-level entry point for AI-related operations.

    Capability:

    - summarise_text(text): generic text summarisation

    Internally it uses a pluggable summariser implementation and wraps operations in a
    traced operation context so that when Langfuse is installed, operations are traced.
    """

    def __init__(self, app_name: str | None = None):
        self.app_name = app_name or "unknown_app"
        self._summariser: TextSummariser = get_text_summariser()

    def health(self) -> dict[str, Any]:
        """Simple health check useful in tests and examples."""
        return {"status": "ok", "app_name": self.app_name}

    def summarise_text(
        self,
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """
        Summarise the given text into a shorter, human-readable form.

        :param text: Input text to be summarised.
        :param metadata: Optional metadata dictionary;
        :return: A summary string.
        """
        combined_metadata: dict[str, Any] = {"app_name": self.app_name}
        if metadata:
            combined_metadata.update(metadata)

        # Avoid logging excessively large inputs into traces.
        trace_inputs = {"text": (text[:5000] if text is not None else "")}

        with traced_operation(
            name="summarise_text",
            inputs=trace_inputs,
            metadata=combined_metadata,
        ):
            summary = self._summariser.summarise(text)

        return summary
