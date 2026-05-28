# NovelForge-Agent

NovelForge-Agent is a reusable agent framework for long-form novel writing. It uses `llm-wiki` as the daily knowledge entry point for story facts, settings, characters, the overall plot outline, timelines, foreshadowing, and continuity checks. Per-chapter spines live under `novel/03_plot/chapters/` and are reached through `llm-wiki/wiki/outline.md`.

This repository is not a finished novel. It is a project structure and behavior-rule set for AI-assisted fiction writing.

## Documentation

- Chinese README: [README.md](README.md)
- Chinese usage manual: [docs/usage-guide.md](docs/usage-guide.md)
- AIGC quality control notes: [docs/aigc-quality-control.md](docs/aigc-quality-control.md)
- Codex project rules: [AGENTS.md](AGENTS.md)
- Claude project rules: [Claude.md](Claude.md)
- Full framework plan: [docs/novel-agent-plan.md](docs/novel-agent-plan.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- 1.0.1 release notes: [docs/releases/v1.0.1.md](docs/releases/v1.0.1.md)

## Goals

- Treat each novel as an independent long-running project.
- Keep every important story fact in files instead of chat memory.
- Use `llm-wiki` to manage settings, characters, plot, timeline, foreshadowing, and current states.
- Maintain a plot outline and short chapter spines to connect chapter groups, stage progression, and per-chapter state changes.
- Add originality and AIGC-trace quality checks to reduce formulaic, generic, and homogenized prose.
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
│   └── usage-guide.md
├── raw
│   └── README.md
├── novel
│   ├── 00_project
│   ├── 01_world
│   ├── 02_characters
│   ├── 03_plot
│   │   └── chapters
│   ├── 04_scenes
│   ├── 05_manuscript
│   ├── 06_research
│   ├── 07_continuity
│   └── 08_archive
└── llm-wiki
    ├── llm-wiki说明.md
    ├── ingest-manifest.md
    ├── query-prompts.md
    ├── templates
    │   ├── character-card-template.md
    │   ├── location-card-template.md
    │   ├── organization-card-template.md
    │   ├── rule-card-template.md
    │   ├── item-card-template.md
    │   ├── scene-card-template.md
    │   └── foreshadowing-node-template.md
    ├── logs
    ├── sources
    └── wiki
        ├── book-spine.md
        ├── timeline.md
        ├── character-states.md
        ├── relationship-states.md
        ├── foreshadowing-ledger.md
        ├── contradiction-flags.md
        ├── outline.md
        ├── index.md
        ├── log.md
        ├── characters
        ├── locations
        ├── organizations
        ├── rules
        ├── items
        ├── scenes
        └── foreshadowing
```

## Three-Layer Model

### `raw/`

Original source layer. Store user-provided materials, clipped web pages, reference articles, images, and imported notes here. This layer is read-only.

### `novel/`

Novel engineering layer. Store manuscript drafts, finished chapters, chapter spines, writing process files, and backups here. It is not the daily source for story-setting lookup; chapter spines are read when the wiki outline points to them.

### `llm-wiki/`

Knowledge and setting layer. Store AI-maintained wiki pages, indexes, logs, query notes, continuity ledgers, and contradiction checks here. Normal writing, querying, reviewing, and continuity work should start from this layer.

`llm-wiki/wiki/` stores final graph nodes. `llm-wiki/wiki/outline.md` stores the plot outline that connects chapter groups and stage progression. `novel/03_plot/chapters/` stores per-chapter spines.

## Chapter Spine Workflow

Every chapter should have a chapter spine under `novel/03_plot/chapters/`, for example:

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

A chapter is not considered complete until the manuscript, plot outline, chapter spine, continuity ledgers, and related `llm-wiki` pages are synchronized.

Default chapter length is about 3,000 Chinese characters. A normal chapter should not be below 2,500 or above 4,000 main-text characters unless the exception is recorded in the chapter spine and log.

`llm-wiki` should be maintained as a linked knowledge base: manuscript text does not enter the wiki, but reusable characters, locations, organizations, rules, items, important scenes, foreshadowing, timelines, relationships, and states should become wiki nodes when they reach the card-creation threshold.

## Recommended Workflow

1. Put original materials into `raw/`.
2. Ingest long-term story facts into `llm-wiki/`.
3. Before writing, read `llm-wiki/wiki/index.md`, `book-spine.md`, `llm-wiki/wiki/outline.md`, the current chapter spine, and related character, timeline, and foreshadowing pages.
4. Write the manuscript in `novel/05_manuscript/`.
5. After writing, update the chapter spine, plot outline, book spine, timeline, character states, relationship states, foreshadowing ledger, contradiction flags, index, and log.
6. Run a node-gap check: reusable characters, locations, organizations, rules, items, important scenes, and foreshadowing should not remain only in index summaries or templates.

## Agent Rule Files

- Use `AGENTS.md` with Codex or other agents that read AGENTS rules.
- Use `Claude.md` with Claude-based workflows.
- Keep both files semantically synchronized. They define the same project behavior rules, with file names adapted for each agent.

## License

This project is released under the Apache License 2.0.

If you modify and distribute this project, you must clearly state that changes were made and describe the major changes. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
