from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from novelforge_agent.core import (
    NovelForgeError,
    ValidationFailure,
    approve_project,
    init_project,
    invoke_stage,
    prepare_project,
    prepare_review,
    validate_project,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


BRIEF = """# 项目简报

## 架构状态

- 架构版本：v1
- 当前状态：已批准
- 当前是否允许生成正式正文：是

## 故事承诺与长线动力

- 读者持续追读所期待的核心体验：承诺标记
- 主角真正想得到什么：欲望标记
- 主角的欲望会怎样持续制造麻烦：麻烦标记
- 外部主线怎样迫使主角不能退出：外部动力标记
- 主要关系怎样改变主线，而不是装饰主线：关系标记
- 当前阶段结束时必须发生的不可逆变化：不可逆标记
"""

BOOK_SPINE = """# 全书龙骨

## 架构权限

- 架构版本：v1
- 批准状态：已批准
- 当前是否可供章节写作子智能体使用：是

## 读者承诺与人物发动机

- 读者持续期待的核心体验：追读承诺
- 主角核心欲望：核心欲望
- 主角欲望或缺点怎样制造下一轮麻烦：持续麻烦
- 主要关系怎样改变主线：关系改变主线
- 长线动力为何不会在数章后耗尽：长线动力

## 核心矛盾

- 最终必须回答的问题：最终问题

BOOK_CANON_MARKER
"""

OUTLINE = """# 剧情总纲

## 架构权限

- 对应架构版本：v1
- 批准状态：已批准
- 当前是否可供章节写作子智能体使用：是
- 与全书龙骨的版本是否一致：是

## 阶段规划

| 范围 | 人物在追求什么 | 阶段阻力 | 必须作出的选择与代价 | 不可逆结果 | 状态 |
| --- | --- | --- | --- | --- | --- |
| ch001-ch010 | 找到真相 | 对手阻挡 | 放弃退路 | 身份暴露 | 已批准 |

OUTLINE_CANON_MARKER
"""

STYLE_CANON = """# 文风正本

## 使用权限

- 对应架构版本：v1
- 批准状态：已批准
- 当前是否可供章节写作子智能体使用：是

## 叙事基准

- 叙事视角与距离：有限视角，贴近当场感知
- 叙述者态度：克制但有判断
- 句段节奏：随场景压力变化

## 人物表达

- 对话的身份差异：由身份、利益和关系决定

## 项目边界

- 必须保留的阅读感：人物正在现场做选择
- 容易写偏的方向：替人物解释和替读者总结

STYLE_CANON_MARKER
"""

CHAPTER_SPINE = """# ch001 章节龙骨

## 基本信息

- 章节编号：ch001

## 章节功能

SPINE_FUNCTION_MARKER

## 开章状态

SPINE_OPENING_MARKER

## 本章目标

- 剧情目标：推动当前冲突
- 人物目标：争取眼前利益

SPINE_GOAL_MARKER

## 架构与近章闸门

- 当前架构版本：v1
- 架构是否已经得到用户确认：是
- 当前故事承诺：让人物欲望持续制造后果
- 所属阶段及阶段终点：第一阶段，身份暴露
- 本章必须造成的选择、代价或状态变化：主角选择冒险并失去退路
- 本章与近章不同的场景动力：第一章，无近章复用
- 写作闸门：通过

SPINE_GATE_MARKER

## 写作输入白名单

UNSELECTED_ALLOWLIST_BOILERPLATE

## 内容执行标准

- 本章阅读感：紧张中带人物偏心

SPINE_STANDARD_MARKER

## 章节写作包

- 本章开场状态：主角刚抵达现场
- 人物动机：主角想保住眼前利益
- 本章核心冲突：主角必须在暴露和退让之间选择
- 本章必须推进：主角作出不可撤回的选择
- 本章结尾变化预期：退路被切断
- 项目文风提醒：贴行动，不替人物总结

SPINE_PACKAGE_MARKER

## 子智能体隔离记录

ISOLATION_LOG_SECRET

## 核心推进

SPINE_PROGRESS_MARKER

## 结尾变化

SPINE_ENDING_MARKER

## 正文纯净检查

QUALITY_SECRET

## 同步检查

SYNC_SECRET
"""


def write_text(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")
    return path


def write_json(root: Path, relative: str, value: object) -> Path:
    return write_text(root, relative, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def create_project(root: Path, *, approve: bool = True) -> Path:
    root.mkdir(parents=True)
    config = {
        "schema_version": 1,
        "global_canon": {
            "brief": "novel/00_project/brief.md",
            "book_spine": "llm-wiki/wiki/book-spine.md",
            "outline": "llm-wiki/wiki/outline.md",
            "style_canon": "llm-wiki/wiki/rules/style-canon.md",
        },
        "review_principles": ["NOVEL_REVIEW_PROTOCOL.md"],
        "blocked_paths": [
            "novel/08_archive",
            "llm-wiki/logs",
            "llm-wiki/wiki/log.md",
            ".novelforge",
        ],
    }
    write_json(root, "novelforge.json", config)
    write_text(root, "novel/00_project/brief.md", BRIEF)
    write_text(root, "llm-wiki/wiki/book-spine.md", BOOK_SPINE)
    write_text(root, "llm-wiki/wiki/outline.md", OUTLINE)
    write_text(root, "llm-wiki/wiki/rules/style-canon.md", STYLE_CANON)
    write_text(root, "NOVEL_REVIEW_PROTOCOL.md", "REVIEW_PRINCIPLE_MARKER\n")
    write_text(root, "novel/03_plot/chapters/ch001-spine.md", CHAPTER_SPINE)
    write_text(root, "novel/02_characters/hero.md", "SOURCE_ALLOWED_MARKER\n")
    write_text(root, "novel/02_characters/unlisted.md", "UNLISTED_SECRET\n")
    write_text(
        root,
        "novel/05_manuscript/ch000.md",
        "PREV_LINE_1\nPREV_LINE_2\nPREV_LINE_3\nPREV_LINE_4\n",
    )
    write_text(root, "novel/05_manuscript/ch098.md", "RECENT_ONE_MARKER\n")
    write_text(root, "novel/05_manuscript/ch099.md", "RECENT_TWO_MARKER\n")
    write_text(root, "novel/08_archive/old.md", "ARCHIVE_SECRET\n")
    job = {
        "schema_version": 1,
        "chapter": "ch001",
        "spine": "novel/03_plot/chapters/ch001-spine.md",
        "draft": "novel/05_manuscript/ch001.md",
        "chapter_sources": ["novel/02_characters/hero.md"],
        "previous_excerpt": {
            "path": "novel/05_manuscript/ch000.md",
            "start_line": 2,
            "end_line": 3,
        },
        "recent_chapters": [
            "novel/05_manuscript/ch098.md",
            "novel/05_manuscript/ch099.md",
        ],
    }
    write_json(root, "jobs/ch001.json", job)
    if approve:
        approve_project(root, "用户明确批准 v1 架构")
    return root / "jobs/ch001.json"


class NovelForgeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name) / "中文小说项目"
        self.job = create_project(self.project)

    def load_job(self) -> dict[str, object]:
        return json.loads(self.job.read_text(encoding="utf-8"))

    def save_job(self, job: dict[str, object]) -> None:
        write_json(self.project, "jobs/ch001.json", job)

    def test_approve_requires_confirmation_and_records_hashes(self) -> None:
        with self.assertRaisesRegex(NovelForgeError, "confirmation"):
            approve_project(self.project, "  ")

        approval_path = approve_project(self.project, "再次明确批准")
        approval = json.loads(approval_path.read_text(encoding="utf-8"))
        self.assertEqual(approval["schema_version"], 1)
        self.assertEqual(approval["architecture_version"], "v1")
        self.assertEqual(approval["confirmation"], "再次明确批准")
        self.assertTrue(approval["approved_at"].endswith("Z"))
        self.assertEqual(set(approval["canon"]), {"brief", "book_spine", "outline", "style_canon"})
        for entry in approval["canon"].values():
            self.assertFalse(Path(entry["path"]).is_absolute())
            self.assertRegex(entry["sha256"], r"^[0-9a-f]{64}$")

    def test_approve_rejects_hollow_style_canon(self) -> None:
        style = self.project / "llm-wiki/wiki/rules/style-canon.md"
        style.write_text(
            """# 文风正本

- 对应架构版本：v1
- 批准状态：已批准
- 当前是否可供章节写作子智能体使用：是
""",
            encoding="utf-8",
        )

        with self.assertRaises(ValidationFailure) as caught:
            approve_project(self.project, "不能批准空文风")

        self.assertIn("style-canon", str(caught.exception))

    def test_validate_rejects_unapproved_architecture(self) -> None:
        brief = self.project / "novel/00_project/brief.md"
        brief.write_text(BRIEF.replace("当前状态：已批准", "当前状态：讨论中"), encoding="utf-8")
        with self.assertRaises(ValidationFailure) as caught:
            validate_project(self.project)
        self.assertIn("批准状态必须为“已批准”", str(caught.exception))

    def test_historical_fields_cannot_override_current_gates(self) -> None:
        brief = self.project / "novel/00_project/brief.md"
        brief.write_text(
            BRIEF.replace("当前状态：已批准", "当前状态：讨论中")
            + "\n## 历史版本\n\n- 当前状态：已批准\n- 当前是否允许生成正式正文：是\n",
            encoding="utf-8",
        )
        with self.assertRaises(ValidationFailure) as approval:
            approve_project(self.project, "历史字段不能批准当前架构")
        self.assertIn("当前为 讨论中", str(approval.exception))

        brief.write_text(BRIEF, encoding="utf-8")
        approve_project(self.project, "恢复当前架构")
        spine = self.project / "novel/03_plot/chapters/ch001-spine.md"
        spine.write_text(
            CHAPTER_SPINE.replace("写作闸门：通过", "写作闸门：不通过")
            + "\n## 历史检查\n\n- 写作闸门：通过\n",
            encoding="utf-8",
        )
        with self.assertRaises(ValidationFailure) as chapter_gate:
            validate_project(self.project, self.job)
        self.assertIn("当前为 不通过", str(chapter_gate.exception))

    def test_validate_rejects_version_mismatch(self) -> None:
        outline = self.project / "llm-wiki/wiki/outline.md"
        outline.write_text(OUTLINE.replace("对应架构版本：v1", "对应架构版本：v2"), encoding="utf-8")
        with self.assertRaises(ValidationFailure) as caught:
            validate_project(self.project)
        self.assertIn("架构版本不一致", str(caught.exception))

    def test_validate_rejects_canon_changed_after_approval(self) -> None:
        book_spine = self.project / "llm-wiki/wiki/book-spine.md"
        book_spine.write_text(BOOK_SPINE + "批准后的内容变化\n", encoding="utf-8")
        with self.assertRaises(ValidationFailure) as caught:
            validate_project(self.project)
        message = str(caught.exception)
        self.assertIn("架构批准后全局正本 book_spine", message)
        self.assertIn("sha256 已变化", message)

    def test_validate_rejects_path_traversal_and_blocked_path(self) -> None:
        job = self.load_job()
        job["chapter_sources"] = ["../outside.md"]
        self.save_job(job)
        with self.assertRaises(ValidationFailure) as traversal:
            validate_project(self.project, self.job)
        self.assertIn("路径穿越", str(traversal.exception))

        job["chapter_sources"] = ["novel/08_archive/old.md"]
        self.save_job(job)
        with self.assertRaises(ValidationFailure) as blocked:
            validate_project(self.project, self.job)
        self.assertIn("blocked_paths", str(blocked.exception))

    def test_validate_enforces_source_role_boundaries(self) -> None:
        job = self.load_job()
        job["chapter_sources"] = ["architecture-approval.json"]
        self.save_job(job)
        with self.assertRaises(ValidationFailure) as control_file:
            validate_project(self.project, self.job)
        self.assertIn("控制文件", str(control_file.exception))

        job["chapter_sources"] = ["novel/05_manuscript/ch098.md"]
        self.save_job(job)
        with self.assertRaises(ValidationFailure) as reviewer_overlap:
            validate_project(self.project, self.job)
        self.assertIn("不得同时进入", str(reviewer_overlap.exception))

    def test_internal_symlink_cannot_relabel_reviewer_material_as_writer_source(self) -> None:
        link = self.project / "novel/02_characters/review-link.md"
        try:
            link.symlink_to(self.project / "NOVEL_REVIEW_PROTOCOL.md")
        except OSError as exc:
            self.skipTest(f"当前环境不能创建符号链接：{exc}")
        job = self.load_job()
        job["chapter_sources"] = ["novel/02_characters/review-link.md"]
        self.save_job(job)

        with self.assertRaises(ValidationFailure) as caught:
            validate_project(self.project, self.job)

        self.assertIn("审稿原则", str(caught.exception))

    def test_chapter_number_binds_spine_and_draft(self) -> None:
        job = self.load_job()
        job["chapter"] = "ch002"
        self.save_job(job)

        with self.assertRaises(ValidationFailure) as caught:
            validate_project(self.project, self.job)

        message = str(caught.exception)
        self.assertIn("ch002-spine.md", message)
        self.assertIn("ch002.md", message)

    def test_validate_rejects_non_utf8_explicit_source(self) -> None:
        invalid = self.project / "novel/02_characters/invalid.md"
        invalid.write_bytes(b"\xff\xfe")
        job = self.load_job()
        job["chapter_sources"] = ["novel/02_characters/invalid.md"]
        self.save_job(job)
        with self.assertRaises(ValidationFailure) as caught:
            validate_project(self.project, self.job)
        self.assertIn("不是有效 UTF-8", str(caught.exception))

    def test_validate_rejects_external_symlink_source(self) -> None:
        outside = Path(self.temporary.name) / "outside.md"
        outside.write_text("OUTSIDE_SECRET\n", encoding="utf-8")
        link = self.project / "novel/02_characters/external-link.md"
        try:
            link.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"当前环境不能创建符号链接：{exc}")
        job = self.load_job()
        job["chapter_sources"] = ["novel/02_characters/external-link.md"]
        self.save_job(job)
        with self.assertRaises(ValidationFailure) as caught:
            validate_project(self.project, self.job)
        self.assertIn("越出项目", str(caught.exception))

    def test_prepare_uses_only_writer_allowlist_and_exact_excerpt(self) -> None:
        run = prepare_project(self.project, self.job, "runs/allowlist")
        writer_task = (run / "writer-task.md").read_text(encoding="utf-8")
        for marker in (
            "BOOK_CANON_MARKER",
            "OUTLINE_CANON_MARKER",
            "STYLE_CANON_MARKER",
            "SPINE_FUNCTION_MARKER",
            "SPINE_OPENING_MARKER",
            "SPINE_GOAL_MARKER",
            "SPINE_GATE_MARKER",
            "SPINE_STANDARD_MARKER",
            "SPINE_PACKAGE_MARKER",
            "SPINE_PROGRESS_MARKER",
            "SPINE_ENDING_MARKER",
            "SOURCE_ALLOWED_MARKER",
            "PREV_LINE_2",
            "PREV_LINE_3",
        ):
            self.assertIn(marker, writer_task)
        for secret in (
            "UNSELECTED_ALLOWLIST_BOILERPLATE",
            "ISOLATION_LOG_SECRET",
            "QUALITY_SECRET",
            "SYNC_SECRET",
            "UNLISTED_SECRET",
            "PREV_LINE_1",
            "PREV_LINE_4",
            "RECENT_ONE_MARKER",
            "RECENT_TWO_MARKER",
            "REVIEW_PRINCIPLE_MARKER",
        ):
            self.assertNotIn(secret, writer_task)

        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["state"], "prepared")
        self.assertEqual(manifest["state_history"][0]["state"], "prepared")
        self.assertTrue(all({"role", "path", "sha256"} <= set(source) for source in manifest["sources"]))
        excerpt = next(source for source in manifest["sources"] if source["role"] == "previous_excerpt")
        self.assertEqual((excerpt["start_line"], excerpt["end_line"]), (2, 3))

    def test_recent_chapters_enter_only_reviewer_and_hash_change_blocks_review(self) -> None:
        run = prepare_project(self.project, self.job, "runs/review-isolation")
        write_text(self.project, "novel/05_manuscript/ch001.md", "# ch001\n\nDRAFT_MARKER\n")
        write_text(run, "writer-self-eval.md", "WRITER_REASONING_SECRET\n")
        reviewer_path = prepare_review(self.project, run)
        writer_task = (run / "writer-task.md").read_text(encoding="utf-8")
        reviewer_task = reviewer_path.read_text(encoding="utf-8")
        self.assertNotIn("RECENT_ONE_MARKER", writer_task)
        self.assertNotIn("RECENT_TWO_MARKER", writer_task)
        self.assertIn("RECENT_ONE_MARKER", reviewer_task)
        self.assertIn("RECENT_TWO_MARKER", reviewer_task)
        self.assertIn("REVIEW_PRINCIPLE_MARKER", reviewer_task)
        self.assertIn("DRAFT_MARKER", reviewer_task)
        self.assertNotIn("WRITER_REASONING_SECRET", reviewer_task)
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["state"], "review_prepared")

        second_project = Path(self.temporary.name) / "哈希变化项目"
        second_job = create_project(second_project)
        second_run = prepare_project(second_project, second_job, "runs/hash-change")
        write_text(second_project, "novel/05_manuscript/ch001.md", "# ch001\n正文\n")
        write_text(second_project, "novel/02_characters/hero.md", "SOURCE_CHANGED_AFTER_PREPARE\n")
        with self.assertRaises(ValidationFailure) as caught:
            prepare_review(second_project, second_run)
        self.assertIn("sha256 已变化", str(caught.exception))
        self.assertFalse((second_run / "reviewer-task.md").exists())

    def test_invoke_missing_context_does_not_pollute_draft(self) -> None:
        run = prepare_project(self.project, self.job, "runs/missing")
        command = [
            sys.executable,
            "-c",
            "print('NOVELFORGE_MISSING_CONTEXT: 缺少人物状态')",
        ]
        with self.assertRaisesRegex(NovelForgeError, "资料缺口"):
            invoke_stage(self.project, run, "writer", command, timeout=3)
        self.assertFalse((self.project / "novel/05_manuscript/ch001.md").exists())
        self.assertIn("NOVELFORGE_MISSING_CONTEXT:", (run / "missing-context.md").read_text(encoding="utf-8"))
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["state"], "missing_context")
        self.assertEqual([item["state"] for item in manifest["state_history"]], ["prepared", "missing_context"])

    def test_invoke_treats_metacharacters_as_argument_and_tracks_states_without_passed(self) -> None:
        run = prepare_project(self.project, self.job, "runs/success")
        metacharacter_argument = "正文 & echo SHELL_RAN > injected.txt"
        writer_command = [
            sys.executable,
            "-c",
            "import sys; sys.stdin.read(); print(sys.argv[1])",
            metacharacter_argument,
        ]
        draft = invoke_stage(self.project, run, "writer", writer_command, timeout=3)
        self.assertEqual(draft.read_text(encoding="utf-8").strip(), metacharacter_argument)
        self.assertFalse((self.project / "injected.txt").exists())
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["state"], "drafted")

        prepare_review(self.project, run)
        reviewer_command = [sys.executable, "-c", "import sys; sys.stdin.read(); print('REVIEW_COMPLETE')"]
        review = invoke_stage(self.project, run, "reviewer", reviewer_command, timeout=3)
        self.assertEqual(review.read_text(encoding="utf-8").strip(), "REVIEW_COMPLETE")
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        states = [item["state"] for item in manifest["state_history"]]
        self.assertEqual(states, ["prepared", "drafted", "review_prepared", "reviewed"])
        self.assertEqual(manifest["state"], "reviewed")
        self.assertNotIn("passed", states)

    def test_invoke_timeout_writes_no_output(self) -> None:
        run = prepare_project(self.project, self.job, "runs/timeout")
        command = [sys.executable, "-c", "import time; time.sleep(2); print('TOO_LATE')"]
        with self.assertRaisesRegex(NovelForgeError, "timeout"):
            invoke_stage(self.project, run, "writer", command, timeout=0.05)
        self.assertFalse((self.project / "novel/05_manuscript/ch001.md").exists())
        manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["state"], "prepared")

    def test_invoke_rejects_stale_locked_inputs(self) -> None:
        run = prepare_project(self.project, self.job, "runs/stale-before-invoke")
        write_text(self.project, "novel/02_characters/hero.md", "SOURCE_CHANGED_BEFORE_INVOKE\n")
        command = [sys.executable, "-c", "print('SHOULD_NOT_RUN')"]

        with self.assertRaises(ValidationFailure) as caught:
            invoke_stage(self.project, run, "writer", command, timeout=3)

        self.assertIn("sha256 已变化", str(caught.exception))
        self.assertFalse((self.project / "novel/05_manuscript/ch001.md").exists())

    def test_invoke_rederives_manifest_and_task_before_running(self) -> None:
        run = prepare_project(self.project, self.job, "runs/forged-sources")
        manifest_path = run / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["sources"] = []
        write_json(run, "manifest.json", manifest)
        side_effect = self.project / "forged-command-ran.txt"
        command = [
            sys.executable,
            "-c",
            f"from pathlib import Path; Path({str(side_effect)!r}).write_text('ran')",
        ]
        with self.assertRaises(ValidationFailure):
            invoke_stage(self.project, run, "writer", command, timeout=3)
        self.assertFalse(side_effect.exists())

        second_project = Path(self.temporary.name) / "伪造任务项目"
        second_job = create_project(second_project)
        second_run = prepare_project(second_project, second_job, "runs/forged-task")
        task_path = second_run / "writer-task.md"
        forged_task = task_path.read_text(encoding="utf-8") + "\nUNAUTHORIZED_CONTEXT\n"
        task_path.write_bytes(forged_task.encode("utf-8"))
        second_manifest_path = second_run / "manifest.json"
        second_manifest = json.loads(second_manifest_path.read_text(encoding="utf-8"))
        second_manifest["writer_task"]["sha256"] = hashlib.sha256(
            forged_task.encode("utf-8")
        ).hexdigest()
        write_json(second_run, "manifest.json", second_manifest)
        with self.assertRaisesRegex(NovelForgeError, "不是由当前已批准"):
            invoke_stage(second_project, second_run, "writer", [sys.executable, "-c", "print('x')"])

    def test_reviewer_rejects_draft_changed_after_review_packet(self) -> None:
        run = prepare_project(self.project, self.job, "runs/stale-review")
        draft = invoke_stage(
            self.project,
            run,
            "writer",
            [sys.executable, "-c", "print('# ch001\\n\\nDRAFT_A')"],
            timeout=3,
        )
        prepare_review(self.project, run)
        with self.assertRaisesRegex(NovelForgeError, "状态不能再次写作"):
            invoke_stage(
                self.project,
                run,
                "writer",
                [sys.executable, "-c", "print('LATE_REWRITE')"],
                overwrite=True,
                timeout=3,
            )
        draft.write_text("# ch001\n\nDRAFT_B\n", encoding="utf-8")

        with self.assertRaisesRegex(NovelForgeError, "待审正文已.*变化"):
            invoke_stage(
                self.project,
                run,
                "reviewer",
                [sys.executable, "-c", "print('SHOULD_NOT_REVIEW')"],
                timeout=3,
            )

        self.assertFalse((run / "review.md").exists())

    def test_invoke_rejects_batch_or_shell_entry(self) -> None:
        run = prepare_project(self.project, self.job, "runs/no-shell")
        batch = self.project / "runner.cmd"
        batch.write_text("@echo off\r\necho SHOULD_NOT_RUN\r\n", encoding="utf-8")

        with self.assertRaisesRegex(NovelForgeError, "批处理文件或命令解释器"):
            invoke_stage(self.project, run, "writer", [str(batch)], timeout=3)

        self.assertFalse((self.project / "novel/05_manuscript/ch001.md").exists())

    @unittest.skipUnless(os.name == "nt", "Windows 8.3 short paths only")
    def test_prepare_accepts_canonicalized_windows_short_output_path(self) -> None:
        import ctypes

        get_short_path = ctypes.windll.kernel32.GetShortPathNameW
        size = get_short_path(str(self.project), None, 0)
        if not size:
            self.skipTest("无法读取 Windows 8.3 短路径")
        buffer = ctypes.create_unicode_buffer(size)
        get_short_path(str(self.project), buffer, size)
        short_project = Path(buffer.value)
        if "~" not in str(short_project):
            self.skipTest("当前卷未启用 8.3 短路径")

        run = prepare_project(
            self.project,
            self.job,
            short_project / "runs" / "short-output",
        )

        self.assertTrue(run.is_dir())
        self.assertTrue(run.is_relative_to(self.project.resolve()))

    def test_script_entry_runs_without_installing_package(self) -> None:
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [
                sys.executable,
                str(REPOSITORY_ROOT / "scripts/novelforge.py"),
                "validate",
                str(self.project),
                "--job",
                str(self.job),
            ],
            cwd=Path(self.temporary.name),
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("验证通过", result.stdout)

    def test_script_invoke_accepts_documented_argument_order(self) -> None:
        run = prepare_project(self.project, self.job, "runs/cli-invoke")
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [
                sys.executable,
                str(REPOSITORY_ROOT / "scripts/novelforge.py"),
                "invoke",
                str(self.project),
                "--run",
                str(run),
                "--stage",
                "writer",
                "--timeout",
                "3",
                "--",
                sys.executable,
                "-c",
                "import sys; sys.stdin.read(); print('CLI_DRAFT')",
            ],
            cwd=Path(self.temporary.name),
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (self.project / "novel/05_manuscript/ch001.md").read_text(encoding="utf-8").strip(),
            "CLI_DRAFT",
        )


class InitProjectTestCase(unittest.TestCase):
    def test_init_copies_template_approval_and_root_rules_and_refuses_nonempty_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source = base / "source-repository"
            template = source / "templates/novel-project"
            write_text(template, "architecture-approval.json", "{}\n")
            write_text(template, "novelforge.json", "{}\n")
            for name in (
                "AGENTS.md",
                "Claude.md",
                "AIGC_DETECTION_PRINCIPLES.md",
                "NOVEL_REVIEW_PROTOCOL.md",
            ):
                write_text(source, name, f"ROOT_{name}\n")

            target = base / "new-project"
            initialized = init_project(target, repository_root=source)
            self.assertEqual((initialized / "architecture-approval.json").read_text(encoding="utf-8"), "{}\n")
            self.assertEqual((initialized / "AGENTS.md").read_text(encoding="utf-8"), "ROOT_AGENTS.md\n")
            with self.assertRaisesRegex(NovelForgeError, "非空"):
                init_project(target, repository_root=source)


if __name__ == "__main__":
    unittest.main()
