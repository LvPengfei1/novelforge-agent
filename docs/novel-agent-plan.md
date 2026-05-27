# 小说写作智能体方案

## 可行性判断

这套思路可行，而且适合长篇小说项目。你补充的 llm-wiki 内容说明重点不在某个具体工具，而在一种知识库维护模式：原始资料不可改，LLM 维护中间 wiki，项目规则文件规定工作流。用于小说项目时，它可以解决长篇写作中最常见的三个问题：设定散落、人物变化丢失、伏笔和时间线难以长期维护。

- `src`、`backend` 这类代码目录对应小说中的“正文”“设定”“人物”“主线”“连续性资料”。
- 人物性格、经历、关系和剧情推进会不断变化，适合单独建档并持续更新。
- 主线内容应保持压缩版，作为每次写作前的高密度上下文入口。
- 具体写某个角色、地点或场景时，只读取相关文件，避免把所有设定一次性塞入上下文。
- llm-wiki 作为小说资料的日常唯一入口，负责快速查找、交叉引用、矛盾检查和上下文压缩。
- 每一本小说都应视为一个独立项目，默认持续向后创作；只有在确有必要时才小范围回改前文，并同步检查受影响设定。
- 每章必须维护简短剧情龙骨，用于记录开章状态、核心推进和结尾变化，防止长篇前后矛盾。

需要注意的是：小说资料库不能只建目录，还要有维护规则。否则后期会出现正文推进了，但人物状态、伏笔表、时间线没有同步更新的问题。

## 推荐架构

```text
E:\小说智能体
├── claude.md
├── docs
│   └── novel-agent-plan.md
├── raw
│   ├── assets
│   ├── imports
│   └── notes
├── llm-wiki
│   ├── README.md
│   ├── ingest-manifest.md
│   ├── query-prompts.md
│   ├── sources
│   ├── wiki
│   │   ├── book-spine.md
│   │   ├── character-states.md
│   │   ├── contradiction-flags.md
│   │   ├── foreshadowing-ledger.md
│   │   ├── index.md
│   │   ├── log.md
│   │   ├── relationship-states.md
│   │   ├── timeline.md
│   │   └── chapters
│   │       ├── README.md
│   │       └── _chapter-spine-template.md
│   └── logs
└── novel
    ├── 00_project
    │   └── brief.md
    ├── 01_world
    │   ├── locations.md
    │   ├── organizations.md
    │   ├── rules.md
    │   └── terminology.md
    ├── 02_characters
    │   ├── _character-template.md
    │   └── relationships.md
    ├── 03_plot
    │   ├── mainline.md
    │   ├── branches.md
    │   └── chapter-outline.md
    ├── 04_scenes
    │   └── _scene-template.md
    ├── 05_manuscript
    │   └── README.md
    ├── 06_research
    │   └── README.md
    ├── 07_continuity
    │   ├── timeline.md
    │   ├── foreshadowing.md
    │   └── state-tracker.md
    └── 08_archive
        └── README.md
```

## 核心使用流程

### 0. 三层资料模型

`raw/` 是原始资源层，保存用户原始资料、参考文章、网页剪藏、图片和外部来源。这个层只读，不改写。

`novel/` 是小说工程层，保存正文草稿、章节成稿、写作过程文件和必要备份。它不是日常设定检索入口。

`llm-wiki/` 是资料与设定层，保存由智能体维护的 wiki 页面、索引、日志、查询记录和矛盾检查。日常写作、查询和连续性检查只从这里读取资料。

### 0.1 单本小说项目边界

每一本小说都是一个独立项目。当前目录只服务当前这一本小说。

如果未来同一工作区需要管理多本小说，应为每本小说建立独立目录，分别维护 `raw/`、`novel/`、`llm-wiki/` 和项目规则。不同小说不能共用人物库、设定库和主线索引，除非用户明确要求共享宇宙或系列化设定。

### 1. 开始写作前

读取：

1. `llm-wiki/wiki/index.md`
2. `llm-wiki/wiki/log.md`，仅在需要了解最近变化时读取
3. `llm-wiki/wiki/book-spine.md`
4. 当前章节和相邻章节龙骨
5. llm-wiki 中与当前任务相关的人物、地点、组织、规则、主线、伏笔和状态页面
6. `llm-wiki/ingest-manifest.md`，仅在需要确认未摄入资料时读取
7. `novel/05_manuscript/` 中对应章节正文，仅在续写、改写或核对原文时读取

然后压缩成当前写作上下文：

- 主线进展
- 当前章节目标
- 出场人物状态
- 当前冲突
- 必须延续的伏笔
- 不能违背的设定

### 2. 写作过程中

正文写在 `novel/05_manuscript/`。

建议命名：

```text
ch001.md
ch002.md
ch003.md
```

场景素材写在 `novel/04_scenes/`。

建议命名：

```text
ch001-scene-01.md
ch001-scene-02.md
```

### 2.1 章节龙骨

本节是方案摘要。强制规则以 `claude.md` 和 `llm-wiki/wiki/chapters/_chapter-spine-template.md` 的同步检查清单为准。

