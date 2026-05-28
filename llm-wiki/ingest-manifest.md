# llm-wiki 摄入清单

本文件记录需要摄入、整理或重新同步到 llm-wiki 的资料。

状态可用：

- `pending`：待摄入
- `ingested`：已摄入
- `review`：需要人工审查 llm-wiki 输出
- `conflict`：发现矛盾，待处理
- `superseded`：已被新版本取代

| 状态 | 资料或页面 | 处理原因 | 涉及条目 | 最近处理 |
| --- | --- | --- | --- | --- |
| pending | raw/ | 原始资源层 | 用户资料、外部来源 | 按需导入 |
| pending | llm-wiki/process/outline.md | 剧情总纲 | 章节组功能、阶段推进、支线咬合、后续规划 | 按章节组维护 |
| pending | llm-wiki/process/chapters/ | 章节龙骨 | 章节推进、结尾变化、后续约束 | 按章维护 |
| ingested | llm-wiki/wiki/book-spine.md | 初始化全书龙骨 | 主线、阶段、当前进度 | 2026-05-27 初始化 |
| ingested | llm-wiki/wiki/timeline.md | 初始化时间线账本 | 事件顺序 | 2026-05-27 初始化 |
| ingested | llm-wiki/wiki/character-states.md | 初始化人物状态账本 | 人物状态 | 2026-05-27 初始化 |
| ingested | llm-wiki/wiki/relationship-states.md | 初始化关系状态账本 | 人物关系 | 2026-05-27 初始化 |
| ingested | llm-wiki/wiki/foreshadowing-ledger.md | 初始化伏笔账本 | 伏笔、回收、限制 | 2026-05-27 初始化 |
| ingested | llm-wiki/wiki/contradiction-flags.md | 初始化矛盾标记 | 连续性矛盾 | 2026-05-27 初始化 |

## 更新规则

每次修改人物、设定、主线、章节龙骨、时间线或伏笔后，都要在表格中补充一行或更新状态。

不要把临时讨论直接加入摄入清单。用户明确提供的原始资料先进入 `raw/`；需要长期检索、交叉引用和防矛盾的内容必须进入 `llm-wiki/`。只有正文草稿、章节成稿或写作过程文件写入 `novel/`。
