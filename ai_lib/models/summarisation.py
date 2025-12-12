from __future__ import annotations
from typing import Protocol


class TextSummariser(Protocol):
    """Interface for text summarisation backends."""

    def summarise(self, text: str) -> str: ...


class SimpleTextSummariser:
    """
    A small, deterministic summarisation backend.

    This implementation:
    - always returns a non-empty summary,
    - is dependency-free,
    - is deterministic for tests and CI,
    """

    def summarise(self, text: str) -> str:
        text = (text or "").strip()

        if not text:
            return "No content provided to summarise."

        # Basic approach: take first 1–2 sentences, limited to a max length.
        max_len = 320

        # Split on basic sentence boundaries.
        for sep in [". ", "\n"]:
            if sep in text:
                parts = text.split(sep)
                candidate = sep.join(parts[:2]).strip()
                if candidate:
                    text = candidate
                break

        if len(text) > max_len:
            return text[: max_len - 3].rstrip() + "..."

        return text


def get_text_summariser() -> TextSummariser:
    """
    Factory for the default summariser.
    """
    return SimpleTextSummariser()
