# Model Catalog

This SDK exposes AI capabilities via `AIClient`. Each capability may have multiple backends.

## Summarisation

**Method:** `AIClient.summarise_text(text: str) -> str`

### Backends
| Backend | How to enable | Model | Notes |
|--------|---------------|-------|------|
| simple | `AI_LIB_SUMMARISATION_BACKEND=simple` | N/A | Deterministic baseline for CI |
| hf | `AI_LIB_SUMMARISATION_BACKEND=hf` | `sshleifer/distilbart-cnn-12-6` | Hugging face model fro summarisation |
