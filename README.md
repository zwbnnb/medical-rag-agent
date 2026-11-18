# Medical RAG Agent

Home-health Q&A agent with **RAG + tool calling**, served by FastAPI.

Pipeline:

```
user question → vector retrieve → optional tools → grounded answer
```

## Features

- LangChain tools for blood-pressure / blood-glucose classification (deterministic, auditable)
- Chroma-backed RAG over Markdown knowledge files (swap-ready in `app/ingest.py`)
- FastAPI + simple web UI (`static/index.html`)
- Offline mock mode (`MOCK_LLM=true`) for retrieve + tool traces without an API key
- Regression suite: `scripts/run_tests.py` + `tests/test_questions.json`

## Stack

| Layer | Choice |
| --- | --- |
| Agent / tools | LangChain `@tool`, OpenAI-compatible chat API |
| RAG | RecursiveCharacterTextSplitter + Chroma |
| Serving | FastAPI |
| LLM | DashScope / any OpenAI-compatible endpoint (or mock) |

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

python scripts/build_index.py
python scripts/run_tests.py
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000

### Real LLM

```env
MOCK_LLM=false
OPENAI_API_KEY=...
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus
EMBED_MODEL=text-embedding-v3
```

Rebuild the index after enabling real embeddings.

## Knowledge base

| File | Topic |
| --- | --- |
| `01` / `02` | Home BP / glucose monitoring notes |
| `03` | Assistant safety / refusal boundaries |
| `04` / `05` | Public research notes (method summary & GDSC FAQ; not proprietary source code) |

## Layout

```
app/              # config, ingest, tools, agent, API
data/knowledge/   # RAG corpus
scripts/          # build_index, run_tests
static/           # web UI
tests/            # fixed questions
```

## Disclaimer

Educational / engineering demo only. Not medical advice. Knowledge texts are general summaries.
