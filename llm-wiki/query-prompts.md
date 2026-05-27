# llm-wiki 常用查询提示

## 写作前查询

```text
请根据当前 llm-wiki，生成【章节编号】的章节龙骨草案。必须包含章节功能、开章状态、本章目标、核心推进、结尾变化、后续约束和待回收问题。不要写正文。
```

```text
请根据当前 wiki，汇总与【章节/场景名称】相关的人物、地点、组织、规则、伏笔和未解决冲突。只列已确立事实，并标出 wiki 缺失、矛盾或需要证据回查的条目。
```

```text
请查询【人物名】的当前状态、核心动机、关系变化、已发生关键事件和禁止违背的写法。
```

```text
请查询【地点名】的功能、氛围、相关人物、已发生事件和当前限制。
```

## 连续性检查

```text
请检查【章节编号】的章节龙骨是否与 book-spine、timeline、character-states、relationship-states、foreshadowing-ledger 和 contradiction-flags 一致。列出矛盾、缺失同步项和建议修正。
```

```text
请检查【章节/场景名称】涉及的人物状态、时间线、地点、道具、信息差和伏笔是否存在矛盾。输出冲突条目、相关 wiki 页面、可能需要回查的 raw/novel 位置和建议处理方式。
```

```text
请列出当前所有未回收伏笔，按与【当前章节】的相关度排序，并说明哪些不能提前揭示。
```

## 摄入后审查

```text
请根据【章节正文或摘要】更新对应章节龙骨，并列出需要同步到 book-spine、timeline、character-states、relationship-states、foreshadowing-ledger、contradiction-flags 和 index 的项目。
```

```text
请列出本次摄入后新增或更新的 wiki 页面，并标注可能与旧设定冲突的条目。
```

```text
请找出同名、近义或可能重复的人物、地点、组织、规则、物品页面，给出合并建议，但不要直接合并。
```
