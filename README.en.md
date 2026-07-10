# NovelForge-Agent

NovelForge-Agent is a reusable agent framework for long-form novel writing. It uses `llm-wiki` as the daily knowledge entry point for story facts, settings, characters, the overall plot outline, timelines, foreshadowing, and continuity checks. Per-chapter spines live under `novel/03_plot/chapters/` and are reached through `llm-wiki/wiki/outline.md`.

This repository is not a finished novel. It provides a reusable project structure, agent rules, and deterministic chapter-packet tooling. The code does not judge whether a story works; it rejects unapproved or modified canon, validates project-bound input paths, supplies only explicitly declared packet sources, and separates writer and reviewer packets.

An input allowlist is not an operating-system sandbox. External commands launched through `invoke` retain whatever filesystem and network access the host grants them. Use a container or restricted workspace when hard isolation is required; NovelForge guarantees only the inputs it assembles and records.

Real novels should live under `projects/<novel-slug>/` or outside this repository. The repository root is for framework rules, documentation, and empty templates, so manuscript work does not pollute framework commits.

## Documentation

- Chinese README: [README.md](README.md)
- AIGC text detection principles: [AIGC_DETECTION_PRINCIPLES.md](AIGC_DETECTION_PRINCIPLES.md)
- Default independent review protocol: [NOVEL_REVIEW_PROTOCOL.md](NOVEL_REVIEW_PROTOCOL.md)
- Chinese usage manual: [docs/usage-guide.md](docs/usage-guide.md)
- Project instance guide: [docs/project-instance-guide.md](docs/project-instance-guide.md)
- AIGC quality control notes: [docs/aigc-quality-control.md](docs/aigc-quality-control.md)
- Codex agent principles: [AGENTS.md](AGENTS.md)
- Codex skill entry point: [SKILL.md](SKILL.md)
- Claude agent principles: [Claude.md](Claude.md)
- Full framework plan: [docs/novel-agent-plan.md](docs/novel-agent-plan.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- 1.0.3 release notes: [docs/releases/v1.0.3.md](docs/releases/v1.0.3.md)

## Goals

- Treat each novel as an independent long-running project.
- Keep every important story fact in files instead of chat memory.
- Use `llm-wiki` to manage settings, characters, plot, timeline, foreshadowing, and current states.
- Maintain a plot outline and short chapter spines to connect chapter groups, stage progression, and per-chapter state changes.
- Use an approval-gated workflow: architecture approval -> chapter input allowlist -> fresh writer -> fresh reviewer -> orchestration and minimal integration -> synchronization.
- Label story facts and research conclusions with evidence levels so AI inferences are not treated as established facts.
- Start every new chapter with a fresh writing agent that does not inherit the parent conversation. It receives the approved project brief, book spine, overall outline, prose-style canon, chapter-specific context, and only the necessary ending of the previous chapter.
- After the draft is complete, use a different fresh reviewer for whole-chapter reading, recent-chapter structural comparison, and prose review under `NOVEL_REVIEW_PROTOCOL.md`.
- Keep raw sources, manuscripts, and searchable knowledge pages separated.
- Give AI agents stable principles for drafting, rewriting, reviewing, and maintaining story knowledge; concrete fields, checklists, and example constraints live in the current templates and novel instance.

## Project Structure

```text
.
├── AGENTS.md
├── Claude.md
├── SKILL.md
├── NOVEL_REVIEW_PROTOCOL.md
├── agents
├── README.md
├── README.en.md
├── NOTICE
├── LICENSE
├── docs
│   ├── novel-agent-plan.md
│   ├── project-instance-guide.md
│   └── usage-guide.md
├── novelforge_agent
├── scripts
│   └── novelforge.py
├── tests
├── templates
│   └── novel-project
│       ├── raw
│       ├── novel
│       └── llm-wiki
└── projects
    └── README.md
```

`templates/novel-project/` is the blank project template. `projects/` is for local novel instances and is ignored by Git by default.

## Create a Novel Instance

The recommended command is:

```powershell
python scripts/novelforge.py init projects/<novel-slug>
```

It copies the blank template plus `AGENTS.md`, `Claude.md`, `AIGC_DETECTION_PRINCIPLES.md`, and `NOVEL_REVIEW_PROTOCOL.md`, and refuses to overwrite a non-empty target. The same setup can still be performed manually.

`approve` validates the brief's story engine, the book spine's long-running engine, at least one complete outline stage, and the prose-style baseline before recording hashes for all four canon files.

Write the novel inside `projects/<novel-slug>/`. Framework improvements should still be committed from the repository root.

## Three-Layer Model

The following paths are relative to a copied novel instance.

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

A chapter is not considered complete until the manuscript, plot outline, chapter spine, continuity ledgers, associated-file synchronization check, and related `llm-wiki` pages are synchronized.

If the current novel instance, user request, or target platform defines a chapter-length policy, record and verify it in the chapter spine and log. Without an explicit policy, the framework should not impose a global fixed word-count range.

`llm-wiki` should be maintained as a linked knowledge base: manuscript text does not enter the wiki, but reusable characters, locations, organizations, rules, items, important scenes, foreshadowing, timelines, relationships, and states should become wiki nodes when they reach the card-creation threshold.

## Recommended Workflow

1. Put original materials into `raw/`.
2. Ingest long-term story facts into `llm-wiki/`.
3. Confirm that the project brief, book spine, and overall outline belong to the same approved architecture version; otherwise stop formal drafting.
4. After explicit user approval, run `approve` to bind the evidence, version, and hashes of all four canon files.
5. Create chapter-specific spine and job files with explicit sources, an exact previous-chapter excerpt, and at most three reviewer-only comparison files.
6. Run `python scripts/novelforge.py prepare <project> --job <job>` to validate and create `writer-task.md`.
7. Start a fresh writer without parent-conversation inheritance and give it only that task.
8. After the draft exists, run `prepare-review` and start a different fresh reviewer with `reviewer-task.md`.
9. Let the orchestrator perform minimal integration, then synchronize affected story pages, continuity ledgers, indexes, and logs.

## Command-Line Tool

```powershell
python scripts/novelforge.py approve projects/<novel-slug> --confirmation "user approval evidence"
python scripts/novelforge.py validate projects/<novel-slug>
python scripts/novelforge.py prepare projects/<novel-slug> --job novel/03_plot/chapters/ch001-job.json
python scripts/novelforge.py prepare-review projects/<novel-slug> --run <run-directory>
```

The manifest records every permitted source, role, optional line range, and SHA-256 hash. Each `invoke` re-derives the expected sources and task from the currently approved job, rejecting forged or stale packets. Review preparation also locks the draft hash, so any later manuscript change invalidates that review packet.

`invoke` accepts direct executables only, rejects `.cmd`, `.bat`, and common command interpreters, and starts writer and reviewer processes separately with `shell=False`. It is still not a filesystem or network sandbox.

## Agent Rule Files

- Use `AGENTS.md` with Codex or other agents that read AGENTS rules.
- Use `Claude.md` with Claude-based workflows.
- Keep both files semantically synchronized. They define the same agent behavior principles, with file names adapted for each agent.

## License

This project is released under the Apache License 2.0.

If you modify and distribute this project, you must clearly state that changes were made and describe the major changes. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
