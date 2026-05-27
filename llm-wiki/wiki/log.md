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
- 影响页面：AGENTS.md、docs/novel-agent-plan.md、llm-wiki/README.md、llm-wiki/wiki/index.md、llm-wiki/wiki/log.md
- 处理结果：建立三层资料模型和 wiki 运维规则
- 是否影响 novel/ 正文或草稿：否，当前为项目架构规则

## [2026-05-27] update | 章节龙骨机制

- 来源：用户确认每章需要简短大纲龙骨，防止长篇前后期矛盾
- 影响页面：AGENTS.md、docs/novel-agent-plan.md、llm-wiki/README.md、llm-wiki/wiki/index.md、llm-wiki/wiki/book-spine.md、llm-wiki/wiki/chapters/_chapter-spine-template.md、llm-wiki/wiki/timeline.md、llm-wiki/wiki/character-states.md、llm-wiki/wiki/relationship-states.md、llm-wiki/wiki/foreshadowing-ledger.md、llm-wiki/wiki/contradiction-flags.md
- 处理结果：建立全书龙骨、章节龙骨模板和章后连续性账本；规定章节完成必须同步龙骨、时间线、人物状态、关系、伏笔和矛盾标记
- 是否影响 novel/ 正文或草稿：否，当前为项目管理规则和 llm-wiki 模板
