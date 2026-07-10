# 框架仓库与小说实例分离

NovelForge-Agent 仓库只维护智能体规则、文档和空项目模板。真实小说项目应作为独立实例运行，避免正文、设定和私有资料污染框架仓库提交。

## 推荐结构

```text
novelforge-agent/
├── AGENTS.md
├── Claude.md
├── docs/
├── templates/
│   └── novel-project/
│       ├── raw/
│       ├── novel/
│       └── llm-wiki/
└── projects/
    └── <novel-slug>/   # 本地实例，默认被 Git 忽略
```

## 新建小说实例

推荐在框架仓库运行：

```powershell
python scripts/novelforge.py init projects/<novel-slug>
```

该命令将 `templates/novel-project/` 复制为目标实例，并把根目录的 `AGENTS.md`、`Claude.md`、`AIGC_DETECTION_PRINCIPLES.md`、`NOVEL_REVIEW_PROTOCOL.md` 放入实例根目录。目标目录非空时会停止，不覆盖已有小说。也可以手工完成同样的复制。

之后在 `projects/<novel-slug>/` 中创作正文、维护设定和运行 llm-wiki。

实例中的 `novelforge.json` 声明四份全局正本、审稿原则和禁止进入章节封包的路径；`architecture-approval.json` 绑定用户确认依据、架构版本和批准时的正本哈希；`.novelforge/` 保存按章生成的临时封包和来源哈希，默认不提交。小说实例需要独立版本管理时，可调整自身 `.gitignore`，但不得把运行封包当作故事正本。

## 提交规则

- 框架优化：提交仓库根目录的 `AGENTS.md`、`Claude.md`、`docs/`、`templates/`、`README` 等文件。
- 小说创作：默认留在 `projects/<novel-slug>/`，不随框架提交。
- 模板优化：只修改 `templates/novel-project/` 中的空模板和说明，不写入具体小说正文或私有设定。

如果某本小说也需要版本管理，应在小说实例目录内初始化独立 Git 仓库，或放到仓库外独立管理。
