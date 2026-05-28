# NovelForge-Agent

NovelForge-Agent 是一个面向长篇小说创作的智能体框架。它使用 `llm-wiki` 作为小说资料的日常检索入口，通过全书龙骨、总体大纲、章节龙骨、人物状态账本、伏笔账本和矛盾标记，帮助作者在持续创作中保持主线、人物、时间线和设定一致。单章龙骨存放在 `novel/03_plot/chapters/`，由 `llm-wiki/wiki/outline.md` 统一关联。

本项目不是具体小说正文，而是一套可复用的小说写作项目结构和智能体行为规则。

## 文档入口

- 英文版 README：[README.en.md](README.en.md)
- 使用手册：[docs/usage-guide.md](docs/usage-guide.md)
- Codex 项目规则：[AGENTS.md](AGENTS.md)
- Claude 项目规则：[Claude.md](Claude.md)
- 完整方案：[docs/novel-agent-plan.md](docs/novel-agent-plan.md)
- 修改记录：[CHANGELOG.md](CHANGELOG.md)
- 1.0.1 发布摘要：[docs/releases/v1.0.1.md](docs/releases/v1.0.1.md)

## 核心目标

- 让每一本小说作为独立项目持续创作。
- 用 `llm-wiki` 管理所有长期使用的设定、人物、主线、时间线、伏笔和状态。
- 用“剧情总纲”串联章节组功能和整体发展脉络，用“章节龙骨”记录每章开章状态、核心推进和结尾变化，减少长篇前后矛盾。
- 将原始资料、正文草稿和可检索知识库分层管理。
- 让 AI 写作、续写、审查和设定维护都有稳定规则可依。

## 目录结构

```text
.
├── AGENTS.md
├── Claude.md
├── README.md
├── README.en.md
├── NOTICE
├── LICENSE
├── docs
│   ├── novel-agent-plan.md
│   └── usage-guide.md
├── raw
│   └── README.md
├── novel
│   ├── 00_project
│   ├── 01_world
│   ├── 02_characters
│   ├── 03_plot
│   │   └── chapters
│   ├── 04_scenes
│   ├── 05_manuscript
│   ├── 06_research
│   ├── 07_continuity
│   └── 08_archive
└── llm-wiki
    ├── llm-wiki说明.md
    ├── ingest-manifest.md
    ├── query-prompts.md
    ├── templates
    │   ├── character-card-template.md
    │   ├── location-card-template.md
    │   ├── organization-card-template.md
    │   ├── rule-card-template.md
    │   ├── item-card-template.md
    │   ├── scene-card-template.md
    │   └── foreshadowing-node-template.md
    ├── logs
    ├── sources
    └── wiki
        ├── book-spine.md
        ├── timeline.md
        ├── character-states.md
        ├── relationship-states.md
        ├── foreshadowing-ledger.md
        ├── contradiction-flags.md
        ├── outline.md
        ├── index.md
        ├── log.md
        ├── characters
        ├── locations
        ├── organizations
        ├── rules
        ├── items
        ├── scenes
        └── foreshadowing
```

## 三层资料模型

### `raw/`

原始资源层。保存用户提供的资料、网页剪藏、参考文章、图片和导入材料。该目录只读，不改写。

### `novel/`

小说工程层。保存正文草稿、章节成稿、写作过程文件和必要备份。它不是日常设定检索入口。

### `llm-wiki/`

资料与设定层。保存由智能体维护的 wiki 页面、索引、日志、查询记录和矛盾检查结果。日常写作、查询、审查和连续性检查都优先从这里读取资料。

其中 `llm-wiki/wiki/` 是最终图谱节点层；`llm-wiki/wiki/outline.md` 是剧情总纲，用于串联章节龙骨和整体发展脉络；`novel/03_plot/chapters/` 保存单章龙骨。

## 章节龙骨机制

每章必须在 `novel/03_plot/chapters/` 下维护一个章节龙骨文件，例如：

```text
ch001-spine.md
ch002-spine.md
ch003-spine.md
```

章节龙骨只记录防矛盾所需的骨架信息：

- 章节功能
- 开章状态
- 本章目标
- 核心推进
- 结尾变化
- 后续约束
- 待回收问题

章节正文写完但剧情总纲、章节龙骨和连续性账本未同步，不算真正完成该章。

章节还必须完成字数验收：默认约 3000 字，单章正文不得低于 2500 字，不得高于 4000 字。统计默认按连载平台“正文字数”口径，不计章节标题，正文去除空白字符后统计；如目标平台后台给出正文字数，以后台显示为准。剧情节点过长时，应拆为同名章节的上下、中下、上中下，或使用（1）（2）（3）（4）等编号。

`llm-wiki` 应按关联型知识库维护：正文原文不进 wiki，但世界设定、人物卡、地点卡、组织卡、规则卡、重要场景卡、伏笔、时间线、关系和状态追踪都应进入 wiki。人物、地点、组织、规则、物品、重要场景或伏笔达到复用门槛时，必须建立独立节点页；不能只停留在 `index.md` 摘要、总账表或 `novel/` 模板中。

## 推荐工作流

1. 将原始资料放入 `raw/`。
2. 将需要长期检索、交叉引用和防矛盾的内容整理进 `llm-wiki/`。
3. 写作前读取 `llm-wiki/wiki/index.md`、`book-spine.md`、`llm-wiki/wiki/outline.md`、当前章节龙骨和相关人物/伏笔/时间线页面。
4. 写正文到 `novel/05_manuscript/`。
5. 写完后同步章节龙骨、剧情总纲、全书龙骨、时间线、人物状态、关系状态、伏笔账本、矛盾标记、索引和日志。
6. 每完成一段连续创作、一次大规模回改或一次设定集中更新后，将 `llm-wiki` 当前结论同步为 `novel/00_project/`、`novel/01_world/`、`novel/02_characters/`、`novel/03_plot/`、`novel/07_continuity/` 中的可读摘要备份，避免这些文件长期停留在空模板状态。
7. 执行节点缺口检查，确认触发建卡门槛的人物、地点、组织、规则、物品、重要场景和伏笔已建立或更新独立 wiki 页面。

## 关键文件

- `AGENTS.md`：智能体项目级行为规则。
- `Claude.md`：Claude 工作流使用的项目级行为规则，规则内容应与 `AGENTS.md` 保持等价。
- `README.en.md`：英文版项目说明。
- `docs/usage-guide.md`：从零开始使用 NovelForge-Agent 的中文手册。
- `docs/novel-agent-plan.md`：完整方案说明。
- `llm-wiki/wiki/book-spine.md`：全书龙骨。
- `llm-wiki/wiki/outline.md`：剧情总纲。
- `novel/03_plot/chapters/_chapter-spine-template.md`：章节龙骨模板。
- `llm-wiki/wiki/index.md`：llm-wiki 内容索引。
- `llm-wiki/wiki/log.md`：llm-wiki 操作日志。

## 许可证

本项目使用 Apache License 2.0 开源。

如果你修改本项目并分发修改后的版本，必须清楚标注已做修改，并说明主要变更。详见 `LICENSE` 和 `NOTICE`。
