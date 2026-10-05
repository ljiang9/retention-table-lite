"""retention-table-lite 命令行入口。

用法示例：
    python3 cli.py                 # 运行内置示例
    python3 cli.py --file events.csv   # CSV：user,period
"""

from __future__ import annotations

import argparse
import sys

from retention import build_retention, render_markdown


# 内置示例事件
SAMPLE = [
    ("u1", 0), ("u2", 0), ("u3", 0), ("u4", 0),
    ("u1", 1), ("u2", 1), ("u3", 1),
    ("u1", 2), ("u2", 2),
    ("u5", 1), ("u6", 1), ("u7", 1),
    ("u5", 2), ("u6", 2),
    ("u5", 3),
]


def load_csv(path: str) -> list[tuple[str, int]]:
    out = []
    with open(path, encoding="utf-8") as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip()]
    if lines and "user" in lines[0].lower():
        lines = lines[1:]
    for ln in lines:
        parts = ln.replace(" ", "").split(",")
        if len(parts) >= 2:
            try:
                out.append((parts[0], int(parts[1])))
            except ValueError:
                continue
    return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="retention-table-lite",
        description="按首次活跃分 cohort，生成留存率矩阵",
    )
    p.add_argument("--file", help="事件 CSV：user,period（可选）")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    events = load_csv(args.file) if args.file else SAMPLE
    table = build_retention(events)
    print(render_markdown(table))
    return 0


if __name__ == "__main__":
    sys.exit(main())
