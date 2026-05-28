# llm-wiki 输出目录

本目录用于保存 LLM 生成或导出的 wiki 页面。

这些页面用于检索、交叉引用和矛盾检查。长期使用的设定、人物、主线、时间线、伏笔和状态都应维护在本目录；剧情总纲和章节龙骨属于流程层，维护在 `llm-wiki/process/`；模板维护在 `llm-wiki/templates/`；`novel/` 只保存正文草稿、章节成稿和写作过程文件。

核心文件：

- `index.md`：内容索引。
- `log.md`：时间日志。
- `book-spine.md`：全书龙骨。
- `timeline.md`：时间线。
- `character-states.md`：人物状态账本。
- `relationship-states.md`：关系状态账本。
- `foreshadowing-ledger.md`：伏笔账本。
- `contradiction-flags.md`：矛盾标记。
- `characters/`：人物卡。
- `locations/`：地点卡。
- `organizations/`：组织和势力卡。
- `rules/`：规则、术语和体系设定。
- `items/`：重要物品、证据、账册和道具。
- `scenes/`：重要场景卡。
- `foreshadowing/`：独立伏笔节点页。

分类主节点：

- `characters/人物档案.md`
- `locations/地点档案.md`
- `organizations/组织档案.md`
- `rules/规则与术语档案.md`
- `items/物品档案.md`
- `scenes/场景档案.md`
- `foreshadowing/伏笔与连续性档案.md`

页面命名建议：

- 人物：`characters/姓名.md` 或 `character-姓名.md`
- 地点：`locations/名称.md` 或 `location-名称.md`
- 组织：`organizations/名称.md` 或 `organization-名称.md`
- 规则：`rules/名称.md` 或 `rule-名称.md`
- 物品：`items/名称.md` 或 `item-名称.md`
- 场景：`scenes/场景名.md` 或 `scene-场景名.md`
- 伏笔：`foreshadowing/名称.md` 或 `foreshadow-名称.md`
- 来源：`source-标题.md`

总表不能替代节点页。达到复用门槛的人物、地点、组织、规则、物品、重要场景和伏笔，必须建立独立页面，并写入对应分类主节点；`index.md` 只关联分类主节点，不直接关联每一张具体卡。剧情总纲、章节龙骨和模板不写入 `index.md`，避免最终图谱被流程文件污染。
