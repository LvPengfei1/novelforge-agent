# AIGC 检测与原创性质量控制

本文档只记录项目执行口径。检测原理以根目录 `AIGC_DETECTION_PRINCIPLES.md` 为准。

## 定位

AIGC 文本检测中的观察维度可作为小说文本优化方向，用于减少模板化、空泛化、同质化和拼贴式文本。本项目不追求检测器分数，也不把检测结果当作事实证明。

## 执行时机

原创性与文本质量检查只在正文初稿完成后、章节完成前执行。初稿阶段先把正文写完整，不为了检查项反复中断生成。

## 检查重点

- 是否从章节龙骨、人物状态、场景冲突和伏笔出发写正文。
- 人物对白、内心独白和叙述表达是否符合身份、经历、关系和当前情绪。
- 场景是否有动作、物件、空间、感官、选择、代价和后果。
- 段落、句式、连接词和推进方式是否机械重复。
- 是否存在抽象套话、过度总结、主题直白说教。
- 参考资料是否已转化为小说场景逻辑，是否存在拼贴或同义词替换式改写。
- 是否能从章节龙骨、正文版本、修改原因、来源记录和同步日志追溯创作过程。

## 处理规则

发现明显问题时，先列出位置和影响，再按人物、场景、节奏、细节密度和创作依据修改正文。修改后必须复查；复查通过后再进入章后同步。

## 参考来源

- OpenAI, New AI classifier for indicating AI-written text: https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/
- Turnitin, Using the AI Writing Report: https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report
- AI-generated text detection: A comprehensive review of methods, datasets, and applications: https://www.sciencedirect.com/science/article/pii/S1574013725000693
