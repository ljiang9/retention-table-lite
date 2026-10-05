# retention-table-lite

零依赖的**队列留存表（Cohort Retention）生成器**：根据「用户 + 周期」事件，按每个用户**首次活跃**的周期分 cohort，计算其后每个周期的留存率矩阵，并渲染成 Markdown 表格。内置示例事件，无需任何 API。

## 功能简介

- 自动把用户按首次出现周期分组（cohort）。
- 计算 cohort 内「第 0 期 = 100%」，其后每期仍活跃人数占比。
- 输出按 cohort 行、偏移周期列的留存矩阵 Markdown 表格。

## 快速开始

```bash
# 运行内置示例
python3 cli.py

# 用自己的事件 CSV（两列：user,period）
python3 cli.py --file events.csv
```

输出形如：

```
# 留存表
| Cohort | 规模 | D0 | +1 | +2 | +3 |
| 0 | 4 | 100.0% | 75.0% | 50.0% | 25.0% |
| 1 | 3 | 100.0% | 66.7% | 33.3% | |
```

## 无 API key 如何运行

本项目**完全不需要 API key**，纯本地规则统计。

## 目录说明

```
retention-table-lite/
├── retention.py   # build_retention / render_markdown
├── cli.py       # 命令行入口（含内置示例事件）
├── tests/
│   └── test_retention.py
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## License

MIT License，Copyright (c) 2026 ljiang9。
