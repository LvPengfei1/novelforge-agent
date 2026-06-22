# llm-wiki 接入说明

本目录用于按 llm-wiki 模式管理小说项目设定。在没有专用工具时，Codex 可按 `AGENTS.md` 维护 wiki，Claude 可按 `Claude.md` 维护 wiki。

## 定位

llm-wiki 是小说资料的日常检索和定位入口。写作、查询、审查和连续性检查，应优先从本目录定位资料；单章龙骨通过 `wiki/outline.md` 链接到 `../novel/03_plot/chapters/` 后按需读取。

- `raw/` 保存不可改写的原始资源。
- `novel/` 保存正文草稿、章节成稿和写作过程文件。
- `llm-wiki/` 保存 LLM 维护的 wiki、摄入清单、查询提示、日志和矛盾处理记录。
- `AIGC_DETECTION_PRINCIPLES.md` 保存 AIGC 文本检测原理，是原创性与文本质量检查依据。
- `docs/aigc-quality-control.md` 保存 AIGC 检测手段研究摘要和原创性质量控制规则。

所有长期使用的设定、人物、主线、时间线、伏笔和状态，都必须进入 `llm-wiki/`。如果 wiki 页面缺失或矛盾，再回查 `raw/` 或 `novel/`，并把有效结论补回 wiki。

`llm-wiki` 应按关联型知识库维护。总账型文件用于快速扫描，节点型小文件用于快速组建上下文。正文原文不进入 wiki；正文产生的人物、地点、组织、规则、物品、重要场景、伏笔、时间线、关系和状态变化必须抽取后进入 wiki。

## 证据等级

wiki 页面中的重要设定、研究结论和推断应标注证据等级。具体等级和写前研究触发条件以 `AGENTS.md` / `Claude.md` 为准。

## 推荐目录

```text
llm-wiki
├── llm-wiki说明.md
├── ingest-manifest.md
├── query-prompts.md
├── sources
├── templates
│   ├── character-card-template.md
│   ├── location-card-template.md
│   ├── organization-card-template.md
│   ├── rule-card-template.md
│   ├── item-card-template.md
│   ├── scene-card-template.md
│   └── foreshadowing-node-template.md
├── wiki
│   ├── book-spine.md
│   ├── character-states.md
│   ├── contradiction-flags.md
│   ├── foreshadowing-ledger.md
│   ├── index.md
│   ├── log.md
│   ├── outline.md
│   ├── relationship-states.md
│   ├── timeline.md
│   ├── characters
│   ├── locations
│   ├── organizations
│   ├── rules
│   ├── items
│   ├── scenes
│   └── foreshadowing
└── logs
```

目录职责：

- `ingest-manifest.md`：记录哪些源文件需要摄入或重新摄入。
- `query-prompts.md`：保存常用查询问题。
- `sources/`：如 llm-wiki 需要独立输入源，可放置复制或导出的源文件。
- `wiki/book-spine.md`：全书主线龙骨和当前进度。
- `wiki/outline.md`：总体大纲，串联章节龙骨、章节组功能和阶段推进；只保留总体内容和章节龙骨链接。
- `../novel/03_plot/chapters/`：每章剧情龙骨，属于小说工程层，不纳入最终 wiki 图谱。
- `wiki/timeline.md`：事件时间线。
- `wiki/character-states.md`：人物当前状态。
- `wiki/relationship-states.md`：人物关系状态。
- `wiki/foreshadowing-ledger.md`：伏笔账本。
- `wiki/contradiction-flags.md`：待处理矛盾。
- `wiki/index.md`：顶层索引，只关联分类主节点，不逐章列出章节龙骨、模板或具体档案卡。
- `wiki/log.md`：时间日志，只追加记录导入、查询、审查和健康检查。
- `wiki/characters/`：人物卡。达到复用门槛的人物必须独立成页。
- `wiki/locations/`：地点卡。多章出现或带有空间规则的地点必须独立成页。
- `wiki/organizations/`：组织、势力和群体卡。
- `wiki/rules/`：修行、符法、世界运行规则和术语说明。
- `wiki/items/`：重要道具、证据、账册、符物和可复用物品。
- `wiki/scenes/`：复杂或可复用重要场景卡。
- `wiki/foreshadowing/`：需要独立追踪的伏笔节点。
- `wiki/`：保存 LLM 生成或导出的最终图谱节点页面；具体档案卡必须写入对应分类主节点，`index.md` 只维护分类主节点入口。
- `templates/`：保存人物卡、地点卡、组织卡、规则卡、物品卡、场景卡和伏笔节点模板，不纳入最终图谱。
- `logs/`：保存摄入日志、矛盾检查日志、人工处理记录。

