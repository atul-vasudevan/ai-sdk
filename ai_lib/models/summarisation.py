from __future__ import annotations

import os
from typing import Protocol

try:
    from transformers import pipeline
except Exception:
    pipeline = None  # type: ignore
  
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

        # limited to a max length.
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

class HFTextSummariser:
    """
    Summariser backed by a Hugging Face Transformers model.

    Loads a summarisation pipeline once and reuses it.
    Requires 'transformers' to be installed.
    """

    def __init__(self, model_name: str = "sshleifer/distilbart-cnn-12-6"):
        if pipeline is None:
            raise RuntimeError(
                "transformers is not installed; install with `pip install ai-lib[hf]`"
            )

        self._pipe = pipeline("summarization", model=model_name)

    def summarise(self, text: str) -> str:
        if not text.strip():
            return "No content provided to summarise."

        # Get actual token count
        # The pipeline's tokenizer is accessible via the model's tokenizer
        tokenizer = self._pipe.tokenizer
        input_tokens = len(tokenizer.encode(text, add_special_tokens=True))
        
        # max length is capped at 200 for longer texts
        # min_length to be at most half of max_length, but cap at 30
        max_length = min(200, max(input_tokens - 5, 10))
        min_length = min(30, max(max_length // 2, 5))

        result = self._pipe(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
        )
        return result[0]["summary_text"]


def get_text_summariser() -> TextSummariser:
    backend = os.getenv("AI_LIB_SUMMARISATION_BACKEND", "simple").lower()

    if backend == "hf":
        return HFTextSummariser()
    return SimpleTextSummariser()
