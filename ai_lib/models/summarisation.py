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

        # Get token count to scale summary length
        tokenizer = self._pipe.tokenizer
        input_tokens = len(tokenizer.encode(text, add_special_tokens=True))

        # Length strategy tuned for short inputs (to avoid returning the original text)
        if input_tokens < 50:
            # Very short inputs: keep concise but allow paraphrase
            max_length = min(20, max(12, int(input_tokens * 0.8)))
            min_length = max(5, min(8, max_length // 2))
        else:
            # Longer inputs: proportional length with sensible caps
            max_length = min(200, max(40, int(input_tokens * 0.4)))
            min_length = max(10, min(60, max_length // 3))

        result = self._pipe(
            text,
            max_length=max_length,
            min_length=min_length,
            num_beams=4,
            no_repeat_ngram_size=3,
            length_penalty=0.8,
            do_sample=False,
        )
        return result[0]["summary_text"]


def get_text_summariser() -> TextSummariser:
    backend = os.getenv("AI_LIB_SUMMARISATION_BACKEND", "simple").lower()

    if backend == "hf":
        return HFTextSummariser()
    return SimpleTextSummariser()
