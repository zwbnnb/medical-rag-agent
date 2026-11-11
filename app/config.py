from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # OpenAI-compatible API (DashScope / 硅基流动 / OpenAI / 本地 vLLM 均可)
    openai_api_key: str = ""
    openai_api_base: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    llm_model: str = "qwen-plus"
    embed_model: str = "text-embedding-v3"

    # true = 无 Key 也能跑检索+工具+规则回答（便于自测）
    mock_llm: bool = True

    knowledge_dir: Path = ROOT / "data" / "knowledge"
    chroma_dir: Path = ROOT / "chroma_db"
    collection_name: str = "medical_rag"
    top_k: int = 4
    host: str = "127.0.0.1"
    port: int = 8000


settings = Settings()
