from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from ai_lib import AIClient

app = FastAPI(
    title="AI Summarisation Service",
    version="0.1.0",
    description="Example microservice using ai_lib.AIClient to summarise text.",
)

# Create a single shared client instance
client = AIClient(app_name="service")


class SummariseRequest(BaseModel):
    text: str


class SummariseResponse(BaseModel):
    summary: str


@app.get("/health")
def health():
    """Simple health endpoint."""
    return client.health()


@app.post("/summarise", response_model=SummariseResponse)
def summarise(req: SummariseRequest):
    """
    HTTP endpoint that uses the shared AIClient to summarise text.
    """
    summary = client.summarise_text(req.text)
    return SummariseResponse(summary=summary)
