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
- 处理结果：新增"总账 + 节点页 + 章节龙骨"三层 wiki 规则，明确人物、地点、组织、规则、物品、重要场景和伏笔的独立建卡门槛；章节完成清单新增节点缺口检查；补充人物卡、地点卡、组织卡、规则卡、物品卡、场景卡和伏笔节点模板。
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

- 来源：章节龙骨迁移到 `novel/03_plot/chapters/` 后，需要避免"只从 llm-wiki 读取资料"的绝对表述与新结构冲突。
- 影响页面：AGENTS.md、Claude.md、README.md、README.en.md、docs/usage-guide.md、docs/novel-agent-plan.md、llm-wiki/llm-wiki说明.md、novel/00_project/brief.md
- 处理结果：统一改为"llm-wiki 是日常设定检索和资料定位入口"；单章龙骨由 `llm-wiki/wiki/outline.md` 关联后按需读取 `novel/03_plot/chapters/`。
- 是否影响 novel/ 正文或草稿：否，当前为项目结构和规则口径调整。

## [2026-05-28] ingest | 技术栈 wiki 页面创建

- 来源：raw/出海备份【完成】/ 下 5 个原始资料文件（Web出海赚美元知识库v3/README.md、赫兹出海系列4篇）
- 影响页面：llm-wiki/wiki/world/tech-stack.md（新建）、llm-wiki/wiki/index.md（更新）
- 处理结果：从原始资料中提取前端开发栈、部署基础设施、支付变现、分析监控、AI编程工具链和建站流程，整理为结构化 wiki 页面。覆盖 Next.js+Tailwind+TypeScript 前端栈、Vercel/Cloudflare 基础设施、Stripe/AdSense/Creem 变现渠道、GA4/GSC/Hotjar 分析工具、ChatGPT/Claude/Cursor/v0.dev AI 工具链，以及从关键词研究到上线的10步建站流程。
- 是否影响 novel/ 正文或草稿：否

## [2026-05-28] ingest | AI编程工具演进时间线

- 来源：`raw/出海备份【完成】/赫兹出海【完成】/网站出海每日分享_用嘴编程一些技巧.md`、`raw/出海备份【完成】/Web出海赚美元知识库v3/README.md`
- 影响页面：`llm-wiki/wiki/world/ai-tools-timeline.md`（新建）、`llm-wiki/wiki/index.md`（更新索引）
- 处理结果：从原始资料提取"用嘴编程"Prompt技巧、E-E-A-T政策变化、工具演进节点和变现策略趋势，整合为世界观设定页面，补充小说时间线内真实的工具发布节点
- 是否影响 novel/ 正文或草稿：否，为设定参考页面

## [2026-05-28] ingest | SEO知识体系 wiki 页面创建

- 来源：raw/出海备份【完成】/哥飞出海【完成】/哥飞的文件/00-新手小白实操路径-从零开始.md、raw/出海备份【完成】/赫兹出海【完成】/ 下 6 篇赫兹出海文章（Google排名影响因素、截流、通过词根找需求、基于GSC的出词数据反向新增内页、找需求的一些方法、蹭词的新玩法）
- 影响页面：llm-wiki/wiki/world/seo-knowledge.md（新建）、llm-wiki/wiki/index.md（更新）
- 处理结果：从7个原始资料文件中提取SEO核心知识，整理为5个板块：SEO核心概念（排名机制/TDK/内容结构/内外链/Sitemap）、关键词策略（新词狙击/KGR/长尾词/蹭词/截流/GSC反向内页/词根找需求）、Google算法变化（E-E-A-T/AI内容惩罚/HCU/Core Updates）、SEO工具链、对小说的剧情价值（博弈场景/新词狙击流程/算法打击恢复路径）
- 是否影响 novel/ 正文或草稿：否

## [2026-05-28] ingest | 出海建站行业概览

- 来源：`raw/出海备份【完成】/Web出海赚美元知识库v3/README.md`、`raw/出海备份【完成】/赫兹出海【完成】/第一次赚美元_纯新手深度复盘网站出海_一文掌握全流程.md`、`raw/出海备份【完成】/赫兹出海【完成】/出海半年复盘分享_终于要月入千刀了.md`、`raw/出海备份【完成】/赫兹出海【完成】/网站出海就是一个种树的故事_浇水施肥_静待开花结果.md`
- 影响页面：`llm-wiki/wiki/world/industry-overview.md`（新建）、`llm-wiki/wiki/index.md`（更新索引）
- 处理结果：从4个原始资料中提取出海建站行业定义、核心方法论（新词新站/种树理论/数量优先/完成比完美重要）、收入模型（广告/订阅/联盟/数字产品）与真实收入曲线、2023-2025行业关键节点、出海圈社群生态（深海圈/哥飞SEO/三木/推特社区）、典型挑战（焦虑期/关键词风险/算法更新/AI惩罚）和技术栈参考，整理为结构化行业设定页面
- 是否影响 novel/ 正文或草稿：否，为设定参考页面

