from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.agent import run_agent
from app.config import settings

app = FastAPI(
    title="Medical RAG Agent Demo",
    description="家用医疗监测科普 + 课题知识 RAG Agent（求职作品）",
    version="0.1.0",
)

static_dir = Path(__file__).resolve().parents[1] / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


@app.get("/")
def index():
    index_html = static_dir / "index.html"
    if index_html.exists():
        return FileResponse(index_html)
    return {"message": "OK", "docs": "/docs"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mock_llm": settings.mock_llm or not bool(settings.openai_api_key),
        "model": settings.llm_model,
    }


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        return run_agent(req.question.strip())
    except Exception as e:  # noqa: BLE001 — demo surface
        raise HTTPException(status_code=500, detail=str(e)) from e
