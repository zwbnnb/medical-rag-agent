# Medical RAG Agent Demo

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-green)
![LangChain](https://img.shields.io/badge/LangChain-RAG%20%2B%20Tools-orange)

面向杭州/苏州 **2027 届 AI 算法·技术开发校招** 与 **线上实习** 的作品集项目：家用医疗监测科普问答 + 课题知识库 RAG，本地可跑，暂不上云。

## 亮点（约 200 字）

本 Demo 用 Python + LangChain 工具调用 + Chroma 向量检索 + FastAPI 网页，把「血压/血糖示意分级」做成确定性 Function Calling，把说明书级科普与 Residual-DPLS / GDSC 药敏课题摘要做成可引用知识库，回答强制「结论→依据→建议→免责」。默认 `MOCK_LLM=true` 无 API Key 也能完整演示检索与工具轨迹；换成通义千问 / OpenAI 兼容接口即可切真实大模型。场景贴合家用医疗器械智能客服与健康数据算法交叉，适合作为线上实习证明「我能交付可跑的 Agent，而不是只会聊概念」。

## 技术栈

| 层 | 选型 |
| --- | --- |
| Agent / Tools | LangChain `@tool` + 绑定工具的 ChatOpenAI |
| RAG | Markdown 知识库 → 切分 → Chroma |
| API / UI | FastAPI + 单页 `static/index.html` |
| LLM | 通义千问兼容模式 / 任意 OpenAI-compatible（可 Mock） |

未用 Milvus：本地 Demo 用 Chroma 更轻；上线时可替换为 Milvus/FAISS，接口已隔离在 `app/ingest.py`。

## 知识库从哪来（结合你的现状）

| 文件 | 内容 |
| --- | --- |
| `01/02` | 血压、血糖家庭监测科普（医疗器械客服高频） |
| `03` | 智能客服话术边界（合规 / 反幻觉） |
| `04/05` | 你的 Residual-DPLS 与 GDSC 实验量级摘要（生信×AI） |

## 快速开始（本地）

```bash
cd medical_rag_agent
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# 1) 建索引
python scripts/build_index.py

# 2) 五题自测（产出 tests/last_run.jsonl，便于截图）
python scripts/run_tests.py

# 3) 启动网页
uvicorn app.main:app --host 127.0.0.1 --port 8000
# 浏览器打开 http://127.0.0.1:8000
```

### 切换真实大模型

编辑 `.env`：

```env
MOCK_LLM=false
OPENAI_API_KEY=你的Key
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus
EMBED_MODEL=text-embedding-v3
```

然后重建索引（嵌入会走真实 Embedding）并重启服务。

## 五道标准测试题

1. 血压 135/85 算高吗？该怎么测更准？  
2. 空腹血糖 6.5 mmol/L 需要注意什么？  
3. 智能客服能不能直接给人开降压药？  
4. Residual-DPLS 公开基准大概多少 R²？  
5. GDSC 药敏实验大概用了多少样本？  

自测后请截图：终端五题输出、网页问答、`/docs` 接口页。简历可写：「独立交付 Medical RAG Agent（LangChain + Chroma + FastAPI），含工具调用与 5 题回归用例」。

## 目录

```
medical_rag_agent/
  app/           # config / ingest / tools / agent / FastAPI
  data/knowledge # 知识库 Markdown
  scripts/       # build_index / run_tests
  static/        # 简易网页
  tests/         # 标准问题与运行结果
```

## 面试与推送

- 演示话术：见 [`面试演示脚本.md`](./面试演示脚本.md)（8–10 分钟三连问）  
- 推 GitHub：见 [`GITHUB_推送清单.md`](./GITHUB_推送清单.md)

## 暂不做（按你的要求）

- 云服务器 / Docker 公网部署：本地跑通并截图即可投递；需要上线时再补 `Dockerfile` 与 Nginx。  
- 真实诊疗指南全文：避免版权与合规风险，当前为科普 + 课题自有摘要。

## 免责声明

本项目仅用于技术演示与求职，不提供医疗诊断或用药建议。
