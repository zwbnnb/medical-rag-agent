from __future__ import annotations

import hashlib
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


class HashEmbeddings(Embeddings):
    """无 API Key 时的确定性伪向量，保证本地可建库、可检索（演示级）。"""

    def __init__(self, dim: int = 64):
        self.dim = dim

    def _embed_one(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        tokens = text.lower().replace("\n", " ").split()
        if not tokens:
            tokens = [text]
        for tok in tokens:
            h = hashlib.md5(tok.encode("utf-8")).hexdigest()
            idx = int(h[:8], 16) % self.dim
            sign = 1.0 if int(h[8:10], 16) % 2 == 0 else -1.0
            vec[idx] += sign
        # L2 normalize
        norm = sum(x * x for x in vec) ** 0.5 or 1.0
        return [x / norm for x in vec]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_one(text)


def get_embeddings() -> Embeddings:
    if settings.mock_llm or not settings.openai_api_key:
        return HashEmbeddings()
    from langchain_openai import OpenAIEmbeddings

    return OpenAIEmbeddings(
        model=settings.embed_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_api_base,
    )


def load_markdown_docs(knowledge_dir: Path | None = None) -> list[Document]:
    root = knowledge_dir or settings.knowledge_dir
    docs: list[Document] = []
    for path in sorted(root.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        docs.append(Document(page_content=text, metadata={"source": path.name}))
    if not docs:
        raise FileNotFoundError(f"知识库为空：{root}")
    return docs


def split_docs(docs: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    return splitter.split_documents(docs)


def build_vectorstore(persist: bool = True):
    from langchain_community.vectorstores import Chroma

    docs = split_docs(load_markdown_docs())
    embeddings = get_embeddings()
    settings.chroma_dir.mkdir(parents=True, exist_ok=True)
    vs = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=settings.collection_name,
        persist_directory=str(settings.chroma_dir) if persist else None,
    )
    return vs, len(docs)


def get_vectorstore():
    from langchain_community.vectorstores import Chroma

    embeddings = get_embeddings()
    return Chroma(
        collection_name=settings.collection_name,
        embedding_function=embeddings,
        persist_directory=str(settings.chroma_dir),
    )


def _keyword_score(query: str, text: str) -> float:
    q = query.lower()
    t = text.lower()
    keys = [
        "血压", "收缩压", "舒张压", "血糖", "空腹", "餐后", "mmol",
        "客服", "开药", "降压", "dpls", "residual", "gdsc", "药敏",
        "r²", "r2", "样本", "测量",
    ]
    score = 0.0
    for key in keys:
        if key in q and key in t:
            score += 2.0
    # light token overlap
    for tok in set(q.replace("/", " ").split()):
        if len(tok) >= 2 and tok in t:
            score += 0.25
    return score


def retrieve(query: str, k: int | None = None) -> list[Document]:
    """向量召回 + 关键词加权重排，Mock 伪向量下也能命中对应文档。"""
    top_k = k or settings.top_k
    vs = get_vectorstore()
    # over-fetch then rerank
    candidates = vs.similarity_search(query, k=max(top_k * 3, 8))
    ranked = sorted(
        candidates,
        key=lambda d: _keyword_score(query, d.page_content + " " + str(d.metadata)),
        reverse=True,
    )
    # de-duplicate by source+prefix
    seen: set[str] = set()
    out: list[Document] = []
    for d in ranked:
        key = f"{d.metadata.get('source')}:{d.page_content[:40]}"
        if key in seen:
            continue
        seen.add(key)
        out.append(d)
        if len(out) >= top_k:
            break
    return out
