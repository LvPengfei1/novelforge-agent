# NovelForge-Agent

NovelForge-Agent 是一个面向长篇小说创作的智能体框架。它使用 `llm-wiki` 作为小说资料的日常检索入口，通过全书龙骨、总体大纲、章节龙骨、人物状态账本、伏笔账本和矛盾标记，帮助作者在持续创作中保持主线、人物、时间线和设定一致。单章龙骨存放在 `novel/03_plot/chapters/`，由 `llm-wiki/wiki/outline.md` 统一关联。

本项目不是具体小说正文，而是一套可复用的小说写作项目结构、智能体行为规则和确定性章节封包工具。它不会替模型判断故事好坏；代码负责拒绝未批准或已被改动的正本、越界输入路径和写作/审稿封包混用，并且只向任务封包提供显式声明的材料。

封包白名单不是操作系统沙箱。通过 `invoke` 启动的外部命令仍可能按其自身权限读取磁盘或网络；需要强文件隔离时，应在容器、受限工作区或其他宿主沙箱中运行。框架只对自己组装和记录的输入作保证。

真实小说请放在 `projects/<novel-slug>/` 或仓库外部目录；本仓库根目录只提交智能体框架、文档和空项目模板。这样开始创作后，正文和私有设定不会影响框架优化提交。

## 文档入口

- 英文版 README：[README.en.md](README.en.md)
- AIGC 文本检测原理：[AIGC_DETECTION_PRINCIPLES.md](AIGC_DETECTION_PRINCIPLES.md)
- 默认独立审稿协议：[NOVEL_REVIEW_PROTOCOL.md](NOVEL_REVIEW_PROTOCOL.md)
- 使用手册：[docs/usage-guide.md](docs/usage-guide.md)
- 小说实例分离说明：[docs/project-instance-guide.md](docs/project-instance-guide.md)
- AIGC 质量控制：[docs/aigc-quality-control.md](docs/aigc-quality-control.md)
- Codex 项目规则：[AGENTS.md](AGENTS.md)
- Codex Skill 入口：[SKILL.md](SKILL.md)
- Claude 项目规则：[Claude.md](Claude.md)
- 完整方案：[docs/novel-agent-plan.md](docs/novel-agent-plan.md)
- 修改记录：[CHANGELOG.md](CHANGELOG.md)
- 1.0.3 发布摘要：[docs/releases/v1.0.3.md](docs/releases/v1.0.3.md)

## 核心目标

- 让每一本小说作为独立项目持续创作。
- 用 `llm-wiki` 管理所有长期使用的设定、人物、主线、时间线、伏笔和状态。
- 用“剧情总纲”串联章节组功能和整体发展脉络，用“章节龙骨”记录每章开章状态、核心推进和结尾变化，减少长篇前后矛盾。
- 使用“架构批准 -> 章节输入白名单 -> 全新写作子智能体 -> 全新审查子智能体 -> 主控整合 -> 章后同步”的流程，并用证据等级区分已确立事实和 AI 推断。
- 每个新章节使用不继承主对话的全新写作子智能体；它固定读取已批准的项目简报、全书龙骨、总体大纲和文风正本，同时只接收本章相关资料与必要的前章结尾。
- 正文初稿完成后，由另一个全新审查子智能体依据 `NOVEL_REVIEW_PROTOCOL.md` 做整章读稿、近章结构比较和语言复查；不合格则重构并复查，再进入章节同步。
- 将原始资料、正文草稿和可检索知识库分层管理。
- 让 AI 写作、续写、审查和设定维护都有稳定原则可依；具体字段、检查项和示例口径以当前模板和小说实例为准。

## 目录结构

```text
.
├── AGENTS.md
├── Claude.md
├── SKILL.md
├── NOVEL_REVIEW_PROTOCOL.md
├── agents
├── README.md
├── README.en.md
├── NOTICE
├── LICENSE
├── docs
│   ├── novel-agent-plan.md
│   ├── project-instance-guide.md
│   └── usage-guide.md
├── novelforge_agent
├── scripts
│   └── novelforge.py
├── tests
├── templates
│   └── novel-project
│       ├── raw
│       ├── novel
│       └── llm-wiki
└── projects
    └── README.md
```

`templates/novel-project/` 是空小说项目模板；`projects/` 用于本地小说实例，默认被 Git 忽略。

## 新建小说实例

推荐直接运行：

```powershell
python scripts/novelforge.py init projects/<novel-slug>
```

该命令复制 `templates/novel-project/`，并把根目录的 `AGENTS.md`、`Claude.md`、`AIGC_DETECTION_PRINCIPLES.md`、`NOVEL_REVIEW_PROTOCOL.md` 放入小说实例。目标目录非空时命令会拒绝覆盖。也可以手工完成同样的复制。

`approve` 不只读取状态字样，还会校验项目简报的故事发动机、全书龙骨的长线动力、总体大纲的完整阶段行和文风正本的叙事基准；通过后才记录四份正本哈希。

