from dataclasses import dataclass

@dataclass(frozen=True)
class GuardrailsConfig:
    max_input_chars: int = 2_000

def validate_input(text: str, cfg: GuardrailsConfig) -> None:
    if not text or not text.strip():
        raise ValueError("No content provided to summarise.")
    if len(text) > cfg.max_input_chars:
        raise ValueError(f"Input too large. Max {cfg.max_input_chars} characters.")

def validate_output(input_text: str, summary: str) -> None:
    if not summary or not summary.strip():
        raise ValueError("Model returned an empty summary.")

    if len(input_text.strip()) > 200 and len(summary.strip()) >= len(input_text.strip()):
        raise ValueError("Summary was not shorter than the input (likely not summarised).")