每章必须在 `llm-wiki/wiki/chapters/` 下维护一个章节龙骨文件。

命名：

```text
ch001-spine.md
ch002-spine.md
ch003-spine.md
```

章节龙骨不是详细大纲，也不是正文摘要。它只记录防矛盾所需的骨架信息：

- 本章在全书中的功能。
- 开章时的时间、地点、人物状态、已知信息和未解决冲突。
- 本章目标，包括剧情目标、人物目标、读者获得的信息和不能提前揭示的内容。
- 本章真正推进的 1-3 个关键事件。
- 章末状态变化，包括事件、人物、关系、信息差、道具、地点和伏笔变化。
- 后文不能违背的事实。
- 待回收问题。

写正文前先建立章节龙骨草案；写正文后按实际内容修正。章节龙骨建议 300-800 字，复杂章节最多 1200 字。

章节完成标准：正文已写入或更新，并完成章节龙骨模板中的同步检查清单。

### 3. 写作完成后

根据正文变化同步更新：

- llm-wiki 主线页面：压缩主线进度。
- llm-wiki 章节龙骨：记录本章核心推进和结尾变化。
- llm-wiki 时间线页面：时间推进和事件顺序。
- llm-wiki 伏笔页面：新增或回收伏笔。
- llm-wiki 人物页面：经历、关系、性格变化、当前状态。
- llm-wiki 世界设定页面：新地点、新组织、新规则、新术语。
- `llm-wiki/wiki/index.md`：新增或更新页面索引。
- `llm-wiki/wiki/log.md`：记录本次变更。
- `llm-wiki/logs/`：记录矛盾、合并建议和人工处理结果。

### 3.1 前文回改

小说默认持续向后推进。前文回改只在必要时执行：

- 错字、病句、称谓、局部语气可以直接修。
- 时间线、人物状态、道具、信息差等连续性问题，需要同步检查后续章节。
- 世界规则、人物经历、组织关系、主线因果等设定级修改，需要先列影响范围。
- 章节顺序、关键事件、人物弧线、伏笔位置等结构级修改，需要先确认方案，再动正文。

回改后必须同步更新：

- 受影响章节。
- llm-wiki 人物页面和人物历程。
- llm-wiki 主线压缩页面。
- llm-wiki 时间线页面。
- llm-wiki 伏笔页面。
- llm-wiki 状态追踪页面。
- llm-wiki 索引、相关页面和日志。

### 4. llm-wiki 同步原则

llm-wiki 是日常资料入口。它负责：

- 从 `raw/`、`novel/` 和用户当前说明中抽取人物、地点、组织、规则、物品、伏笔和事件页面。
- 在页面之间建立 `[[wikilinks]]`。
- 发现重复设定和潜在矛盾。
- 帮助写作前快速检索相关上下文。

其他目录负责：

- `raw/` 保存原始证据，不改写。
- `novel/` 保存正文草稿、成稿和写作过程文件。
- `docs/` 保存项目方案和工作流程。

### 5. llm-wiki 日志和索引

`llm-wiki/wiki/index.md` 是内容索引，按人物、地点、组织、规则、剧情、伏笔、来源等分类记录 wiki 页面和一句话摘要。写作或查询前先读它。

`llm-wiki/wiki/log.md` 是时间日志，只追加记录导入、查询、审查、健康检查和人工确认。它让智能体知道最近发生了什么，避免重复处理。

`llm-wiki/wiki/chapters/` 是章节龙骨目录。它保存每章剧情发展的最短可用骨架，是后期查找前文影响和排查矛盾的入口。

日志建议使用固定前缀：

```markdown
## [2026-05-27] ingest | 资料标题
## [2026-05-27] query | 查询主题
## [2026-05-27] audit | 检查主题
```

## 关键约束

- 所有设定必须落文件，不依赖对话记忆。
- 日常资料查询只走 llm-wiki；源文件只用于证据回查或正文核对。
- 每章必须维护章节龙骨；没有完成章后状态同步，不算真正完成该章。
- `raw/` 中原始资源不得被改写。
- 不相关设定不进上下文。
- 主线文件要短，必须可快速读取。
- 人物文件可以细，但每个人单独存放。
- 人物变化要记录“变化原因”，不能只写变化结果。
- 废弃设定归档，不直接删除。
- 正文是最终产出，资料库只服务正文。

## 后续可扩展

如果项目后续变成多智能体协作，可以增加：

- `agents/outline-agent.md`：大纲智能体。
- `agents/character-agent.md`：人物一致性智能体。
- `agents/continuity-agent.md`：连续性审查智能体。
- `agents/style-agent.md`：文风润色智能体。

当前阶段建议先使用一个项目级 `claude.md`，避免过早拆分导致维护成本上升。

## 当前本机状态

本项目已经建立 llm-wiki 目录和规则；即使没有专用工具，也可以由 Codex 按 `claude.md`、`llm-wiki/README.md`、`llm-wiki/wiki/index.md` 和 `llm-wiki/wiki/log.md` 维护这套知识库。