## [2026-05-28] ingest | 全书龙骨建立

- 来源：novel/00_project/brief.md（用户确认的小说核心设定）
- 影响页面：llm-wiki/wiki/book-spine.md（重写）
- 处理结果：根据 brief 建立完整全书龙骨，包含一句话主线、核心矛盾、前世关键事实时间线、五卷阶段表、五卷核心事件链（每卷10个关键事件）、不可违背事实（10条）、待确认事项（5条）
- 是否影响 novel/ 正文或草稿：否，为写作参考

## [2026-05-28] ingest | 人物档案建立

- 来源：novel/00_project/brief.md、llm-wiki/wiki/book-spine.md
- 影响页面：characters/lu-yuan.md、characters/zhou-shuheng.md、characters/lin-xiao.md、characters/zhao-yan.md、characters/chen-lu.md、characters/qin-yue.md、characters/he-gong.md、llm-wiki/wiki/index.md
- 处理结果：建立7个人物档案。主角含前世经历、重生优势、性格缺陷与成长弧线、能力矩阵、心理锚点、前世记忆清单。6个配角各含背景、性格、关系、剧情作用、说话风格。
- 是否影响 novel/ 正文或草稿：否，为写作参考

## [2026-05-28] ingest | 术语表建立

- 来源：raw/出海备份【完成】/下3个原始资料文件
- 影响页面：llm-wiki/wiki/world/glossary.md（新建）、llm-wiki/wiki/index.md
- 处理结果：提取55个核心术语，分为出海建站核心（9条）、SEO（18条）、技术（9条）、变现（9条）、AI编程（7条）、社群行业（3条）六大类
- 是否影响 novel/ 正文或草稿：否，为术语一致性参考

## [2026-05-28] update | 关键设定确认

- 来源：用户确认三项待定设定
- 影响页面：llm-wiki/wiki/book-spine.md、llm-wiki/wiki/characters/lu-yuan.md
- 处理结果：
  1. 前世死因确认为"过劳猝死"——连续熬夜做站，凌晨四点猝死在出租屋电脑前，屏幕还开着AdSense后台。开章基调定为疲惫、孤独、不甘。
  2. 家庭背景确认——父母在武汉经营早餐店，朴实勤劳，不知儿子被裁。母亲每周电话催就业构成外部压力线。不抢戏但有存在感。
  3. 蝴蝶效应规则确立——宏观时间线不变（工具发布/算法更新）、微观竞争格局会偏移（提前介入导致赛道更卷）、人物命运可改变、偏移随时间递增、不可逆。
  4. 主角前世记忆清单细化为7条具体关键词机会表，每条含前世情况、重生预判、可靠度评级。新增记忆时效衰减规则（五卷对应可靠度90%→0%）。
- 是否影响 novel/ 正文或草稿：否，但直接影响后续正文写作的一致性基准

## [2026-05-28] write | 第1章「凌晨四点」

- 来源：ch001-spine.md 章节龙骨
- 影响页面：novel/05_manuscript/ch001.md（新建正文）、chapters/ch001-spine.md（状态更新为"已写"）、timeline.md（新增4条事件）、character-states.md（陆远状态）、foreshadowing-ledger.md（新增4条伏笔）、book-spine.md（当前进度更新）
- 处理结果：第1章正文完成，约3000字。前世猝死→重生确认→冷静分析→出门面对被裁。基调：疲惫→震惊→清醒→复杂。四条伏笔埋设：$0.47对比、被裁邮件、出租屋、"种树别急"清单。
- 是否影响 novel/ 正文或草稿：是，第1章正文已生成

## [2026-05-28] write | 第2章「N+1」

- 来源：ch002-spine.md 章节龙骨
- 影响页面：novel/05_manuscript/ch002.md（新建正文）、chapters/ch002-spine.md（状态更新为"已写"）、timeline.md（新增4条事件）、character-states.md（陆远状态更新）、foreshadowing-ledger.md（被裁邮件推进为部分回收、新增2条伏笔）
- 处理结果：第2章正文完成，约2800字。被裁现场（8分钟签完，赵岩对比）→地铁上用ChatGPT写prompt → JSON formatter原型跑通。核心体验：前世3周的工作量，今生6小时。新增伏笔：JSON formatter站的命运、"完成比完美重要"原则。推进伏笔：被裁邮件（部分回收）、"种树别急"（主角已经急了，形成矛盾）。
- 是否影响 novel/ 正文或草稿：是，第2章正文已生成

