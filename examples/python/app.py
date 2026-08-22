"""Synthetic FastAPI health endpoint for the ai-sdlc worked example."""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="ai-sdlc-example", version="0.1.0")


class HealthResponse(BaseModel):
    status: str
    version: str


@app.get("/api/v1/healthz", response_model=HealthResponse)
def healthz() -> JSONResponse:
    """Read-only health probe; returns fixed JSON, no side effects."""
    payload = HealthResponse(status="ok", version="0.1.0")
    return JSONResponse(content=payload.model_dump())