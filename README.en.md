# NovelForge-Agent

NovelForge-Agent is a reusable agent framework for long-form novel writing. It uses `llm-wiki` as the daily knowledge entry point for story facts, settings, characters, timelines, foreshadowing, and continuity checks.

This repository is not a finished novel. It is a project structure and behavior-rule set for AI-assisted fiction writing.

## Documentation

- Chinese README: [README.md](README.md)
- Chinese usage manual: [docs/usage-guide.md](docs/usage-guide.md)
- Codex project rules: [AGENTS.md](AGENTS.md)
- Claude project rules: [Claude.md](Claude.md)
- Full framework plan: [docs/novel-agent-plan.md](docs/novel-agent-plan.md)

## Goals

- Treat each novel as an independent long-running project.
- Keep every important story fact in files instead of chat memory.
- Use `llm-wiki` to manage settings, characters, plot, timeline, foreshadowing, and current states.
- Maintain a short chapter spine for every chapter to prevent long-range continuity drift.
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
│   ├── 04_scenes
│   ├── 05_manuscript
│   ├── 06_research
│   ├── 07_continuity
│   └── 08_archive
└── llm-wiki
    ├── README.md
    ├── ingest-manifest.md
    ├── query-prompts.md
    ├── logs
    ├── sources
    └── wiki
        ├── book-spine.md
        ├── timeline.md
        ├── character-states.md
        ├── relationship-states.md
        ├── foreshadowing-ledger.md
        ├── contradiction-flags.md
        ├── index.md
        ├── log.md
        └── chapters
            └── _chapter-spine-template.md
```

## Three-Layer Model

### `raw/`

Original source layer. Store user-provided materials, clipped web pages, reference articles, images, and imported notes here. This layer is read-only.

### `novel/`

Novel engineering layer. Store manuscript drafts, finished chapters, writing process files, and backups here. It is not the daily source for story-setting lookup.

### `llm-wiki/`

Knowledge and setting layer. Store AI-maintained wiki pages, indexes, logs, query notes, continuity ledgers, and contradiction checks here. Normal writing, querying, reviewing, and continuity work should start from this layer.

## Chapter Spine Workflow

Every chapter should have a chapter spine under `llm-wiki/wiki/chapters/`, for example:

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

A chapter is not considered complete until the manuscript and the related `llm-wiki` pages are synchronized.

## Recommended Workflow

1. Put original materials into `raw/`.
2. Ingest long-term story facts into `llm-wiki/`.
3. Before writing, read `llm-wiki/wiki/index.md`, `book-spine.md`, the current chapter spine, and related character, timeline, and foreshadowing pages.
4. Write the manuscript in `novel/05_manuscript/`.
5. After writing, update the chapter spine, book spine, timeline, character states, relationship states, foreshadowing ledger, contradiction flags, index, and log.

## Agent Rule Files

- Use `AGENTS.md` with Codex or other agents that read AGENTS rules.
- Use `Claude.md` with Claude-based workflows.
- Keep both files synchronized. They define the same project behavior rules.

## License

This project is released under the Apache License 2.0.

If you modify and distribute this project, you must clearly state that changes were made and describe the major changes. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
