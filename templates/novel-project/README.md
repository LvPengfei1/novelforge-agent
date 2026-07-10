# 小说项目实例模板

这是单本小说项目的空骨架。复制到 `projects/<novel-slug>/` 或仓库外部目录后再开始创作。

目录职责：

- `raw/`：原始资料，只读，不改写。
- `novel/`：正文、草稿、章节龙骨和写作过程文件。
- `llm-wiki/`：设定知识库、索引、日志、连续性账本和矛盾检查。

建议将仓库根目录的 `AGENTS.md`、`Claude.md`、`AIGC_DETECTION_PRINCIPLES.md` 和 `NOVEL_REVIEW_PROTOCOL.md` 一并复制到实例根目录，确保小说实例脱离框架仓库后仍有完整规则与审稿正本。

`novelforge.json` 定义机器可读的全局正本和禁读路径。用户明确批准当前架构后，由框架的 `approve` 命令把批准依据、架构版本和四份正本哈希写入 `architecture-approval.json`；正本变化后必须重新确认。每章将 `_chapter-job-template.json` 复制为 `chXXX-job.json`，只列入本章明确需要的资料，再由框架仓库的 `scripts/novelforge.py` 校验和封包。`.novelforge/` 保存临时运行记录，默认不进入小说实例的 Git。
