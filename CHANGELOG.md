# Changelog

## Unreleased

### Added

- Added `docs/aigc-quality-control.md` to summarize common AIGC detection approaches and define originality-focused quality controls.
- Added originality and AIGC-trace quality checks to chapter completion rules, chapter spine template, and usage guide.

### Changed

- Clarified that AIGC-related rules are for reducing formulaic, generic, and homogenized prose, not for bypassing or deceiving detection tools.

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
