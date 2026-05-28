# llm-wiki 日志

本文件只追加记录 llm-wiki 的重要操作。

推荐格式：

```markdown
## [YYYY-MM-DD] ingest | 标题

- 来源：
- 影响页面：
- 处理结果：
- 是否影响 novel/ 正文或草稿：

## [YYYY-MM-DD] query | 主题

- 问题：
- 使用页面：
- 结论：
- 是否归档为 wiki 页面：

## [YYYY-MM-DD] audit | 主题

- 检查范围：
- 发现问题：
- 处理结果：
- 是否需要用户确认：
```

## [2026-05-27] init | llm-wiki 结构初始化

- 来源：用户提供的 llm-wiki 概念说明
- 影响页面：AGENTS.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/wiki/index.md、llm-wiki/wiki/log.md
- 处理结果：建立三层资料模型和 wiki 运维规则
- 是否影响 novel/ 正文或草稿：否，当前为项目架构规则

## [2026-05-27] update | 章节龙骨机制

- 来源：用户确认每章需要简短大纲龙骨，防止长篇前后期矛盾
- 影响页面：AGENTS.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/wiki/index.md、llm-wiki/wiki/book-spine.md、llm-wiki/process/chapters/_chapter-spine-template.md、llm-wiki/wiki/timeline.md、llm-wiki/wiki/character-states.md、llm-wiki/wiki/relationship-states.md、llm-wiki/wiki/foreshadowing-ledger.md、llm-wiki/wiki/contradiction-flags.md
- 处理结果：建立全书龙骨、章节龙骨模板和章后连续性账本；规定章节完成必须同步龙骨、时间线、人物状态、关系、伏笔和矛盾标记
- 是否影响 novel/ 正文或草稿：否，当前为项目管理规则和 llm-wiki 模板

## [2026-05-28] update | AGENTS 与 Claude 规则入口同步

- 来源：用户要求排查其他文档中只指向单一项目规则文件的说明并一并修正
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md
- 处理结果：将规则引用统一为项目规则文件（AGENTS.md / Claude.md），保留 Codex 与 Claude 各自入口；Claude.md 除标题外与 AGENTS.md 保持规则内容一致
- 是否影响 novel/ 正文或草稿：否，当前为项目规则和说明文档同步

## [2026-05-28] update | llm-wiki 节点建卡门槛

- 来源：用户确认正文不进 wiki，但世界设定、人物卡、关系、场景卡、伏笔、时间线和状态追踪等结构化小文件应进入关联型知识库。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/query-prompts.md、llm-wiki/wiki/wiki图谱说明.md、llm-wiki/wiki/index.md、llm-wiki/process/chapters/_chapter-spine-template.md、llm-wiki/templates/*
- 处理结果：新增“总账 + 节点页 + 章节龙骨”三层 wiki 规则，明确人物、地点、组织、规则、物品、重要场景和伏笔的独立建卡门槛；章节完成清单新增节点缺口检查；补充人物卡、地点卡、组织卡、规则卡、物品卡、场景卡和伏笔节点模板。
- 是否影响 novel/ 正文或草稿：否，当前为智能体架构规则和模板更新。

## [2026-05-28] update | 章节龙骨移出图谱层

- 来源：用户指出最终 wiki 图谱应是高组织架构内容，不应被章节标题节点占据。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/wiki/wiki图谱说明.md、llm-wiki/wiki/index.md、llm-wiki/process/chapters/*、llm-wiki/templates/*
- 处理结果：明确章节龙骨属于流程层，迁移到 `llm-wiki/process/chapters/`；节点模板迁移到 `llm-wiki/templates/`；`wiki/index.md` 不再逐章链接章节龙骨，也不再链接模板文件，避免最终图谱被流程文件和脚手架节点污染。
- 是否影响 novel/ 正文或草稿：否，当前为智能体模板架构规则、索引和目录结构调整。

## [2026-05-28] update | 新增剧情总纲

- 来源：用户指出章节龙骨是主线推进记录，章节龙骨之外还需要大纲串联整体剧情发展脉络。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/query-prompts.md、llm-wiki/ingest-manifest.md、llm-wiki/process/流程层.md、llm-wiki/process/outline.md、llm-wiki/process/chapters/章节龙骨目录.md、llm-wiki/process/chapters/_chapter-spine-template.md、llm-wiki/wiki/index.md、llm-wiki/wiki/wiki图谱说明.md
- 处理结果：新增 `llm-wiki/process/outline.md` 作为剧情总纲，明确其位于 `wiki/book-spine.md` 和单章龙骨之间，用于记录章节组功能、阶段推进、支线咬合和后续规划；章节完成清单新增剧情总纲同步检查。
- 是否影响 novel/ 正文或草稿：否，当前为智能体模板架构和流程资料更新。

## [2026-05-28] update | 中文分类主节点命名

- 来源：用户指出不应把每个分类主节点都命名为 README，否则知识图谱中会出现大量重名节点；主内容文件应按文件夹含义命名，最好使用中文。
- 影响页面：AGENTS.md、Claude.md、README.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/wiki/index.md、llm-wiki/wiki/wiki图谱说明.md、llm-wiki/wiki/*/中文档案主节点、llm-wiki/process/流程层.md、llm-wiki/process/chapters/章节龙骨目录.md
- 处理结果：将 llm-wiki 内图谱层和流程层的 README 主节点全部改为中文语义文件名；`wiki/index.md` 仅链接分类主节点，具体档案卡由分类主节点继续关联；同步更新智能体模板规则。
- 是否影响 novel/ 正文或草稿：否，当前为知识图谱结构和智能体规则更新。

## [2026-05-28] update | 章节龙骨迁移至 novel

- 来源：用户明确要求章节龙骨按小说工程资料管理，wiki 中只保留总体大纲内容，并由总体大纲关联章节龙骨。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/query-prompts.md、llm-wiki/wiki/index.md、llm-wiki/wiki/outline.md、llm-wiki/wiki/wiki图谱说明.md、novel/03_plot/chapters/*、novel/03_plot/chapter-outline.md、novel/05_manuscript/README.md
- 处理结果：将总体大纲移动为 `llm-wiki/wiki/outline.md`，将章节龙骨目录和模板移动到 `novel/03_plot/chapters/`；规定 wiki 不再逐章收录龙骨，只通过总体大纲链接章节龙骨。
- 是否影响 novel/ 正文或草稿：否，当前为项目结构、规则和模板调整。

## [2026-05-28] update | 明确 llm-wiki 检索入口口径

- 来源：章节龙骨迁移到 `novel/03_plot/chapters/` 后，需要避免“只从 llm-wiki 读取资料”的绝对表述与新结构冲突。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、novel/00_project/brief.md
- 处理结果：统一改为“llm-wiki 是日常设定检索和资料定位入口”；单章龙骨由 `llm-wiki/wiki/outline.md` 关联后按需读取 `novel/03_plot/chapters/`。
- 是否影响 novel/ 正文或草稿：否，当前为项目结构和规则口径调整。

## [2026-05-28] update | AIGC 痕迹质量控制

- 来源：用户要求研究 AIGC 检测手段，并增加相关要求。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/aigc-quality-control.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、novel/03_plot/chapters/_chapter-spine-template.md、CHANGELOG.md
- 处理结果：新增 AIGC 检测手段研究摘要；将“反 AIGC 检测”改为合规的原创性与 AIGC 痕迹质量控制，明确不以绕过或欺骗检测器为目标；章节完成清单新增原创性与 AIGC 痕迹质量检查。
- 是否影响 novel/ 正文或草稿：否，当前为规则、文档和检查清单更新。