## 使用流程

本文件是操作摘要。通用原则以根目录项目规则文件（`AGENTS.md` / `Claude.md`）为准；具体字段、路径和同步检查清单以当前小说实例和 `novel/03_plot/chapters/_chapter-spine-template.md` 为准。

### 1. 导入前

先更新 `ingest-manifest.md`，列出本次要处理的资料、目标 wiki 页面、原因和状态。

优先处理：

1. `raw/` 中新增的原始资料。
2. 用户当前明确补充的设定、人物、剧情或规则。
3. `novel/05_manuscript/` 中已经产生设定变化、人物变化、伏笔或关键事件的章节。
4. `novel/03_plot/chapters/` 中新增或变更的章节龙骨。

正文章节不建议全部长期摄入。只有当章节包含已确定的设定变化、人物变化、伏笔或关键事件时，才摄入或摘要后摄入。

外部资料和用户原始说明应先放入 `raw/`，再从中抽取条目进入 wiki。只有正文草稿、章节成稿或写作过程文件进入 `novel/`。

节点建卡门槛：

- 人物出场超过 2 章、推动关键剧情、与主角关系持续变化、有秘密/动机/阵营/语言习惯/禁止写法/未回收伏笔，或后续需要复用其性格和状态时，必须建立人物卡。
- 地点多章出现、具有空间结构、路线、入口、禁忌、机关、历史或危险规则，或后续行动需要复用其方位和限制时，必须建立地点卡。
- 组织、规则、术语、物品只要影响人物选择、冲突成本、世界运行、修行体系、主线支线或后续口径，就必须建立独立节点页。
- 重要场景只有在复杂、可复用、存在空间调度、关键证据链或伏笔作用时建立场景卡。

### 2. 写作前

先读取 `wiki/index.md`，再查询或读取相关 wiki 页面：

- 剧情总纲如何安排当前章节组？
- 当前章节龙骨是否存在？
- 当前章节承接上一章哪些状态变化？
- 当前章节涉及哪些人物？
- 这些人物的当前状态、动机、关系是什么？
- 当前地点和规则有哪些限制？
- 哪些伏笔必须延续或不能提前揭示？
- 是否存在与当前场景相关的矛盾提示？

写正文前还必须从当前项目资料派生临时“内容执行标准”，再整理“内容上下文胶囊”。内容执行标准用于确定本次写作的类型题材、目标读者、文风基准、核心看点、禁用写法、章节功能、人物状态、核心冲突和本章阅读感；内容上下文胶囊只保留正文生成需要的故事信息，不包含同步检查表、文件路径、内部流程、操作说明或日志。

只有当 wiki 缺失、矛盾或需要证据时，才回查 `raw/` 或 `novel/`；回查后的有效结论必须补回 wiki。

### 3. 写作后

如果正文产生新事实：

1. 更新对应章节龙骨。
2. 更新 `book-spine.md`、`wiki/outline.md`、`timeline.md`、`character-states.md`、`relationship-states.md`、`foreshadowing-ledger.md`。
3. 如发现矛盾，更新 `contradiction-flags.md`。
4. 更新相关 wiki 页面。
5. 更新对应分类主节点；如索引入口或摘要变化，再更新 `wiki/index.md`。
6. 将变更追加到 `wiki/log.md`。
7. 将处理结果写入 `llm-wiki/logs/`。
8. 如正文或章节规划受影响，再更新 `novel/`。
9. 执行节点缺口检查：触发建卡门槛的内容若只存在于 `index.md` 摘要、分类主节点摘要、总账表或 `novel/` 模板中，不算同步完成。
10. 执行关联文件同步检查；无变化的关联文件说明“已检查，无需更新”。
11. 正文初稿完成后，依据 `AIGC_DETECTION_PRINCIPLES.md` 执行原创性与文本质量检查；不合格内容必须修改复查。
12. 执行正文自然度、项目匹配度、工程词转译和读者侧复读检查；如果正文更像流程记录而不是小说，应补戏、转译或重写。

章节正文写完但章节龙骨、剧情总纲和连续性账本未同步，不算真正完成该章。

正文文件必须保持纯净，只包含章节标题和正文。章末变更记录、同步检查、修改原因和审查记录，应写入章节龙骨、连续性资料或 `wiki/log.md`，不要写进 `novel/05_manuscript/`。

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
- 不要让达到复用门槛的人物、地点、组织、规则、物品、重要场景或伏笔只停留在总账表、分类主节点摘要或 `index.md` 摘要中。
- 不要把全部正文无筛选塞给 wiki。
- 不要跳过章节龙骨直接进入下一章。
- 不要让 wiki 自动改写人物核心动机、主线方向或结局，除非用户明确要求。
