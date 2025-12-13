from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Dict, Optional

try:
    from langfuse import Langfuse
except ImportError:
    Langfuse = None


_langfuse_client: Optional["Langfuse"] = None  # type: ignore[name-defined]


def get_langfuse() -> Optional["Langfuse"]:  # type: ignore[name-defined]
    """
    Lazily initialise and cache a Langfuse client.

    If the library is not installed or required environment variables are
    missing, this returns None so the rest of the SDK can continue as normal.
    """
    global _langfuse_client

    if _langfuse_client is not None:
        return _langfuse_client

    if Langfuse is None:
        return None

    secret = os.getenv("LANGFUSE_SECRET_KEY")
    public = os.getenv("LANGFUSE_PUBLIC_KEY")
    host = os.getenv("LANGFUSE_HOST")  # optional

    if not secret or not public:
        # Not configured – operate in no-op mode.
        return None

    _langfuse_client = Langfuse(
        secret_key=secret,
        public_key=public,
        host=host,
    )
    return _langfuse_client


@contextmanager
def traced_operation(
    name: str,
    inputs: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
):
    """
    Context manager that wraps an operation in a Langfuse trace.

    Usage:
        with traced_operation("summarise_text", inputs={"text": "..."}, metadata={"app": "x"}):
            ... do work ...

    Behaviour:
    - If Langfuse is not installed or not configured with env vars,
      this acts as a no-op.
    - On success, records a simple success output.
    - On exception, records error information and re-raises.
    """
    lf = get_langfuse()

    if lf is None:
        # No tracing available – still yield so caller code runs normally.
        yield None
        return

    # Use start_as_current_span() which is a context manager in the new API
    with lf.start_as_current_span(
        name=name,
        input=inputs or {},
        metadata=metadata or {},
    ) as span:
        try:
            yield span
            span.update(
                output={"status": "success"},
            )
        except Exception as exc:  # noqa: BLE001 - we want to capture any error
            span.update(
                output={
                    "status": "error",
                    "error": str(exc),
                },
                level="ERROR",
            )
            raise
        finally:
            lf.flush()