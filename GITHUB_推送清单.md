# 推到 GitHub 清单（本机执行）

当前环境无 `gh` CLI。在你自己电脑或已登录 GitHub 的终端按下面做。

## 建议仓库名

`medical-rag-agent`  
一句话简介：`Home-health RAG Agent with LangChain tools + Chroma + FastAPI (internship portfolio)`

## 推送步骤

```bash
cd /path/to/medical_rag_agent

# 确认不要提交密钥与向量库缓存
cat .gitignore   # 应含 .env / chroma_db / .venv / tests/last_run.jsonl

# 独立仓库（推荐，不要和 trim 大仓绑死）
git init
git add app data/knowledge scripts static tests requirements.txt \
  README.md .env.example .gitignore 面试演示脚本.md GITHUB_推送清单.md
git status   # 确认没有 .env、chroma_db、.venv

git commit -m "$(cat <<'EOF'
Add medical RAG agent demo for internship portfolio.

Local-runnable LangChain tools + Chroma + FastAPI with five regression questions.
EOF
)"

# 在 GitHub 网页新建空仓库 medical-rag-agent 后：
git branch -M main
git remote add origin git@github.com:<你的用户名>/medical-rag-agent.git
git push -u origin main
```

## README 顶部可再加（推送后）

```markdown
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-green)
![LangChain](https://img.shields.io/badge/LangChain-RAG%20%2B%20Tools-orange)
```

并把克隆地址写进简历项目栏。

## 投递邮件可附

- GitHub 链接  
- 「本地 3 分钟可跑；可约屏幕共享演示」  
- 附件：2–3 张截图（网页问答 / 工具轨迹 / 五题自测）
