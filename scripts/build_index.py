#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.ingest import build_vectorstore


def main() -> None:
    vs, n = build_vectorstore(persist=True)
    print(f"OK: indexed {n} chunks -> {vs._collection.name}")  # noqa: SLF001


if __name__ == "__main__":
    main()
