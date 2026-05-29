# NovelForge-Agent

NovelForge-Agent is a reusable agent framework for long-form novel writing. It uses `llm-wiki` as the daily knowledge entry point for story facts, settings, characters, the overall plot outline, timelines, foreshadowing, and continuity checks. Per-chapter spines live under `小说工程/03_剧情/章节/` and are reached through `llm-wiki/wiki/outline.md`.

This repository is not a finished novel. It is a project structure and behavior-rule set for AI-assisted fiction writing.

Real novels should live under `作品/<novel-slug>/` or outside this repository. The repository root is for framework rules, documentation, and empty templates, so manuscript work does not pollute framework commits.

## Documentation

- Chinese README: [README.md](README.md)
- AIGC text detection principles: [AIGC_DETECTION_PRINCIPLES.md](AIGC_DETECTION_PRINCIPLES.md)
- Chinese usage manual: [docs/usage-guide.md](docs/usage-guide.md)
- Project instance guide: [docs/project-instance-guide.md](docs/project-instance-guide.md)
- AIGC quality control notes: [docs/aigc-quality-control.md](docs/aigc-quality-control.md)
- Codex project rules: [AGENTS.md](AGENTS.md)
- Claude project rules: [Claude.md](Claude.md)
- Full framework plan: [docs/novel-agent-plan.md](docs/novel-agent-plan.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- 1.0.2 release notes: [docs/releases/v1.0.2.md](docs/releases/v1.0.2.md)

## Goals

- Treat each novel as an independent long-running project.
- Keep every important story fact in files instead of chat memory.
- Use `llm-wiki` to manage settings, characters, plot, timeline, foreshadowing, and current states.
- Maintain a plot outline and short chapter spines to connect chapter groups, stage progression, and per-chapter state changes.
- Use a staged workflow: project brief -> ingestion -> chapter spine -> draft -> edit check -> revision and recheck -> synchronization -> health check.
- Label story facts and research conclusions with evidence levels so AI inferences are not treated as established facts.
- After the chapter draft is complete, use `AIGC_DETECTION_PRINCIPLES.md` for originality and prose-quality checks; failed drafts must be revised and rechecked before synchronization.
- Keep raw sources, manuscripts, and searchable knowledge pages separated.
- Give AI agents stable rules for drafting, rewriting, reviewing, and maintaining story knowledge.

## Project Structure

```text
.
├── AGENTS.md
├── Claude.md
├── README.md
├── README.en.md
├── NOTICE
├── LICENSE
├── docs
│   ├── novel-agent-plan.md
│   ├── project-instance-guide.md
│   └── usage-guide.md
├── 模板
│   └── 小说项目
│       ├── 原始资料
│       ├── 小说工程
│       └── llm-wiki
└── 作品
    └── README.md
```

`模板/小说项目/` is the blank project template. `作品/` is for local novel instances and is ignored by Git by default.

## Create a Novel Instance

Copy `模板/小说项目/` to `作品/<novel-slug>/`, then place root-level `AGENTS.md`, `Claude.md`, and `AIGC_DETECTION_PRINCIPLES.md` in that novel instance root.

Write the novel inside `作品/<novel-slug>/`. Framework improvements should still be committed from the repository root.

## Three-Layer Model

The following paths are relative to a copied novel instance.

### `原始资料/`

Original source layer. Store user-provided materials, clipped web pages, reference articles, images, and imported notes here. This layer is read-only.

### `小说工程/`

Novel engineering layer. Store manuscript drafts, finished chapters, chapter spines, writing process files, and backups here. It is not the daily source for story-setting lookup; chapter spines are read when the wiki outline points to them.

### `llm-wiki/`

Knowledge and setting layer. Store AI-maintained wiki pages, indexes, logs, query notes, continuity ledgers, and contradiction checks here. Normal writing, querying, reviewing, and continuity work should start from this layer.

`llm-wiki/wiki/` stores final graph nodes. `llm-wiki/wiki/outline.md` stores the plot outline that connects chapter groups and stage progression. `小说工程/03_剧情/章节/` stores per-chapter spines.

## Chapter Spine Workflow

Every chapter should have a chapter spine under `小说工程/03_剧情/章节/`, for example:

```text
ch001-spine.md
ch002-spine.md
ch003-spine.md
```

A chapter spine records only the high-density facts needed for continuity:

- chapter function
- opening state
- chapter objective
- core progression
- ending changes
- future constraints
- unresolved items

A chapter is not considered complete until the manuscript, plot outline, chapter spine, continuity ledgers, associated-file synchronization check, and related `llm-wiki` pages are synchronized.

Default chapter length is about 3,000 Chinese characters. A normal chapter should not be below 2,500 or above 4,000 main-text characters unless the exception is recorded in the chapter spine and log.

`llm-wiki` should be maintained as a linked knowledge base: manuscript text does not enter the wiki, but reusable characters, locations, organizations, rules, items, important scenes, foreshadowing, timelines, relationships, and states should become wiki nodes when they reach the card-creation threshold.

## Recommended Workflow

1. Put original materials into `原始资料/`.
2. Ingest long-term story facts into `llm-wiki/`.
3. Before writing, read `llm-wiki/wiki/index.md`, `book-spine.md`, `llm-wiki/wiki/outline.md`, the current chapter spine, and related character, timeline, and foreshadowing pages.
4. Write the manuscript in `小说工程/05_正文/`.
5. After writing, use the chapter-spine checklist for prose-quality review, associated-file synchronization, node-gap checks, and logging.

## Agent Rule Files

- Use `AGENTS.md` with Codex or other agents that read AGENTS rules.
- Use `Claude.md` with Claude-based workflows.
- Keep both files semantically synchronized. They define the same project behavior rules, with file names adapted for each agent.

## License

This project is released under the Apache License 2.0.

If you modify and distribute this project, you must clearly state that changes were made and describe the major changes. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
