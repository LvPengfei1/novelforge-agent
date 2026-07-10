# AIGC 检测与原创性质量控制

本文档只记录项目执行口径。实际独立审稿以根目录 `NOVEL_REVIEW_PROTOCOL.md` 为正本；检测方法与局限的研究背景见 `AIGC_DETECTION_PRINCIPLES.md`，后者不默认进入审稿封包。

## 定位

AIGC 文本检测中的观察维度可作为小说文本优化方向，用于减少模板化、空泛化、同质化和拼贴式文本。本项目不追求检测器分数，也不把检测结果当作事实证明。

## 执行时机

原创性与文本质量检查只在正文初稿完成后、章节完成前执行。初稿阶段先把正文写完整，不为了检查项反复中断生成。

审查使用与写作子智能体不同的全新实例。审查者接收同一版本的全书龙骨、总体大纲、本章写作包、必要的上一章结尾和待审正文，但不接收写作者的推理、自评或辩解。

## 检查重点

第一遍完整阅读，只复述人物目的、阻力、选择、代价和留下的场面。第二遍与最近三个相关章节比较，判断解法、信息传播、关系变化、情绪释放和结尾压力是否重复。第三遍才检查人物语言、叙述节奏、旁白解释、生活细节和资料拼接感。

关键词、固定词表、句长、段落长度和检测器分数不得作为正文质量分析的入口或结论。只有项目已经明确规定的禁用词、篇幅和格式才做确定性校验。任何自然度问题必须在完整阅读后落到具体场面、读感和因果。

## 处理规则

发现明显问题时，先判断问题属于故事动力、人物选择、场景因果还是语言表达。前三类问题必须重构章骨或场景，不能靠替换词语处理；语言问题才进入局部修订。修改后必须重新完整阅读，通过后再进入章后同步。

## 参考来源

- OpenAI, New AI classifier for indicating AI-written text: https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/
- Turnitin, Using the AI Writing Report: https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report
- AI-generated text detection: A comprehensive review of methods, datasets, and applications: https://www.sciencedirect.com/science/article/pii/S1574013725000693