之后在 `projects/<novel-slug>/` 中写正文和维护设定。框架优化仍在仓库根目录提交。

## 三层资料模型

以下目录均指复制后的小说实例内部路径。

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

章节正文写完但质量检查、必要修改复查、关联文件同步、剧情总纲、章节龙骨和连续性账本未完成，不算真正完成该章。

如当前小说实例、用户要求或目标平台设置了章节字数口径，应在章节龙骨和同步日志中验收；没有明确口径时，不把固定字数范围写成框架全局规则。剧情节点明显过长时，应优先拆章或调整章节结构。

`llm-wiki` 应按关联型知识库维护：正文原文不进 wiki，但世界设定、人物卡、地点卡、组织卡、规则卡、重要场景卡、伏笔、时间线、关系和状态追踪都应进入 wiki。人物、地点、组织、规则、物品、重要场景或伏笔达到复用门槛时，必须建立独立节点页；不能只停留在 `index.md` 摘要、总账表或 `novel/` 模板中。

## 推荐工作流

1. 将原始资料放入 `raw/`。
2. 将需要长期检索、交叉引用和防矛盾的内容整理进 `llm-wiki/`。
3. 确认项目简报、全书龙骨和总体大纲属于同一已批准架构；否则停止正文写作。
4. 在用户明确确认后运行 `approve`，把批准依据、版本和四份正本哈希写入批准快照。
5. 复制章节龙骨和章节任务模板，显式填写本章资料路径、前章衔接范围和最多三份审稿比较材料。
6. 运行 `python scripts/novelforge.py prepare <project> --job <job>`；只有架构与白名单校验通过才生成 `writer-task.md`。
7. 启动不继承主对话的全新写作子智能体；它只接收 `writer-task.md`，不得自行全库搜索。
8. 正文产生后运行 `prepare-review`，再启动另一个全新审查子智能体读取 `reviewer-task.md`，完成整章读稿和近章结构比较。
9. 主智能体完成取舍与最小整合；审查通过后同步关联文件、节点缺口和日志。
10. 每完成一段连续创作、一次大规模回改或一次设定集中更新后，将 `llm-wiki` 当前结论同步为 `novel/` 下对应摘要备份。

## 命令行工具

```powershell
# 用户明确批准架构后，绑定当前四份正本的版本与哈希
python scripts/novelforge.py approve projects/<novel-slug> --confirmation "用户确认依据"

# 校验全局架构与批准快照
python scripts/novelforge.py validate projects/<novel-slug>

# 校验本章并生成隔离写作任务
python scripts/novelforge.py prepare projects/<novel-slug> --job novel/03_plot/chapters/ch001-job.json

# 正文写入后生成独立审稿任务
python scripts/novelforge.py prepare-review projects/<novel-slug> --run <prepare 输出的目录>
```

`manifest.json` 记录实际进入封包的相对路径、用途、行号范围和 SHA-256。每次 `invoke` 都从当前已批准 job 重新派生预期来源与任务，拒绝伪造或陈旧封包；生成审稿任务时还会锁定待审正文哈希，正文变化后旧审稿包立即失效。

`invoke` 只接受直接可执行程序，拒绝 `.cmd`、`.bat` 和常见命令解释器，并以 `shell=False` 分别启动写作与审稿新进程。它仍不是磁盘或网络沙箱。

## 关键文件

- `AGENTS.md`：智能体通用行为原则。
- `Claude.md`：Claude 工作流使用的通用行为原则，规则内容应与 `AGENTS.md` 保持等价。
- `SKILL.md`：Codex 中的标准工作流入口。
- `NOVEL_REVIEW_PROTOCOL.md`：默认独立审稿正本。
- `scripts/novelforge.py`：初始化、批准、校验、封包和外部进程调用入口。
- `README.en.md`：英文版项目说明。
- `docs/usage-guide.md`：从零开始使用 NovelForge-Agent 的中文手册。
- `docs/project-instance-guide.md`：框架仓库与小说实例分离说明。
- `docs/novel-agent-plan.md`：完整方案说明。
- `templates/novel-project/`：可复制的小说项目模板。
- `templates/novel-project/novelforge.json`：机器可读的全局正本、审稿原则和禁读路径配置。
- `templates/novel-project/novel/03_plot/chapters/_chapter-job-template.json`：每章显式输入任务模板。
- `templates/novel-project/llm-wiki/wiki/book-spine.md`：全书龙骨模板。
- `templates/novel-project/llm-wiki/wiki/outline.md`：剧情总纲模板。
- `templates/novel-project/novel/03_plot/chapters/_chapter-spine-template.md`：章节龙骨模板。

## 许可证

本项目使用 Apache License 2.0 开源。

如果你修改本项目并分发修改后的版本，必须清楚标注已做修改，并说明主要变更。详见 `LICENSE` 和 `NOTICE`。
