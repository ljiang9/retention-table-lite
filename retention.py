"""retention-table-lite：按首次活跃分 cohort，计算各周期留存率矩阵。

事件数据形如 [(user_id, period), ...]，period 为可比较的周期键（如 "2026-W01"、
日期字符串、或整数周序号）。以每个用户首次出现的周期为 cohort，统计其后每个周期
仍活跃的人数与占比。
"""

from __future__ import annotations

from collections import defaultdict
from typing import Hashable


def build_retention(events: list[tuple[Hashable, object]]) -> dict:
    """根据 (user, period) 事件列表构造留存表。

    返回 dict：
    {
      "cohorts": [cohort_period, ...]（按周期升序）,
      "periods": [period_offset, ...]（0,1,2,...）,
      "matrix": [[保留率百分比, ...], ...],   # 行=cohort，列=offset
      "sizes":  [cohort_size, ...],
    }
    """
    # 每个用户首次活跃周期
    first_seen: dict[Hashable, object] = {}
    # (cohort_period, period) -> 活跃用户集合
    active: dict[tuple[object, object], set] = defaultdict(set)

    for user, period in events:
        if user not in first_seen:
            first_seen[user] = period
        active[(first_seen[user], period)].add(user)

    cohort_periods = sorted(set(first_seen.values()))
    # offset = 该周期相对 cohort 周期的差值（假设周期可排序为同一序列）
    # 为了通用，用排序后的索引差
    period_index = {p: i for i, p in enumerate(
        sorted({p for (_, p) in active}))}

    # 收集每个 cohort 的最大 offset
    rows = []
    sizes = []
    for c in cohort_periods:
        cohort_users = {u for u, fp in first_seen.items() if fp == c}
        size = len(cohort_users)
        sizes.append(size)
        row = {}
        max_off = 0
        for (cp, p), users in active.items():
            if cp != c:
                continue
            off = period_index[p] - period_index[c]
            if off >= 0:
                row[off] = len(users)
                max_off = max(max_off, off)
        # 转成留存率百分比
        row_pct = []
        for off in range(max_off + 1):
            cnt = row.get(off, 0)
            row_pct.append(round(cnt / size * 100, 1) if size else 0.0)
        rows.append(row_pct)

    max_len = max((len(r) for r in rows), default=0)
    periods = list(range(max_len))
    return {
        "cohorts": [str(c) for c in cohort_periods],
        "periods": periods,
        "matrix": rows,
        "sizes": sizes,
    }


def render_markdown(table: dict) -> str:
    """把留存矩阵渲染成 Markdown 表格。"""
    header = "| Cohort | 规模 | " + " | ".join(
        f"D{p}" if p == 0 else f"+{p}" for p in table["periods"]) + " |"
    sep = "| --- | --- | " + " | ".join(
        "---" for _ in table["periods"]) + " |"
    lines = ["# 留存表", "", header, sep]
    for c, size, row in zip(table["cohorts"], table["sizes"],
                            table["matrix"]):
        cells = [f"{v}%" for v in row]
        # 补齐
        cells += [""] * (len(table["periods"]) - len(cells))
        lines.append(f"| {c} | {size} | " + " | ".join(cells) + " |")
    return "\n".join(lines)
