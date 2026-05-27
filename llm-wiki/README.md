# llm-wiki 接入说明

本目录用于按 llm-wiki 模式管理小说项目设定。在没有专用工具时，Codex 也应按本目录规则维护 wiki。

## 定位

llm-wiki 是小说资料的日常唯一入口。写作、查询、审查和连续性检查，应优先从本目录读取资料。

- `raw/` 保存不可改写的原始资源。
- `novel/` 保存正文草稿、章节成稿和写作过程文件。
- `llm-wiki/` 保存 LLM 维护的 wiki、摄入清单、查询提示、日志和矛盾处理记录。

所有长期使用的设定、人物、主线、时间线、伏笔和状态，都必须进入 `llm-wiki/`。如果 wiki 页面缺失或矛盾，再回查 `raw/` 或 `novel/`，并把有效结论补回 wiki。

## 推荐目录

```text
llm-wiki
├── README.md
├── ingest-manifest.md
├── query-prompts.md
├── sources
├── wiki
│   ├── book-spine.md
│   ├── character-states.md
│   ├── contradiction-flags.md
│   ├── foreshadowing-ledger.md
│   ├── index.md
│   ├── log.md
│   ├── relationship-states.md
│   ├── timeline.md
│   └── chapters
│       ├── README.md
│       └── _chapter-spine-template.md
└── logs
```

目录职责：

- `ingest-manifest.md`：记录哪些源文件需要摄入或重新摄入。
- `query-prompts.md`：保存常用查询问题。
- `sources/`：如 llm-wiki 需要独立输入源，可放置复制或导出的源文件。
- `wiki/book-spine.md`：全书主线龙骨和当前进度。
- `wiki/chapters/`：每章剧情龙骨。
- `wiki/timeline.md`：事件时间线。
- `wiki/character-states.md`：人物当前状态。
- `wiki/relationship-states.md`：人物关系状态。
- `wiki/foreshadowing-ledger.md`：伏笔账本。
- `wiki/contradiction-flags.md`：待处理矛盾。
- `wiki/index.md`：内容索引，按分类列出所有 wiki 页面。
- `wiki/log.md`：时间日志，只追加记录导入、查询、审查和健康检查。
- `wiki/`：保存 LLM 生成或导出的 wiki 页面。
- `logs/`：保存摄入日志、矛盾检查日志、人工处理记录。

## 使用流程

本文件是操作摘要。强制规则以根目录 `AGENTS.md` 和 `wiki/chapters/_chapter-spine-template.md` 的同步检查清单为准。

### 1. 导入前

先更新 `ingest-manifest.md`，列出本次要处理的资料、目标 wiki 页面、原因和状态。

优先处理：

1. `raw/` 中新增的原始资料。
2. 用户当前明确补充的设定、人物、剧情或规则。
3. `novel/05_manuscript/` 中已经产生设定变化、人物变化、伏笔或关键事件的章节。
4. `llm-wiki/wiki/chapters/` 中新增或变更的章节龙骨。

正文章节不建议全部长期摄入。只有当章节包含已确定的设定变化、人物变化、伏笔或关键事件时，才摄入或摘要后摄入。

外部资料和用户原始说明应先放入 `raw/`，再从中抽取条目进入 wiki。只有正文草稿、章节成稿或写作过程文件进入 `novel/`。

### 2. 写作前

先读取 `wiki/index.md`，再查询或读取相关 wiki 页面：

- 当前章节龙骨是否存在？
- 当前章节承接上一章哪些状态变化？
- 当前章节涉及哪些人物？
- 这些人物的当前状态、动机、关系是什么？
- 当前地点和规则有哪些限制？
- 哪些伏笔必须延续或不能提前揭示？
- 是否存在与当前场景相关的矛盾提示？

只有当 wiki 缺失、矛盾或需要证据时，才回查 `raw/` 或 `novel/`；回查后的有效结论必须补回 wiki。

### 3. 写作后

如果正文产生新事实：

1. 更新对应章节龙骨。
2. 更新 `book-spine.md`、`timeline.md`、`character-states.md`、`relationship-states.md`、`foreshadowing-ledger.md`。
3. 如发现矛盾，更新 `contradiction-flags.md`。
4. 更新相关 wiki 页面。
5. 更新 `wiki/index.md`。
6. 将变更追加到 `wiki/log.md`。
7. 将处理结果写入 `llm-wiki/logs/`。
8. 如正文或章节规划受影响，再更新 `novel/`。

章节正文写完但章节龙骨和连续性账本未同步，不算真正完成该章。

### 4. 健康检查

定期检查：

- 孤立页面。
- 缺少独立页面的重要概念。
- 页面之间的矛盾。
- 被新设定取代的旧说法。
- 缺失的 `[[wikilinks]]`。
- 需要补充研究或用户确认的空白。

## 禁止事项

- 不要把 LLM 自动生成 wiki 内容直接当成正式设定。
- 不要让重要设定只停留在 `raw/` 或 `novel/`，必须整理进 wiki。
- 不要把全部正文无筛选塞给 wiki。
- 不要跳过章节龙骨直接进入下一章。
- 不要让 wiki 自动改写人物核心动机、主线方向或结局，除非用户明确要求。
