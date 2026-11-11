#!/usr/bin/env python3
"""跑 5 道标准测试题，结果写入 tests/last_run.jsonl，便于截图留档。"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agent import run_agent


def main() -> None:
    qpath = ROOT / "tests" / "test_questions.json"
    questions = json.loads(qpath.read_text(encoding="utf-8"))
    out_path = ROOT / "tests" / "last_run.jsonl"
    lines = []
    print("=" * 60)
    print("Medical RAG Agent · 5 题自测")
    print("=" * 60)
    for i, item in enumerate(questions, 1):
        q = item["question"]
        print(f"\n[{i}] Q: {q}")
        result = run_agent(q)
        print(f"    mode={result['mode']}")
        print(f"    tools={[t['tool'] for t in result['tool_traces']]}")
        print(f"    A: {result['answer'][:240]}...")
        lines.append(
            {
                "ts": datetime.now(timezone.utc).isoformat(),
                "id": item.get("id", i),
                "question": q,
                "expect_tools": item.get("expect_tools", []),
                "result": result,
            }
        )
    out_path.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in lines) + "\n",
        encoding="utf-8",
    )
    print("\n" + "=" * 60)
    print(f"已保存：{out_path}")
    print("请对终端输出与网页 http://127.0.0.1:8000 截图留档。")


if __name__ == "__main__":
    main()
