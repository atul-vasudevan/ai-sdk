# AI Library (`ai_lib`)

A Python SDK for AI capabilities with built-in observability and extensible backend support.

## 📦 Installation

### Basic Installation

```bash
pip install -e .
```

### With HuggingFace Backend

To use the HuggingFace summarization backend, install with the `hf` extra:

```bash
pip install -e ".[hf]"
```

### Development Installation

For development with testing and linting tools:

```bash
pip install -e ".[dev]"
```

## 🚀 Quick Start

### Basic Usage

```python
from ai_lib import AIClient

# Initialize the client
client = AIClient(app_name="my-app")

# Summarize text
text = "Your long text here..."
summary = client.summarise_text(text)
print(summary)
```

### Complete Example

```python
from ai_lib import AIClient

def main():
    client = AIClient(app_name="example-app")
    
    text = (
        "Artificial intelligence is rapidly becoming a core component of modern software systems. "
        "By automating repetitive tasks, analyzing large volumes of data, and assisting with "
        "decision-making, AI enables teams to work more efficiently."
    )
    
    summary = client.summarise_text(text)
    print(f"Original: {text}")
    print(f"Summary: {summary}")

if __name__ == "__main__":
    main()
```

## ⚙️ Configuration

### Backend Selection

The library supports multiple summarization backends, controlled via the `AI_LIB_SUMMARISATION_BACKEND` environment variable:

#### Simple Backend (Default)

```bash
export AI_LIB_SUMMARISATION_BACKEND=simple
```

- **No dependencies required** (works out of the box)
- Fast and lightweight
- Truncates text to a fixed length
- Suitable for development and testing

#### HuggingFace Backend

```bash
export AI_LIB_SUMMARISATION_BACKEND=hf
```

- **Requires:** `pip install -e ".[hf]"`
- Uses `sshleifer/distilbart-cnn-12-6` model
- Produces more intelligent summaries
- Requires more memory and compute
- Model downloads automatically on first use

### Observability (Langfuse)

The library automatically traces operations when Langfuse is configured. Set these environment variables:

```bash
export LANGFUSE_SECRET_KEY="sk-lf-xxxxx"
export LANGFUSE_PUBLIC_KEY="pk-lf-xxxxx"
export LANGFUSE_HOST="https://cloud.langfuse.com"
```

**Note:** If Langfuse keys are not set, the library will work normally but without tracing.

## 📚 API Reference

### `AIClient`

Main entry point for AI operations.

#### `__init__(app_name: str | None = None)`

Initialize the AI client.

- **Parameters:**
  - `app_name` (str, optional): Name of your application for observability. Defaults to `"unknown_app"`.

#### `health() -> dict[str, Any]`

Simple health check method.

- **Returns:** Dictionary with `status` and `app_name` keys.

#### `summarise_text(text: str, metadata: dict[str, Any] | None = None) -> str`

Summarize the given text.

- **Parameters:**
  - `text` (str): Input text to be summarized.
  - `metadata` (dict, optional): Additional metadata to attach to the trace.
- **Returns:** Summary string.

**Example:**

```python
client = AIClient(app_name="my-app")

# Basic usage
summary = client.summarise_text("Long text here...")

# With metadata
summary = client.summarise_text(
    "Long text here...",
    metadata={"user_id": "123", "source": "api"}
)
```

## 🔍 Observability

All operations are automatically traced when Langfuse is configured. Traces include:

- Operation name (`summarise_text`)
- Input text (truncated to 5000 characters)
- Metadata (app name and custom metadata)
- Execution time
- Results

View traces in your Langfuse dashboard at https://cloud.langfuse.com

## 🧪 Testing

### Run Unit Tests

```bash
pytest ai_lib/tests
```

### Run with Coverage

```bash
pytest ai_lib/tests --cov=ai_lib --cov-report=html
```

## 🏗️ Architecture

### Backend System

The library uses a pluggable backend system:

1. **Backend Selection:** Controlled via `AI_LIB_SUMMARISATION_BACKEND` env var
2. **Factory Pattern:** `get_text_summariser()` returns the appropriate backend
3. **Interface:** All backends implement `TextSummariser` protocol

### Tracing Integration

- Operations are wrapped in `traced_operation()` context manager
- Automatically handles Langfuse initialization
- Gracefully degrades if Langfuse is not configured

## 🔧 Development

### Project Structure

```
ai_lib/
├── __init__.py          # Public API exports
├── client.py            # AIClient implementation
├── models/
│   └── summarisation.py # Backend implementations
├── tracing.py           # Langfuse integration
├── version.py           # Version information
└── tests/               # Unit tests
```

### Adding New Backends

1. Create a class implementing `TextSummariser` protocol
2. Add it to `get_text_summariser()` factory function
3. Update this README with backend configuration

### Code Quality

The project uses Ruff for linting and formatting:

```bash
# Check code
ruff check .

# Format code
ruff format .

# Auto-fix issues
ruff check --fix .
```
