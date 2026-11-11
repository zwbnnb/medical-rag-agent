from __future__ import annotations

import json
import re
from typing import Any

from app.config import settings
from app.ingest import retrieve
from app.tools import (
    ALL_TOOLS,
    classify_blood_glucose,
    classify_blood_pressure,
    project_metrics_lookup,
)

SYSTEM_PROMPT = """你是家用医疗健康知识助手（求职 Demo），结合检索片段与工具结果回答。
规则：
1. 优先使用工具做血压/血糖数值分级；课题指标用 project_metrics_lookup。
2. 回答结构：结论 → 依据（工具或检索）→ 建议 → 一句免责声明。
3. 不做诊断、不开药；知识不足时明确说不知道。
4. 使用简体中文，控制在 200 字内除非用户要求展开。
"""


def _format_docs(docs) -> str:
    parts = []
    for i, d in enumerate(docs, 1):
        src = d.metadata.get("source", "?")
        parts.append(f"[{i}] ({src})\n{d.page_content[:600]}")
    return "\n\n".join(parts) if parts else "(无检索命中)"


def _maybe_run_tools(question: str) -> list[dict[str, Any]]:
    """启发式触发工具，保证 Mock 与真 LLM 都能展示 Function Calling 痕迹。"""
    traces: list[dict[str, Any]] = []
    q = question.replace(" ", "")

    # 血压：135/85 或 收缩压135舒张压85
    m = re.search(r"(\d{2,3})\s*/\s*(\d{2,3})", question)
    if not m:
        m = re.search(r"收缩压\s*(\d{2,3}).{0,8}舒张压\s*(\d{2,3})", question)
    if m and ("压" in q or "/" in question or "血压" in question):
        out = classify_blood_pressure.invoke(
            {"systolic": float(m.group(1)), "diastolic": float(m.group(2))}
        )
        traces.append({"tool": "classify_blood_pressure", "output": out})

    # 血糖
    gm = re.search(r"血糖[^\d]{0,6}(\d+(?:\.\d+)?)", question)
    if not gm:
        gm = re.search(r"(\d+(?:\.\d+)?)\s*mmol", question, re.I)
    if gm and ("糖" in q or "mmol" in question.lower() or "空腹" in question or "餐后" in question):
        fasting = "餐后" not in question
        out = classify_blood_glucose.invoke(
            {"value_mmol_l": float(gm.group(1)), "fasting": fasting}
        )
        traces.append({"tool": "classify_blood_glucose", "output": out})

    if any(k in question for k in ("DPLS", "dpls", "GDSC", "gdsc", "R²", "R2", "药敏", "Residual")):
        topic = "gdsc" if "GDSC" in question.upper() or "药敏" in question else "dpls"
        if "R" in question and "2" in question:
            topic = "r2"
        out = project_metrics_lookup.invoke({"topic": topic})
        traces.append({"tool": "project_metrics_lookup", "output": out})

    return traces


def _mock_answer(question: str, docs, tool_traces: list[dict[str, Any]]) -> str:
    tool_txt = "；".join(t["output"] for t in tool_traces) if tool_traces else "未触发数值/指标工具"
    snippet = docs[0].page_content[:180].replace("\n", " ") if docs else "（无片段）"
    return (
        "【结论】已结合知识库检索与工具结果作答。\n"
        f"【工具】{tool_txt}\n"
        f"【依据摘录】{snippet}…\n"
        "【建议】若涉及身体不适或紧急症状，请及时就医；本系统为实习作品 Demo，不提供诊疗。\n"
        "（Mock LLM 模式：设置 MOCK_LLM=false 并配置 API Key 可切换真实大模型）"
    )


def run_agent(question: str) -> dict[str, Any]:
    docs = retrieve(question)
    tool_traces = _maybe_run_tools(question)
    context = _format_docs(docs)

    if settings.mock_llm or not settings.openai_api_key:
        answer = _mock_answer(question, docs, tool_traces)
        return {
            "mode": "mock",
            "answer": answer,
            "contexts": [
                {"source": d.metadata.get("source"), "text": d.page_content[:400]}
                for d in docs
            ],
            "tool_traces": tool_traces,
        }

    # Real LLM path (OpenAI-compatible)
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage

    llm = ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_api_base,
        temperature=0.2,
    )
    # Bind tools for demonstration; also inject heuristic tool results into prompt
    llm_with_tools = llm.bind_tools(ALL_TOOLS)
    tool_block = json.dumps(tool_traces, ensure_ascii=False)
    user = (
        f"用户问题：{question}\n\n"
        f"检索片段：\n{context}\n\n"
        f"已执行工具结果（可直接引用）：{tool_block}\n\n"
        f"请作答。"
    )
    msg = llm_with_tools.invoke(
        [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user)]
    )

    # If model requests more tools, execute once
    extra_traces = list(tool_traces)
    if getattr(msg, "tool_calls", None):
        name2fn = {t.name: t for t in ALL_TOOLS}
        for call in msg.tool_calls:
            fn = name2fn.get(call["name"])
            if not fn:
                continue
            out = fn.invoke(call.get("args") or {})
            extra_traces.append({"tool": call["name"], "output": out})
        follow = (
            f"用户问题：{question}\n工具结果：{json.dumps(extra_traces, ensure_ascii=False)}\n"
            f"检索：\n{context}\n请给出最终中文回答。"
        )
        msg = llm.invoke(
            [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=follow)]
        )

    answer = msg.content if isinstance(msg.content, str) else str(msg.content)
    return {
        "mode": "llm",
        "answer": answer,
        "contexts": [
            {"source": d.metadata.get("source"), "text": d.page_content[:400]}
            for d in docs
        ],
        "tool_traces": extra_traces,
    }
