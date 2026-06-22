# Changelog

## Unreleased

暂无。

## 1.0.3 - 2026-06-22

### Added

- Added a writing-flow and context-isolation layer: agents now derive a temporary content execution standard from the current novel project before drafting.
- Added the story-only content context capsule to keep manuscript generation focused on plot state, character motivation, chapter conflict, required progression, ending changes, and project prose style.
- Added clean-manuscript rules: manuscript files should contain only the chapter title and prose, while change records, synchronization checks, revision reasons, and review notes belong in chapter spines, continuity files, or logs.
- Added engineering-term translation rules to prevent workflow terms such as stages, anchors, interfaces, backends, consoles, synchronization, detection, and nodes from leaking into prose unless they naturally exist in the story world.
- Added prose naturalness, project-fit, genre-derived quality checks, and reader-side retelling checks to the chapter spine template and query prompts.

### Changed

- Updated the recommended writing workflow to run project-derived content standards and context capsules before manuscript drafting.
- Clarified that quality checks must derive genre expectations from the current project brief and story state rather than applying a fixed global genre standard.
- Documented context separation between the main orchestration layer, story drafting layer, quality review layer, and continuity review layer without requiring separate agent files by default.

## 1.0.2 - 2026-05-28

### Added

- Added root-level `AIGC_DETECTION_PRINCIPLES.md` as the text-only AIGC detection principles reference.
- Added `docs/aigc-quality-control.md` to summarize common AIGC detection approaches and define originality-focused quality controls.
- Added originality and prose-quality checks to chapter completion rules, chapter spine template, and usage guide.
- Linked prose-quality review rules to `AIGC_DETECTION_PRINCIPLES.md` as the required review basis.
- Added mandatory associated-file synchronization rules for manuscript, chapter spine, character card, world setting, foreshadowing, timeline, outline, book spine, wiki page, and novel mirror updates.
- Added a staged novel workflow adapted from writing-system best practices: brief, ingestion, chapter spine, draft, edit check, revision/recheck, synchronization, and health check.
- Added evidence levels for story facts and research conclusions: established, sourced, inferred pending confirmation, and deprecated.
- Added `projects/` for local novel instances, `templates/novel-project/` for the copyable blank project skeleton, and `.gitignore` rules to keep private writing work out of framework commits.
- Added `docs/project-instance-guide.md` to explain the framework-repo versus novel-instance split.

### Changed

- Clarified that AIGC text-detection observations are used as prose optimization criteria; prose that clearly matches these features fails the quality check.
- Clarified that the prose-quality check runs after the chapter draft is complete, followed by revision and recheck before synchronization.
- Clarified that every changed file must trigger an associated-file impact check, and unchanged dependent files should be explicitly marked as checked.
- Normalized `llm-wiki` wording as the daily knowledge location entry instead of an absolute-only source, because chapter spines intentionally live in `novel/03_plot/chapters/`.
- Moved the tracked blank `raw/`, `novel/`, and `llm-wiki/` skeleton into `templates/novel-project/`; actual writing should happen in ignored `projects/<novel-slug>/` instances or outside the repository.

## 1.0.1 - 2026-05-28

### Summary

This release restructures the `llm-wiki` layer for long-form novel projects. Chapter spines and workflow templates are moved out of the final wiki graph, while reusable story knowledge is organized as linked node pages.

### Changed

- Added `llm-wiki/wiki/outline.md` as the plot outline and wiki-level overview that links to per-chapter spines.
- Moved chapter spines to `novel/03_plot/chapters/`.
- Added `llm-wiki/templates/` for reusable card templates.
- Added wiki category directories for characters, locations, organizations, rules, items, scenes, and foreshadowing.
- Reworked `llm-wiki/wiki/index.md` into a top-level index that links category master nodes instead of every concrete card.
- Replaced llm-wiki internal `README.md` nodes with Chinese semantic names to avoid duplicate README nodes in graph views.
- Added card-creation thresholds for characters, locations, organizations, rules, items, important scenes, and foreshadowing.
- Added chapter word-count acceptance rules: default about 3,000 Chinese characters, normal range 2,500-4,000 main-text characters.
- Updated `AGENTS.md`, `Claude.md`, README files, usage guide, and framework plan to match the new layout.

### Compatibility Notes

- Root-level `README.md` remains unchanged as the repository entry point.
- `raw/` and `novel/` keep their existing README files.
- Existing old paths under `llm-wiki/wiki/chapters/` and `llm-wiki/process/chapters/` are replaced by `novel/03_plot/chapters/`.
- New projects should use category master nodes under `llm-wiki/wiki/`; existing projects can migrate gradually as long as links remain clear.
