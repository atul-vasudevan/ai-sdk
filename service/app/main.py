from __future__ import annotations

import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from ai_lib import AIClient
from service.app.guardrails import GuardrailsConfig, validate_input, validate_output
from service.app.security import require_api_key

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

app = FastAPI(
    title="AI Summarisation Service",
    version="0.1.0",
    description="Example microservice using ai_lib.AIClient to summarise text.",
)

client = AIClient(app_name="service")


class SummariseRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=12_000)

class SummariseResponse(BaseModel):
    summary: str
    request_id: str

def get_request_id(x_request_id: str | None = Header(default=None, alias="X-Request-Id")) -> str:
    return x_request_id or str(uuid.uuid4())

@app.get("/health")
def health():
    """Simple health endpoint."""
    return client.health()


@app.post("/summarise", response_model=SummariseResponse, dependencies=[Depends(require_api_key)])
def summarise(req: SummariseRequest, request_id: str = Depends(get_request_id)):
    cfg = GuardrailsConfig(
        max_input_chars=int(os.getenv("AI_GUARDRAILS_MAX_INPUT_CHARS", "2000"))
    )

    try:
        validate_input(req.text, cfg)

        summary = client.summarise_text(req.text, metadata={"request_id": request_id})

        validate_output(req.text, summary)

        return SummariseResponse(summary=summary, request_id=request_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
