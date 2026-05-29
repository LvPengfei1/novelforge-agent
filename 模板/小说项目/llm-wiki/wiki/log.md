# llm-wiki 日志

本文件只追加记录 llm-wiki 的重要操作。

说明：历史条目记录当时的目录和规则状态，不代表当前最新规则。当前规则以根目录 `AGENTS.md` / `Claude.md`、最新日志条目和当前实际目录为准。

推荐格式：

```markdown
## [YYYY-MM-DD] ingest | 标题

- 来源：
- 影响页面：
- 处理结果：
- 是否影响 小说工程/ 正文或草稿：

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
- 是否影响 小说工程/ 正文或草稿：否，当前为项目架构规则

## [2026-05-27] update | 章节龙骨机制

- 来源：用户确认每章需要简短大纲龙骨，防止长篇前后期矛盾
- 影响页面：AGENTS.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/wiki/index.md、llm-wiki/wiki/book-spine.md、llm-wiki/process/chapters/_chapter-spine-template.md、llm-wiki/wiki/timeline.md、llm-wiki/wiki/character-states.md、llm-wiki/wiki/relationship-states.md、llm-wiki/wiki/foreshadowing-ledger.md、llm-wiki/wiki/contradiction-flags.md
- 处理结果：建立全书龙骨、章节龙骨模板和章后连续性账本；规定章节完成必须同步龙骨、时间线、人物状态、关系、伏笔和矛盾标记
- 是否影响 小说工程/ 正文或草稿：否，当前为项目管理规则和 llm-wiki 模板

## [2026-05-28] update | AGENTS 与 Claude 规则入口同步

- 来源：用户要求排查其他文档中只指向单一项目规则文件的说明并一并修正
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md
- 处理结果：将规则引用统一为项目规则文件（AGENTS.md / Claude.md），保留 Codex 与 Claude 各自入口；Claude.md 除标题外与 AGENTS.md 保持规则内容一致
- 是否影响 小说工程/ 正文或草稿：否，当前为项目规则和说明文档同步

## [2026-05-28] update | llm-wiki 节点建卡门槛

- 来源：用户确认正文不进 wiki，但世界设定、人物卡、关系、场景卡、伏笔、时间线和状态追踪等结构化小文件应进入关联型知识库。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/query-prompts.md、llm-wiki/wiki/wiki图谱说明.md、llm-wiki/wiki/index.md、llm-wiki/process/chapters/_chapter-spine-template.md、llm-wiki/模板/*
- 处理结果：新增“总账 + 节点页 + 章节龙骨”三层 wiki 规则，明确人物、地点、组织、规则、物品、重要场景和伏笔的独立建卡门槛；章节完成清单新增节点缺口检查；补充人物卡、地点卡、组织卡、规则卡、物品卡、场景卡和伏笔节点模板。
- 是否影响 小说工程/ 正文或草稿：否，当前为智能体架构规则和模板更新。

## [2026-05-28] update | 章节龙骨移出图谱层

- 来源：用户指出最终 wiki 图谱应是高组织架构内容，不应被章节标题节点占据。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/wiki/wiki图谱说明.md、llm-wiki/wiki/index.md、llm-wiki/process/chapters/*、llm-wiki/模板/*
- 处理结果：明确章节龙骨属于流程层，迁移到 `llm-wiki/process/chapters/`；节点模板迁移到 `llm-wiki/模板/`；`wiki/index.md` 不再逐章链接章节龙骨，也不再链接模板文件，避免最终图谱被流程文件和脚手架节点污染。
- 是否影响 小说工程/ 正文或草稿：否，当前为智能体模板架构规则、索引和目录结构调整。

## [2026-05-28] update | 新增剧情总纲

- 来源：用户指出章节龙骨是主线推进记录，章节龙骨之外还需要大纲串联整体剧情发展脉络。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/query-prompts.md、llm-wiki/ingest-manifest.md、llm-wiki/process/流程层.md、llm-wiki/process/outline.md、llm-wiki/process/chapters/章节龙骨目录.md、llm-wiki/process/chapters/_chapter-spine-template.md、llm-wiki/wiki/index.md、llm-wiki/wiki/wiki图谱说明.md
- 处理结果：新增 `llm-wiki/process/outline.md` 作为剧情总纲，明确其位于 `wiki/book-spine.md` 和单章龙骨之间，用于记录章节组功能、阶段推进、支线咬合和后续规划；章节完成清单新增剧情总纲同步检查。
- 是否影响 小说工程/ 正文或草稿：否，当前为智能体模板架构和流程资料更新。

## [2026-05-28] update | 中文分类主节点命名

- 来源：用户指出不应把每个分类主节点都命名为 README，否则知识图谱中会出现大量重名节点；主内容文件应按文件夹含义命名，最好使用中文。
- 影响页面：AGENTS.md、Claude.md、README.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/wiki/index.md、llm-wiki/wiki/wiki图谱说明.md、llm-wiki/wiki/*/中文档案主节点、llm-wiki/process/流程层.md、llm-wiki/process/chapters/章节龙骨目录.md
- 处理结果：将 llm-wiki 内图谱层和流程层的 README 主节点全部改为中文语义文件名；`wiki/index.md` 仅链接分类主节点，具体档案卡由分类主节点继续关联；同步更新智能体模板规则。
- 是否影响 小说工程/ 正文或草稿：否，当前为知识图谱结构和智能体规则更新。

## [2026-05-28] update | 章节龙骨迁移至 novel

- 来源：用户明确要求章节龙骨按小说工程资料管理，wiki 中只保留总体大纲内容，并由总体大纲关联章节龙骨。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/query-prompts.md、llm-wiki/wiki/index.md、llm-wiki/wiki/outline.md、llm-wiki/wiki/wiki图谱说明.md、小说工程/03_剧情/章节/*、小说工程/03_剧情/chapter-outline.md、小说工程/05_正文/README.md
- 处理结果：将总体大纲移动为 `llm-wiki/wiki/outline.md`，将章节龙骨目录和模板移动到 `小说工程/03_剧情/章节/`；规定 wiki 不再逐章收录龙骨，只通过总体大纲链接章节龙骨。
- 是否影响 小说工程/ 正文或草稿：否，当前为项目结构、规则和模板调整。

## [2026-05-28] update | 明确 llm-wiki 检索入口口径

- 来源：章节龙骨迁移到 `小说工程/03_剧情/章节/` 后，需要避免“只从 llm-wiki 读取资料”的绝对表述与新结构冲突。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、小说工程/00_项目概况/brief.md
- 处理结果：统一改为“llm-wiki 是日常设定检索和资料定位入口”；单章龙骨由 `llm-wiki/wiki/outline.md` 关联后按需读取 `小说工程/03_剧情/章节/`。
- 是否影响 小说工程/ 正文或草稿：否，当前为项目结构和规则口径调整。

## [2026-05-28] update | AIGC 痕迹质量控制

- 来源：用户要求研究 AIGC 检测手段，并增加相关要求。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/aigc-quality-control.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、小说工程/03_剧情/章节/_chapter-spine-template.md、CHANGELOG.md
- 处理结果：新增 AIGC 检测手段研究摘要；将“反 AIGC 检测”改为合规的原创性与 AIGC 痕迹质量控制，明确不以绕过或欺骗检测器为目标；章节完成清单新增原创性与 AIGC 痕迹质量检查。
- 是否影响 小说工程/ 正文或草稿：否，当前为规则、文档和检查清单更新。

## [2026-05-28] update | 修正人物表达表述

- 来源：用户指出原表述容易被理解为语音或影视概念，不适合小说规则。
- 影响页面：AGENTS.md、Claude.md、docs/aigc-quality-control.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/query-prompts.md、llm-wiki/llm-wiki说明.md
- 处理结果：统一改为“人物文字表达差异”或“人物表达同质”，明确指小说中的对白、内心独白、叙述视角、句式和信息表达方式。
- 是否影响 小说工程/ 正文或草稿：否，当前为规则措辞修正。

## [2026-05-28] update | 增加 AIGC 文本检测原理审核依据

- 来源：用户要求在智能体配置中增加依据 `AIGC_DETECTION_PRINCIPLES.md` 的内容审核。
- 影响页面：AIGC_DETECTION_PRINCIPLES.md、AGENTS.md、Claude.md、README.md、README.en.md、docs/aigc-quality-control.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/query-prompts.md、小说工程/03_剧情/章节/*
- 处理结果：将 `AIGC_DETECTION_PRINCIPLES.md` 设为原创性与 AIGC 痕迹质量检查依据；若正文呈现过度平滑可预测、句式机械、重复模式明显、人物表达同质、场景缺少具体细节、片段风格断裂、参考资料拼贴等特征，应标记为文本质量风险并按小说质量目标修正。
- 是否影响 小说工程/ 正文或草稿：否，当前为规则、文档和检查清单更新。

## [2026-05-28] update | 明确 AIGC 检测原理作为文本优化方向

- 来源：用户澄清目的不是对抗 AIGC 检测，而是把 AIGC 文本检测中的观察维度作为文本优化方向。
- 影响页面：AIGC_DETECTION_PRINCIPLES.md、AGENTS.md、Claude.md、README.md、README.en.md、docs/aigc-quality-control.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/query-prompts.md、小说工程/03_剧情/章节/*、小说工程/05_正文/README.md、CHANGELOG.md
- 处理结果：统一改为“原创性与文本质量检查”；凡正文明显呈现过度平滑、句式机械、重复模式、人物表达同质、场景缺少具体细节、片段风格断裂、参考资料拼贴或同义替换式洗稿等特征，均判定为质量不合格，必须修改后复查。
- 是否影响 小说工程/ 正文或草稿：否，当前为规则、文档和检查清单更新。

## [2026-05-28] update | 调整文本质量检查顺序

- 来源：用户要求检测步骤应在原正文内容完成后，再进行审核、检测和修改。
- 影响页面：AGENTS.md、Claude.md、AIGC_DETECTION_PRINCIPLES.md、README.md、README.en.md、docs/aigc-quality-control.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/query-prompts.md、小说工程/03_剧情/章节/*、小说工程/05_正文/README.md、CHANGELOG.md
- 处理结果：明确流程顺序为“正文初稿完成 -> 原创性与文本质量检查 -> 修改 -> 复查 -> 章节同步”，禁止在初稿未完成时为了检查项反复中断正文生成。
- 是否影响 小说工程/ 正文或草稿：否，当前为规则、文档和检查清单更新。

## [2026-05-28] update | 增加关联文件强制同步规则

- 来源：用户反馈文章更新后部分关联内容不会一起更新，需要增加更明确的同步规则。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/query-prompts.md、小说工程/03_剧情/章节/*、小说工程/05_正文/README.md、CHANGELOG.md
- 处理结果：新增“关联文件强制同步”矩阵，明确修改正文、章节龙骨、人物卡、世界设定、伏笔、时间线、剧情总纲、全书龙骨、wiki 页面和 novel 镜像摘要后的必检关联文件；无需更新的关联文件也必须说明“已检查，无需更新”。
- 是否影响 小说工程/ 正文或草稿：否，当前为规则、文档和检查清单更新。

## [2026-05-28] audit | 全面审查规则重复与吸收写作工作流优点

- 来源：用户要求全面审查智能体文档，排查重复、啰嗦、矛盾设置，并吸收公众号写作 skill 中适合小说项目的优点；读者反馈回流暂不加入。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/wiki/wiki图谱说明.md、llm-wiki/wiki/index.md、llm-wiki/query-prompts.md、llm-wiki/模板/*、小说工程/03_剧情/章节/_chapter-spine-template.md、CHANGELOG.md
- 处理结果：新增小说阶段流程、证据等级与写前研究触发规则、避坑清单；统一 `llm-wiki` 为日常资料检索和定位入口；修正索引更新口径为“索引入口或摘要变化时更新”；为节点模板补充证据等级和来源依据字段；历史日志增加说明，避免旧路径被误认为当前规则。
- 是否影响 小说工程/ 正文或草稿：否，当前为规则、文档和模板更新。

## [2026-05-28] audit | 精简重复规则说明

- 来源：用户要求全面排查不必要声明，列出并精简重复、啰嗦设置。
- 影响页面：AGENTS.md、Claude.md、docs/aigc-quality-control.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、llm-wiki/query-prompts.md、小说工程/03_剧情/章节/章节龙骨目录.md、小说工程/05_正文/README.md、llm-wiki/wiki/log.md
- 处理结果：保留 `AGENTS.md` / `Claude.md` 作为强规则源头；将使用手册、方案和 wiki 说明中的重复流程、AIGC 细则和同步矩阵改为短说明或引用；删除主动规则中的公众号、读者反馈回流等外部写作场景声明。
- 是否影响 小说工程/ 正文或草稿：否，当前为规则与说明文档精简。

## [2026-05-28] architecture | 区分框架仓库与小说实例

- 来源：用户反馈正式开写后，小说正文和设定会污染框架仓库，导致智能体优化不易单独提交。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、CHANGELOG.md、docs/project-instance-guide.md、docs/usage-guide.md、docs/novel-agent-plan.md、templates/README.md、projects/README.md、.gitignore、模板/小说项目/*
- 处理结果：将空小说项目骨架迁入 `模板/小说项目/`；新增被 Git 忽略的 `projects/` 本地实例目录；明确真实小说应复制模板到 `projects/<novel-slug>/` 或仓库外部目录，框架仓库只提交规则、文档和空模板。
- 是否影响 小说工程/ 正文或草稿：否，当前为仓库结构和模板位置调整。
