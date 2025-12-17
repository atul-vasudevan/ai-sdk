from __future__ import annotations


def list_capabilities() -> dict:
    return {
        "summarisation": {
            "method": "AIClient.summarise_text(text: str) -> str",
            "env_var": "AI_LIB_SUMMARISATION_BACKEND",
            "available_models": {
                "simple": {
                    "model": None,
                    "notes": "Deterministic baseline for CI"},
                "hf": {
                    "model": "sshleifer/distilbart-cnn-12-6",
                    "notes": "Hugging Face summariser"},
            },
        }
    }
