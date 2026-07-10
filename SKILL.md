---
name: novelforge-writing
description: Manage, draft, review, and maintain long-form novel projects with NovelForge-Agent. Use when Codex needs to initialize a NovelForge project, approve or revise story architecture, prepare a chapter input allowlist, launch a fresh isolated writer and reviewer for each chapter, check continuity, or synchronize chapter facts back into the novel wiki.
---

# NovelForge Writing

Treat the approved files in the novel instance as canon. Do not use the parent conversation, memory, archived drafts, rejected plans, or repository-wide search as substitutes for current project evidence.

## Prepare The Project

1. Locate the novel instance containing `novelforge.json`, `novel/`, and `llm-wiki/`.
2. For a new project, run `python scripts/novelforge.py init <target>` and fill the generated canon before drafting.
3. After explicit user approval, run `python scripts/novelforge.py approve <project> --confirmation <evidence>` to validate the substantive canon and bind that approval to the current four files. Never infer or manufacture approval.
4. Run `python scripts/novelforge.py validate <project>` from this skill directory.
5. Stop formal drafting when validation reports an unapproved or modified architecture, inconsistent versions, missing story engine, incomplete outline, or unavailable style canon. Continue only with proposal work until the user approves and the canon files are updated.

## Prepare A Chapter

1. Copy `_chapter-spine-template.md` and `_chapter-job-template.json` to chapter-specific files.
2. Put only directly relevant project-relative paths in `chapter_sources`. Put at most three explicit comparison files in `recent_chapters`; these are reviewer-only.
3. Specify the exact previous-chapter line range when a handoff excerpt is needed.
4. Run `python scripts/novelforge.py prepare <project> --job <job>`.
5. Use the generated `writer-task.md` as the writer's complete input. Do not append chat history, process notes, quality reports, logs, or unlisted files.

## Draft In A Fresh Agent

Launch a new writing subagent with parent-context inheritance disabled. When the host exposes `fork_context`, set it to `false`. Pass the text of `writer-task.md`, not a request to search the project. The writer may produce only the chapter draft or a `NOVELFORGE_MISSING_CONTEXT:` report.

Do not reuse a writer between chapters. Do not give the writer review checklists or the previous writer's reasoning. The main agent may save the returned draft to the configured path, or invoke a stateless external command with:

```text
python scripts/novelforge.py invoke <project> --run <run-dir> --stage writer -- <command>
```

`invoke` accepts a direct executable, rejects batch files and command interpreters, and starts a new process without a shell. It is not a filesystem or network sandbox; use a restricted host environment when hard isolation is required.

## Review Independently

1. Run `python scripts/novelforge.py prepare-review <project> --run <run-dir>` after a draft exists.
2. Launch a different fresh subagent with parent-context inheritance disabled and pass only `reviewer-task.md`.
3. Require whole-chapter reading first, recent-chapter structural comparison second, and language diagnosis last. Reject conclusions based only on keyword hits, phrase counts, detector scores, or the writer's stated intention.
4. Save the review separately from the manuscript. A stateless external reviewer can be invoked with `--stage reviewer`.

## Integrate And Synchronize

Use review findings tied to specific scenes and reader effects. Rebuild scene purpose, resistance, choice, cost, information route, or consequence when the story layer fails; do not disguise structural failure with synonym replacement.

After approval, make only the necessary manuscript edits and update the chapter spine, outline, book spine, timeline, character and relationship states, foreshadowing, contradiction flags, affected wiki nodes, and log. Keep the manuscript limited to its title and prose.

Run `python -m unittest discover -s tests -v` when changing this skill or its packet builder.
