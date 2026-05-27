# NovelForge-Agent

NovelForge-Agent 是一个面向长篇小说创作的智能体框架。它使用 `llm-wiki` 作为小说资料的日常唯一入口，通过章节龙骨、全书龙骨、人物状态账本、伏笔账本和矛盾标记，帮助作者在持续创作中保持主线、人物、时间线和设定一致。

本项目不是具体小说正文，而是一套可复用的小说写作项目结构和智能体行为规则。

## 核心目标

- 让每一本小说作为独立项目持续创作。
- 用 `llm-wiki` 管理所有长期使用的设定、人物、主线、时间线、伏笔和状态。
- 用“章节龙骨”记录每章开章状态、核心推进和结尾变化，减少长篇前后矛盾。
- 将原始资料、正文草稿和可检索知识库分层管理。
- 让 AI 写作、续写、审查和设定维护都有稳定规则可依。

## 目录结构

```text
.
├── claude.md
├── NOTICE
├── LICENSE
├── docs
│   └── novel-agent-plan.md
├── raw
│   └── README.md
├── novel
│   ├── 00_project
│   ├── 01_world
│   ├── 02_characters
│   ├── 03_plot
│   ├── 04_scenes
│   ├── 05_manuscript
│   ├── 06_research
│   ├── 07_continuity
│   └── 08_archive
└── llm-wiki
    ├── README.md
    ├── ingest-manifest.md
    ├── query-prompts.md
    ├── logs
    ├── sources
    └── wiki
        ├── book-spine.md
        ├── timeline.md
        ├── character-states.md
        ├── relationship-states.md
        ├── foreshadowing-ledger.md
        ├── contradiction-flags.md
        ├── index.md
        ├── log.md
        └── chapters
            └── _chapter-spine-template.md
```

## 三层资料模型

### `raw/`

原始资源层。保存用户提供的资料、网页剪藏、参考文章、图片和导入材料。该目录只读，不改写。

### `novel/`

小说工程层。保存正文草稿、章节成稿、写作过程文件和必要备份。它不是日常设定检索入口。

### `llm-wiki/`

资料与设定层。保存由智能体维护的 wiki 页面、索引、日志、查询记录和矛盾检查结果。日常写作、查询、审查和连续性检查都优先从这里读取资料。

## 章节龙骨机制

每章必须在 `llm-wiki/wiki/chapters/` 下维护一个章节龙骨文件，例如：

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

章节正文写完但章节龙骨和连续性账本未同步，不算真正完成该章。

## 推荐工作流

1. 将原始资料放入 `raw/`。
2. 将需要长期检索、交叉引用和防矛盾的内容整理进 `llm-wiki/`。
3. 写作前读取 `llm-wiki/wiki/index.md`、`book-spine.md`、当前章节龙骨和相关人物/伏笔/时间线页面。
4. 写正文到 `novel/05_manuscript/`。
5. 写完后同步章节龙骨、全书龙骨、时间线、人物状态、关系状态、伏笔账本、矛盾标记、索引和日志。

## 关键文件

- `claude.md`：智能体项目级行为规则。
- `docs/novel-agent-plan.md`：完整方案说明。
- `llm-wiki/wiki/book-spine.md`：全书龙骨。
- `llm-wiki/wiki/chapters/_chapter-spine-template.md`：章节龙骨模板。
- `llm-wiki/wiki/index.md`：llm-wiki 内容索引。
- `llm-wiki/wiki/log.md`：llm-wiki 操作日志。

## 许可证

本项目使用 Apache License 2.0 开源。

如果你修改本项目并分发修改后的版本，必须清楚标注已做修改，并说明主要变更。详见 `LICENSE` 和 `NOTICE`。

