# 本地小说实例目录

`projects/` 用于存放本机实际创作的小说项目实例，默认不提交到 Git。

推荐做法：

1. 从 `templates/novel-project/` 复制一份到 `projects/<novel-slug>/`。
2. 将根目录的 `AGENTS.md`、`Claude.md` 和 `AIGC_DETECTION_PRINCIPLES.md` 复制到该实例目录。
3. 在实例目录中写正文、维护设定和运行 llm-wiki。
4. 框架优化仍在仓库根目录提交；小说正文和私有设定不会进入 Git。

如果希望某本小说单独版本管理，请在 `projects/<novel-slug>/` 内另行初始化独立 Git 仓库，或把该小说放到仓库外部目录。
