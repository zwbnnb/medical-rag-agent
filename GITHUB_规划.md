# GitHub 开源规划 · medical-rag-agent

## 目标

把 `medical_rag_agent` 做成可公开的作品集仓库，简历填写：

`https://github.com/<你的用户名>/medical-rag-agent`

投杭州/苏州 AI 校招与线上实习时，可附链接 + 投屏演示。

---

## 仓库设定（建议）

| 项 | 建议 |
| --- | --- |
| 仓库名 | `medical-rag-agent` |
| 可见性 | **Public** |
| 简介 | `RAG + tool-calling agent for home-health Q&A (LangChain · Chroma · FastAPI)` |
| Topics | `langchain`, `rag`, `fastapi`, `agent`, `chromadb`, `python`, `llm` |
| License | MIT（演示代码，知识库为自写科普） |

---

## 分步计划

### Step 1｜本地就绪（本次可做）

- [x] 代码可跑、五题回归、README / .gitignore / .env.example  
- [x] `git init` + 首次提交（不含 `.env` / `chroma_db` / `.venv`）  
- [ ] 你提供 **GitHub 用户名**（或网页新建空仓库后把 URL 给我）

### Step 2｜你在网页建仓（2 分钟）

1. 打开 https://github.com/new  
2. Repository name: `medical-rag-agent`  
3. Public；**不要**勾选 Add README（本地已有）  
4. Create repository  

### Step 3｜推送（有用户名后执行）

```bash
cd medical_rag_agent
git remote add origin git@github.com:<USERNAME>/medical-rag-agent.git
# 或 HTTPS: https://github.com/<USERNAME>/medical-rag-agent.git
git branch -M main
git push -u origin main
```

若本机无 SSH Key：用 HTTPS + Personal Access Token，或先 `ssh-keygen` 再加到 GitHub Settings。

### Step 4｜推送后同步简历

把链接填进：

- `简历_AI算法_杭苏校招.md` 的 GitHub 栏与项目 2  
- `求职投递_GrokBot候选人画像.md` 第 1 / 9 节  
- PPT 里「GitHub待开源」改为真实 URL  

### Step 5｜增强（可选，面试前）

- README 顶栏 badges + 3 张截图（`screenshots/`）  
- 真 Key 跑 1 题对比 Mock（截图）  
- 以后再补 Docker / GitHub Actions  

---

## 不会进仓库的内容

`.env`、`.venv/`、`chroma_db/`、`tests/last_run.jsonl`、任何 API Key。

## 公开说明

知识库为求职 Demo 自写科普 + 课题摘要，非诊疗建议；见 README 免责声明。