## [2026-05-28] write | 第3章「收录」

- 来源：ch003-spine.md 章节龙骨
- 影响页面：novel/05_manuscript/ch003.md（新建正文）、chapters/ch003-spine.md（状态更新）、timeline.md（新增5条事件）、character-states.md（陆远状态更新）、foreshadowing-ledger.md（JSON formatter站推进）
- 处理结果：第3章正文完成，约2800字。买域名→Vercel部署→等收录5天→被收录→3个UV→母亲电话催就业。核心体验：AI解决了速度问题但没解决流量问题。建立第一道门槛（等收录），启动母亲压力线，结尾引出周叔衡。域名确认为jsonprettyprint.com。
- 是否影响 novel/ 正文或草稿：是，第3章正文已生成

## [2026-05-28] write | 序章「零点四七」+ 第1章重构

- 来源：用户建议增加序章
- 影响页面：novel/05_manuscript/ch000-prologue.md（新建序章正文）、novel/05_manuscript/ch001.md（重写，去掉前世死亡场景）、chapters/ch000-spine.md（新建序章龙骨）、chapters/ch001-spine.md（更新标题和核心推进）、llm-wiki/wiki/index.md（新增章节索引）
- 处理结果：序章约500字，纯前世终点画面（$0.47→猝死→黑屏）。第1章重写为"重来"，从"亮光"开始，纯粹的重生体验。结构更干净：序章=终点，第1章=起点。
- 是否影响 novel/ 正文或草稿：是，序章新建+第1章重写

## [2026-05-28] sync | 合并上游 v1.0.1 + 补充缺失内容

- 来源：上游仓库更新（AGENTS.md/Claude.md 分离、llm-wiki 三层重构、章节龙骨迁移至 novel 层）
- 影响页面：README.md、docs/novel-agent-plan.md、llm-wiki/wiki/index.md、llm-wiki/wiki/log.md、llm-wiki/wiki/characters/人物档案.md、llm-wiki/wiki/locations/地点档案.md、llm-wiki/wiki/organizations/组织档案.md、llm-wiki/wiki/rules/规则与术语档案.md、llm-wiki/wiki/outline.md、llm-wiki/wiki/book-spine.md、novel/03_plot/chapters/（章节龙骨迁移+目录更新）
- 处理结果：
  1. 合并上游 4 个提交，解决 6 个冲突，本地写作数据完整保留
  2. 章节龙骨从 llm-wiki/wiki/chapters/ 复制到 novel/03_plot/chapters/（ch000-ch003）
  3. 填充人物档案主节点：7个已建人物卡链接、2个待建档人物（母亲、父亲）
  4. 填充地点档案主节点：3个待建档地点（出租屋、原公司、地铁）
  5. 填充组织档案主节点：3个待建档组织（哥飞SEO社群、深海圈、推特/X社区）
  6. 填充规则与术语档案：4条待建档规则（蝴蝶效应、出海方法论、SEO规则、记忆衰减）
  7. 补充剧情总纲 outline.md：阶段规划、已写4章龙骨关联、下一章节组规划（ch004-ch008）、支线与节奏
  8. 更新章节龙骨目录：4章已建龙骨索引
  9. 更新 book-spine.md 当前进度：ch003已写
- 是否影响 novel/ 正文或草稿：否，为结构补充和索引同步

## [2026-05-28] write | 第4章「第一课」

- 来源：ch004-spine.md 章节龙骨
- 影响页面：novel/05_manuscript/ch004.md（新建正文）、chapters/ch004-spine.md（新建龙骨）、timeline.md（新增6条事件）、character-states.md（陆远状态更新）、foreshadowing-ledger.md（JSON formatter站推进、"种树别急"推进）、book-spine.md（当前进度更新）、outline.md（新增ch004龙骨关联）
- 处理结果：第4章正文完成，3076字。加入哥飞社群（199元/年）→阅读周叔衡《TDK先行》→首次SEO优化（重写TDK+FAQ+标题层级）→赵岩晒新工位触发嘲笑"用AI写的也叫网站？"→请求重新索引。核心体验：SEO第一课是TDK，"做出来"和"做对"之间的距离。赵岩嘲笑线正式启动，但陆远心态比前世稳。周叔衡仅通过社群帖子间接出场。
- 是否影响 novel/ 正文或草稿：是，第4章正文已生成
