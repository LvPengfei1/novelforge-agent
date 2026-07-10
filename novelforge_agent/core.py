from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence


SCHEMA_VERSION = 1
CONFIG_NAME = "novelforge.json"
APPROVAL_NAME = "architecture-approval.json"
GLOBAL_CANON_KEYS = ("brief", "book_spine", "outline", "style_canon")
WRITER_SPINE_SECTIONS = (
    "章节功能",
    "开章状态",
    "本章目标",
    "架构与近章闸门",
    "内容执行标准",
    "章节写作包",
    "核心推进",
    "结尾变化",
)
ALLOWED_MANIFEST_ROLES = {
    "novelforge_config",
    "architecture_approval",
    "chapter_job",
    "brief",
    "book_spine",
    "outline",
    "style_canon",
    "chapter_spine",
    "chapter_source",
    "previous_excerpt",
    "recent_chapter",
    "review_principle",
}
RUN_STATES = {"prepared", "missing_context", "drafted", "review_prepared", "reviewed"}
RUN_TRANSITIONS = {
    "prepared": {"missing_context", "drafted", "review_prepared"},
    "missing_context": {"missing_context", "drafted"},
    "drafted": {"drafted", "review_prepared"},
    "review_prepared": {"reviewed"},
    "reviewed": {"reviewed"},
}


class NovelForgeError(Exception):
    """A user-facing workflow error."""


class ValidationFailure(NovelForgeError):
    def __init__(self, errors: Iterable[str], heading: str = "验证失败") -> None:
        self.errors = tuple(errors)
        self.heading = heading
        super().__init__(self._format())

    def _format(self) -> str:
        lines = [f"{self.heading}（{len(self.errors)} 项）："]
        lines.extend(f"  {index}. {error}" for index, error in enumerate(self.errors, 1))
        return "\n".join(lines)


@dataclass(frozen=True)
class BlockedPath:
    relative: Path
    resolved: Path


@dataclass(frozen=True)
class TextFile:
    role: str
    relative_path: str
    absolute_path: Path
    raw: bytes
    text: str
    stages: tuple[str, ...]
    start_line: int | None = None
    end_line: int | None = None

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.raw).hexdigest()

    def manifest_entry(self) -> dict[str, Any]:
        entry: dict[str, Any] = {
            "role": self.role,
            "path": self.relative_path,
            "sha256": self.sha256,
            "stages": list(self.stages),
        }
        if self.start_line is not None:
            entry["start_line"] = self.start_line
            entry["end_line"] = self.end_line
        return entry


@dataclass(frozen=True)
class ValidatedProject:
    root: Path
    config: dict[str, Any]
    config_file: TextFile
    blocked_paths: tuple[BlockedPath, ...]
    global_canon: dict[str, TextFile]
    review_principles: tuple[TextFile, ...]
    architecture_version: str | None = None
    approval_file: TextFile | None = None
    job: dict[str, Any] | None = None
    job_file: TextFile | None = None
    chapter_spine: TextFile | None = None
    chapter_sources: tuple[TextFile, ...] = ()
    previous_excerpt: TextFile | None = None
    recent_chapters: tuple[TextFile, ...] = ()
    draft_relative_path: str | None = None
    draft_path: Path | None = None


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _normalize_relative(path: Path) -> str:
    return path.as_posix()


def _parse_relative_path(value: Any, label: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} 必须是非空的项目内相对路径")
        return None

    path = Path(value)
    if path.is_absolute() or path.drive or path.root:
        errors.append(f"{label} 必须是项目内相对路径：{value!r}")
        return None
    if any(":" in part or any(ord(character) < 32 for character in part) for part in path.parts):
        errors.append(f"{label} 含有不安全的路径字符：{value!r}")
        return None
    if any(part == ".." for part in path.parts):
        errors.append(f"{label} 含有路径穿越 '..'：{value!r}")
        return None
    if not path.parts or path == Path("."):
        errors.append(f"{label} 不能指向项目根目录")
        return None
    return path


def _build_blocked_paths(root: Path, values: Any, errors: list[str]) -> tuple[BlockedPath, ...]:
    if not isinstance(values, list):
        errors.append("novelforge.json 的 blocked_paths 必须是路径数组")
        return ()

    blocked: list[BlockedPath] = []
    for index, value in enumerate(values):
        relative = _parse_relative_path(value, f"blocked_paths[{index}]", errors)
        if relative is None:
            continue
        resolved = (root / relative).resolve(strict=False)
        if not _is_within(resolved, root):
            errors.append(f"blocked_paths[{index}] 经符号链接解析后越出项目：{value!r}")
            continue
        blocked.append(BlockedPath(relative=relative, resolved=resolved))
    return tuple(blocked)


def _is_blocked(relative: Path, resolved: Path, blocked_paths: Sequence[BlockedPath]) -> bool:
    return any(
        _is_within(relative, blocked.relative) or _is_within(resolved, blocked.resolved)
        for blocked in blocked_paths
    )


def _decode_utf8(raw: bytes, label: str, errors: list[str]) -> str | None:
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        errors.append(f"{label} 不是有效 UTF-8：字节位置 {exc.start}")
        return None


def _read_input_file(
    root: Path,
    relative_value: Any,
    label: str,
    role: str,
    stages: tuple[str, ...],
    blocked_paths: Sequence[BlockedPath],
    errors: list[str],
    *,
    start_line: int | None = None,
    end_line: int | None = None,
) -> TextFile | None:
    relative = _parse_relative_path(relative_value, label, errors)
    if relative is None:
        return None

    candidate = root / relative
    try:
        resolved = candidate.resolve(strict=True)
    except (FileNotFoundError, OSError) as exc:
        errors.append(f"{label} 不存在或无法解析：{relative_value!r}（{exc}）")
        return None

    if not _is_within(resolved, root):
        errors.append(f"{label} 经符号链接解析后越出项目：{relative_value!r}")
        return None
    if _is_blocked(relative, resolved, blocked_paths):
        errors.append(f"{label} 落入 blocked_paths：{relative_value!r}")
        return None
    if not resolved.is_file():
        errors.append(f"{label} 不是普通文件：{relative_value!r}")
        return None

    try:
        raw = resolved.read_bytes()
    except OSError as exc:
        errors.append(f"{label} 无法读取：{relative_value!r}（{exc}）")
        return None
    text = _decode_utf8(raw, label, errors)
    if text is None:
        return None
    return TextFile(
        role=role,
        relative_path=_normalize_relative(relative),
        absolute_path=resolved,
        raw=raw,
        text=text,
        stages=stages,
        start_line=start_line,
        end_line=end_line,
    )


def _read_fixed_file(
    root: Path,
    name: str,
    label: str,
    errors: list[str],
    *,
    role: str = "novelforge_config",
    stages: tuple[str, ...] = ("control",),
) -> TextFile | None:
    candidate = root / name
    try:
        resolved = candidate.resolve(strict=True)
    except (FileNotFoundError, OSError) as exc:
        errors.append(f"{label} 不存在或无法解析：{name!r}（{exc}）")
        return None
    if not _is_within(resolved, root):
        errors.append(f"{label} 经符号链接解析后越出项目：{name!r}")
        return None
    if not resolved.is_file():
        errors.append(f"{label} 不是普通文件：{name!r}")
        return None
    try:
        raw = resolved.read_bytes()
    except OSError as exc:
        errors.append(f"{label} 无法读取：{exc}")
        return None
    text = _decode_utf8(raw, label, errors)
    if text is None:
        return None
    return TextFile(
        role=role,
        relative_path=name,
        absolute_path=resolved,
        raw=raw,
        text=text,
        stages=stages,
    )


def _parse_json_file(file: TextFile, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(file.text)
    except json.JSONDecodeError as exc:
        errors.append(f"{label} 不是有效 JSON：第 {exc.lineno} 行第 {exc.colno} 列，{exc.msg}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label} 顶层必须是 JSON 对象")
        return None
    return value


def _check_schema(value: dict[str, Any], label: str, errors: list[str]) -> None:
    version = value.get("schema_version")
    if type(version) is not int or version != SCHEMA_VERSION:
        errors.append(f"{label} schema_version 必须为 {SCHEMA_VERSION}")


def _project_root(project: os.PathLike[str] | str) -> Path:
    candidate = Path(project).expanduser()
    try:
        root = candidate.resolve(strict=True)
    except (FileNotFoundError, OSError) as exc:
        raise NovelForgeError(f"项目目录不存在或无法解析：{candidate}（{exc}）") from exc
    if not root.is_dir():
        raise NovelForgeError(f"项目路径不是目录：{root}")
    return root


def _load_config_only(root: Path) -> tuple[dict[str, Any], TextFile, tuple[BlockedPath, ...]]:
    errors: list[str] = []
    config_file = _read_fixed_file(root, CONFIG_NAME, "项目配置", errors)
    if config_file is None:
        raise ValidationFailure(errors)
    config = _parse_json_file(config_file, CONFIG_NAME, errors)
    if config is None:
        raise ValidationFailure(errors)
    _check_schema(config, CONFIG_NAME, errors)

    global_canon = config.get("global_canon")
    if not isinstance(global_canon, dict):
        errors.append("novelforge.json 的 global_canon 必须是对象")
    review_principles = config.get("review_principles")
    if not isinstance(review_principles, list) or not review_principles:
        errors.append("novelforge.json 的 review_principles 必须是非空路径数组")
    blocked_paths = _build_blocked_paths(root, config.get("blocked_paths"), errors)
    if errors:
        raise ValidationFailure(errors)
    return config, config_file, blocked_paths


_FIELD_RE = re.compile(
    r"^\s*(?:[-*+]\s+|\d+[.)、]\s+)?(?P<key>[^：:\r\n]+?)[：:]\s*(?P<value>.*?)\s*$"
)
_H2_RE = re.compile(r"^##[ \t]+(?P<name>.+?)[ \t]*#*[ \t]*\r?$", re.MULTILINE)


def _clean_field_key(value: str) -> str:
    return value.strip().strip("*`_ ")


def _clean_scalar(value: str) -> str:
    return value.strip().strip("*`_ \t\r\n\"'“”‘’")


def _markdown_fields(
    text: str,
    errors: list[str] | None = None,
    label: str = "Markdown",
) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = _FIELD_RE.match(line)
        if match is None:
            continue
        key = _clean_field_key(match.group("key"))
        if key in fields:
            if errors is not None:
                errors.append(f"{label} 的字段“{key}”重复")
            continue
        fields[key] = match.group("value").strip()
    return fields


def _field(fields: dict[str, str], aliases: Sequence[str]) -> str | None:
    for alias in aliases:
        if alias in fields:
            return _clean_scalar(fields[alias])
    return None


def _markdown_h2_sections(text: str) -> dict[str, list[str]]:
    matches = list(_H2_RE.finditer(text))
    sections: dict[str, list[str]] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        name = _clean_scalar(match.group("name"))
        sections.setdefault(name, []).append(text[match.start() : end].rstrip())
    return sections


def _single_h2_section(
    file: TextFile,
    name: str,
    label: str,
    errors: list[str],
) -> str | None:
    matches = _markdown_h2_sections(file.text).get(name, [])
    if not matches:
        errors.append(f"{label} 缺少“{name}”章节")
        return None
    if len(matches) > 1:
        errors.append(f"{label} 的“{name}”章节重复")
        return None
    return matches[0]


def _validate_global_gate(global_canon: dict[str, TextFile], errors: list[str]) -> str | None:
    versions: dict[str, str] = {}
    permission_sections = {
        "brief": "架构状态",
        "book_spine": "架构权限",
        "outline": "架构权限",
        "style_canon": "使用权限",
    }
    for key in GLOBAL_CANON_KEYS:
        file = global_canon.get(key)
        if file is None:
            continue
        section = _single_h2_section(file, permission_sections[key], f"全局正本 {key}", errors)
        if section is None:
            continue
        fields = _markdown_fields(section, errors, f"全局正本 {key} 的权限章节")
        version = _field(fields, ("架构版本", "对应架构版本", "当前架构版本"))
        status = _field(fields, ("批准状态", "当前状态", "架构状态"))
        writable = _field(
            fields,
            (
                "当前是否允许生成正式正文",
                "当前是否可供章节写作子智能体使用",
                "可写标志",
                "当前是否可写",
            ),
        )
        if not version:
            errors.append(f"全局正本 {key} 的架构版本为空")
        else:
            versions[key] = version
        if status != "已批准":
            errors.append(f"全局正本 {key} 的批准状态必须为“已批准”，当前为 {status or '空'}")
        if writable != "是":
            errors.append(f"全局正本 {key} 的可写标志必须为“是”，当前为 {writable or '空'}")

    unique_versions = set(versions.values())
    if len(unique_versions) > 1:
        details = "，".join(f"{key}={value}" for key, value in versions.items())
        errors.append(f"四份全局正本的架构版本不一致：{details}")
    return next(iter(unique_versions)) if len(unique_versions) == 1 else None


_BRIEF_REQUIRED_FIELDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "故事承诺",
        ("故事承诺", "读者持续追读所期待的核心体验", "读者持续期待的核心体验"),
    ),
    ("主角欲望", ("主角欲望", "主角核心欲望", "主角真正想得到什么")),
    (
        "麻烦发动机",
        ("麻烦发动机", "主角的欲望会怎样持续制造麻烦", "主角欲望或缺点怎样制造下一轮麻烦"),
    ),
    ("外部动力", ("外部动力", "外部主线怎样迫使主角不能退出")),
    (
        "主要关系",
        ("主要关系", "主要关系方向", "主要关系怎样改变主线，而不是装饰主线", "主要关系怎样改变主线"),
    ),
    (
        "阶段不可逆变化",
        ("阶段不可逆变化", "当前阶段终点", "当前阶段结束时必须发生的不可逆变化"),
    ),
)


def _validate_brief(brief: TextFile | None, errors: list[str]) -> None:
    if brief is None:
        return
    section = _single_h2_section(brief, "故事承诺与长线动力", "brief", errors)
    if section is None:
        return
    fields = _markdown_fields(section, errors, "brief 的故事承诺与长线动力")
    for label, aliases in _BRIEF_REQUIRED_FIELDS:
        if not _field(fields, aliases):
            errors.append(f"brief 的{label}不能为空")


_BOOK_SPINE_REQUIRED_FIELDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("读者承诺", ("读者持续期待的核心体验",)),
    ("主角欲望", ("主角核心欲望",)),
    ("麻烦发动机", ("主角欲望或缺点怎样制造下一轮麻烦",)),
    ("主要关系动力", ("主要关系怎样改变主线",)),
    ("长线动力", ("长线动力为何不会在数章后耗尽",)),
    ("最终问题", ("最终必须回答的问题",)),
)


_STYLE_CANON_REQUIRED_FIELDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("叙事视角与距离", ("叙事视角与距离",)),
    ("叙述者态度", ("叙述者态度",)),
    ("句段节奏", ("句段节奏",)),
    ("对话身份差异", ("对话的身份差异",)),
    ("项目阅读感", ("必须保留的阅读感",)),
    ("写偏边界", ("容易写偏的方向", "不适合本项目的叙述方式")),
)


def _validate_required_fields(
    text: str,
    label: str,
    requirements: Sequence[tuple[str, Sequence[str]]],
    errors: list[str],
) -> None:
    fields = _markdown_fields(text, errors, label)
    for field_label, aliases in requirements:
        if not _field(fields, aliases):
            errors.append(f"{label} 的{field_label}不能为空")


def _validate_book_spine(book_spine: TextFile | None, errors: list[str]) -> None:
    if book_spine is None:
        return
    sections: list[str] = []
    for name in ("读者承诺与人物发动机", "核心矛盾"):
        section = _single_h2_section(book_spine, name, "book-spine", errors)
        if section is not None:
            sections.append(section)
    if len(sections) == 2:
        _validate_required_fields(
            "\n".join(sections),
            "book-spine",
            _BOOK_SPINE_REQUIRED_FIELDS,
            errors,
        )


def _validate_style_canon(style_canon: TextFile | None, errors: list[str]) -> None:
    if style_canon is None:
        return
    sections: list[str] = []
    for name in ("叙事基准", "人物表达", "项目边界"):
        section = _single_h2_section(style_canon, name, "style-canon", errors)
        if section is not None:
            sections.append(section)
    if len(sections) == 3:
        _validate_required_fields(
            "\n".join(sections),
            "style-canon",
            _STYLE_CANON_REQUIRED_FIELDS,
            errors,
        )


def _markdown_table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        if not cells or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows[1:] if rows else []


def _validate_outline(outline: TextFile | None, errors: list[str]) -> None:
    if outline is None:
        return
    permission = _single_h2_section(outline, "架构权限", "outline", errors)
    if permission is None:
        return
    fields = _markdown_fields(permission, errors, "outline 的架构权限")
    if _field(fields, ("与全书龙骨的版本是否一致",)) != "是":
        errors.append("outline 必须明确与全书龙骨版本一致")
    sections = _markdown_h2_sections(outline.text)
    stage_sections = sections.get("阶段规划", [])
    if len(stage_sections) != 1:
        errors.append("outline 必须且只能包含一个“阶段规划”章节")
        return
    rows = _markdown_table_rows(stage_sections[0])
    if not any(len(row) >= 5 and all(cell for cell in row[:5]) for row in rows):
        errors.append("outline 的阶段规划至少要有一行完整的范围、人物追求、阻力、选择与代价、不可逆结果")


def _validate_architecture_approval(
    root: Path,
    global_canon: dict[str, TextFile],
    architecture_version: str | None,
    errors: list[str],
) -> TextFile | None:
    approval_file = _read_fixed_file(
        root,
        APPROVAL_NAME,
        "架构批准记录",
        errors,
        role="architecture_approval",
        stages=("control",),
    )
    if approval_file is None:
        return None
    approval = _parse_json_file(approval_file, APPROVAL_NAME, errors)
    if approval is None:
        return approval_file
    _check_schema(approval, APPROVAL_NAME, errors)

    recorded_version = approval.get("architecture_version")
    if not isinstance(recorded_version, str) or not recorded_version.strip():
        errors.append("architecture-approval.json 的 architecture_version 不能为空")
    elif architecture_version is not None and recorded_version != architecture_version:
        errors.append(
            "architecture-approval.json 的版本与当前全局正本不一致："
            f"批准 {recorded_version}，当前 {architecture_version}"
        )

    approved_at = approval.get("approved_at")
    if not isinstance(approved_at, str) or not approved_at.strip():
        errors.append("architecture-approval.json 的 approved_at 不能为空")
    confirmation = approval.get("confirmation")
    if not isinstance(confirmation, str) or not confirmation.strip():
        errors.append("architecture-approval.json 缺少非空 confirmation")

    recorded_canon = approval.get("canon")
    if recorded_canon is None:
        recorded_canon = approval.get("global_canon")
    if not isinstance(recorded_canon, dict):
        errors.append("architecture-approval.json 的 canon 必须是对象")
        return approval_file
    for key in GLOBAL_CANON_KEYS:
        current = global_canon.get(key)
        entry = recorded_canon.get(key)
        if not isinstance(entry, dict):
            errors.append(f"architecture-approval.json 缺少 canon.{key} 记录")
            continue
        path = entry.get("path")
        digest = entry.get("sha256")
        if current is None:
            continue
        if path != current.relative_path:
            errors.append(
                f"architecture-approval.json 中 {key} 的路径不符：批准 {path!r}，当前 {current.relative_path!r}"
            )
        if digest != current.sha256:
            errors.append(
                f"架构批准后全局正本 {key} 的 sha256 已变化："
                f"批准 {digest or '空'}，当前 {current.sha256}"
            )
    return approval_file


def _validate_spine(spine: TextFile | None, global_version: str | None, errors: list[str]) -> None:
    if spine is None:
        return
    gate_section = _single_h2_section(spine, "架构与近章闸门", "章节 spine", errors)
    if gate_section is None:
        return
    fields = _markdown_fields(gate_section, errors, "章节 spine 的架构与近章闸门")
    version = _field(fields, ("当前架构版本", "对应架构版本", "架构版本"))
    confirmed = _field(fields, ("架构是否已经得到用户确认", "用户已确认", "用户确认状态"))
    gate = _field(fields, ("写作闸门",))
    if not version:
        errors.append("章节 spine 的架构版本为空")
    elif global_version is not None and version != global_version:
        errors.append(f"章节 spine 架构版本 {version} 与全局版本 {global_version} 不一致")
    if confirmed not in {"是", "已确认"}:
        errors.append(f"章节 spine 必须标明用户已确认，当前为 {confirmed or '空'}")
    if gate != "通过":
        errors.append(f"章节 spine 的写作闸门必须为“通过”，当前为 {gate or '空'}")

    sections = _markdown_h2_sections(spine.text)
    for name in WRITER_SPINE_SECTIONS:
        count = len(sections.get(name, ()))
        if count == 0:
            errors.append(f"章节 spine 缺少“{name}”章节")
        elif count > 1:
            errors.append(f"章节 spine 的“{name}”章节重复")

    required_by_section = {
        "本章目标": (
            ("剧情目标", ("剧情目标",)),
            ("人物目标", ("人物目标",)),
        ),
        "架构与近章闸门": (
            ("当前故事承诺", ("当前故事承诺",)),
            ("所属阶段及阶段终点", ("所属阶段及阶段终点",)),
            ("选择、代价或状态变化", ("本章必须造成的选择、代价或状态变化",)),
            ("近章结构差异", ("本章与近章不同的场景动力",)),
        ),
        "内容执行标准": (("本章阅读感", ("本章阅读感",)),),
        "章节写作包": (
            ("开场状态", ("本章开场状态",)),
            ("人物动机", ("人物动机",)),
            ("核心冲突", ("本章核心冲突",)),
            ("必须推进", ("本章必须推进",)),
            ("结尾变化预期", ("本章结尾变化预期",)),
            ("文风提醒", ("项目文风提醒",)),
        ),
    }
    for section_name, requirements in required_by_section.items():
        matching = sections.get(section_name, [])
        if len(matching) == 1:
            _validate_required_fields(
                matching[0],
                f"章节 spine 的{section_name}",
                requirements,
                errors,
            )


def _resolve_job_argument(root: Path, job: os.PathLike[str] | str, errors: list[str]) -> str | None:
    value = Path(job).expanduser()
    if value.is_absolute() or value.drive:
        try:
            resolved = value.resolve(strict=True)
        except (FileNotFoundError, OSError) as exc:
            errors.append(f"章节任务不存在或无法解析：{value}（{exc}）")
            return None
        if not _is_within(resolved, root):
            errors.append(f"章节任务必须位于项目内：{value}")
            return None
        return _normalize_relative(resolved.relative_to(root))
    relative = _parse_relative_path(str(value), "章节任务", errors)
    return _normalize_relative(relative) if relative is not None else None


def _safe_chapter_name(value: Any, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append("章节任务的 chapter 必须是非空字符串")
        return None
    chapter = value.strip()
    if re.fullmatch(r"ch\d{3,}", chapter) is None:
        errors.append(f"章节任务的 chapter 必须使用 ch 加至少三位数字：{value!r}")
        return None
    return chapter


def _string_list(value: Any, label: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{label} 必须是路径数组")
        return []
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{label}[{index}] 必须是非空路径字符串")
            continue
        result.append(item)
    return result


def _resolve_draft_path(root: Path, value: Any, errors: list[str]) -> tuple[str | None, Path | None]:
    relative = _parse_relative_path(value, "draft", errors)
    if relative is None:
        return None, None
    if len(relative.parts) < 3 or tuple(part.casefold() for part in relative.parts[:2]) != (
        "novel",
        "05_manuscript",
    ):
        errors.append(f"draft 必须位于 novel/05_manuscript：{value!r}")
        return _normalize_relative(relative), None

    manuscript = root / "novel" / "05_manuscript"
    try:
        manuscript_resolved = manuscript.resolve(strict=True)
        parent_resolved = (root / relative).parent.resolve(strict=True)
    except (FileNotFoundError, OSError) as exc:
        errors.append(f"draft 的父目录不存在或无法解析：{value!r}（{exc}）")
        return _normalize_relative(relative), None
    if not _is_within(manuscript_resolved, root):
        errors.append("novel/05_manuscript 经符号链接解析后越出项目")
        return _normalize_relative(relative), None
    if not _is_within(parent_resolved, manuscript_resolved):
        errors.append(f"draft 经符号链接解析后不在 novel/05_manuscript：{value!r}")
        return _normalize_relative(relative), None

    candidate = root / relative
    if os.path.lexists(candidate):
        try:
            resolved = candidate.resolve(strict=True)
        except (FileNotFoundError, OSError) as exc:
            errors.append(f"draft 已存在但无法安全解析：{value!r}（{exc}）")
            return _normalize_relative(relative), None
        if not _is_within(resolved, manuscript_resolved) or not resolved.is_file():
            errors.append(f"draft 已存在但不是 manuscript 内普通文件：{value!r}")
            return _normalize_relative(relative), None
        try:
            raw = resolved.read_bytes()
        except OSError as exc:
            errors.append(f"draft 无法读取：{value!r}（{exc}）")
            return _normalize_relative(relative), None
        _decode_utf8(raw, "draft", errors)
    return _normalize_relative(relative), candidate


def _path_has_prefix(relative_path: str, *prefixes: tuple[str, ...]) -> bool:
    parts = tuple(part.casefold() for part in Path(relative_path).parts)
    return any(parts[: len(prefix)] == tuple(part.casefold() for part in prefix) for prefix in prefixes)


def _file_identity(file: TextFile) -> tuple[Any, ...]:
    try:
        stat = file.absolute_path.stat()
    except OSError:
        return ("path", os.path.normcase(str(file.absolute_path)))
    return ("inode", stat.st_dev, stat.st_ino)


def _validate_job_role_boundaries(
    validated_files: Sequence[TextFile],
    label: str,
    errors: list[str],
) -> None:
    counts = Counter(_file_identity(file) for file in validated_files)
    labels = {_file_identity(file): file.relative_path for file in validated_files}
    for identity, count in counts.items():
        if count > 1:
            errors.append(
                f"{label} 通过重复路径或链接列入同一文件：{labels[identity]}"
            )


def validate_project(
    project: os.PathLike[str] | str,
    job: os.PathLike[str] | str | None = None,
    *,
    require_approval: bool = True,
) -> ValidatedProject:
    root = _project_root(project)
    config, config_file, blocked_paths = _load_config_only(root)
    errors: list[str] = []

    global_config = config["global_canon"]
    global_canon: dict[str, TextFile] = {}
    for key in GLOBAL_CANON_KEYS:
        if key not in global_config:
            errors.append(f"novelforge.json 缺少 global_canon.{key}")
            continue
        file = _read_input_file(
            root,
            global_config[key],
            f"global_canon.{key}",
            key,
            ("writer", "reviewer"),
            blocked_paths,
            errors,
        )
        if file is not None:
            global_canon[key] = file

    review_values = _string_list(config["review_principles"], "review_principles", errors)
    review_principles: list[TextFile] = []
    for index, value in enumerate(review_values):
        file = _read_input_file(
            root,
            value,
            f"review_principles[{index}]",
            "review_principle",
            ("reviewer",),
            blocked_paths,
            errors,
        )
        if file is not None:
            review_principles.append(file)

    global_version = _validate_global_gate(global_canon, errors)
    _validate_brief(global_canon.get("brief"), errors)
    _validate_book_spine(global_canon.get("book_spine"), errors)
    _validate_outline(global_canon.get("outline"), errors)
    _validate_style_canon(global_canon.get("style_canon"), errors)
    approval_file = (
        _validate_architecture_approval(root, global_canon, global_version, errors)
        if require_approval
        else None
    )

    if job is None:
        if errors:
            raise ValidationFailure(errors)
        return ValidatedProject(
            root=root,
            config=config,
            config_file=config_file,
            blocked_paths=blocked_paths,
            global_canon=global_canon,
            review_principles=tuple(review_principles),
            architecture_version=global_version,
            approval_file=approval_file,
        )

    job_relative = _resolve_job_argument(root, job, errors)
    job_file = None
    job_data = None
    chapter_spine = None
    chapter_sources: list[TextFile] = []
    previous_excerpt = None
    recent_chapters: list[TextFile] = []
    draft_relative = None
    draft_path = None
    chapter_name = None

    if job_relative is not None:
        job_file = _read_input_file(
            root,
            job_relative,
            "章节任务",
            "chapter_job",
            ("control",),
            blocked_paths,
            errors,
        )
    if job_file is not None:
        job_data = _parse_json_file(job_file, "章节任务", errors)

    if job_data is not None:
        _check_schema(job_data, "章节任务", errors)
        chapter_name = _safe_chapter_name(job_data.get("chapter"), errors)

        chapter_spine = _read_input_file(
            root,
            job_data.get("spine"),
            "spine",
            "chapter_spine",
            ("writer", "reviewer"),
            blocked_paths,
            errors,
        )

        source_values = _string_list(job_data.get("chapter_sources"), "chapter_sources", errors)
        for index, value in enumerate(source_values):
            file = _read_input_file(
                root,
                value,
                f"chapter_sources[{index}]",
                "chapter_source",
                ("writer", "reviewer"),
                blocked_paths,
                errors,
            )
            if file is not None:
                chapter_sources.append(file)

        previous = job_data.get("previous_excerpt")
        if previous is not None:
            if not isinstance(previous, dict):
                errors.append("previous_excerpt 必须为 null 或对象")
            else:
                start_line = previous.get("start_line")
                end_line = previous.get("end_line")
                valid_range = True
                if type(start_line) is not int or start_line < 1:
                    errors.append("previous_excerpt.start_line 必须是从 1 开始的整数")
                    valid_range = False
                if type(end_line) is not int or end_line < 1:
                    errors.append("previous_excerpt.end_line 必须是从 1 开始的整数")
                    valid_range = False
                if valid_range and end_line < start_line:
                    errors.append("previous_excerpt.end_line 不能小于 start_line")
                    valid_range = False
                previous_excerpt = _read_input_file(
                    root,
                    previous.get("path"),
                    "previous_excerpt.path",
                    "previous_excerpt",
                    ("writer", "reviewer"),
                    blocked_paths,
                    errors,
                    start_line=start_line if valid_range else None,
                    end_line=end_line if valid_range else None,
                )
                if previous_excerpt is not None and valid_range:
                    line_count = len(previous_excerpt.text.splitlines(keepends=True))
                    if end_line > line_count:
                        errors.append(
                            f"previous_excerpt 行区间 {start_line}-{end_line} 超出文件总行数 {line_count}"
                        )

        recent_values = _string_list(job_data.get("recent_chapters"), "recent_chapters", errors)
        if len(recent_values) > 3:
            errors.append(f"recent_chapters 最多允许 3 个，当前为 {len(recent_values)} 个")
        for index, value in enumerate(recent_values[:3]):
            file = _read_input_file(
                root,
                value,
                f"recent_chapters[{index}]",
                "recent_chapter",
                ("reviewer",),
                blocked_paths,
                errors,
            )
            if file is not None:
                recent_chapters.append(file)

        draft_relative, draft_path = _resolve_draft_path(root, job_data.get("draft"), errors)
        _validate_spine(chapter_spine, global_version, errors)

        if chapter_name is not None:
            if chapter_spine is not None:
                expected_spine_name = f"{chapter_name}-spine.md"
                if Path(chapter_spine.relative_path).name.casefold() != expected_spine_name.casefold():
                    errors.append(
                        f"章节任务 {chapter_name} 必须绑定 {expected_spine_name}，当前为 "
                        f"{Path(chapter_spine.relative_path).name}"
                    )
                basic_section = _single_h2_section(
                    chapter_spine,
                    "基本信息",
                    "章节 spine",
                    errors,
                )
                if basic_section is not None:
                    basic_fields = _markdown_fields(
                        basic_section,
                        errors,
                        "章节 spine 的基本信息",
                    )
                    spine_chapter = _field(basic_fields, ("章节编号",))
                    if spine_chapter != chapter_name:
                        errors.append(
                            f"章节 spine 的章节编号必须为 {chapter_name}，当前为 {spine_chapter or '空'}"
                        )
            if draft_relative is not None:
                expected_draft_name = f"{chapter_name}.md"
                if Path(draft_relative).name.casefold() != expected_draft_name.casefold():
                    errors.append(
                        f"章节任务 {chapter_name} 的 draft 文件名必须为 {expected_draft_name}，当前为 "
                        f"{Path(draft_relative).name}"
                    )

        if chapter_spine is not None and not _path_has_prefix(
            chapter_spine.relative_path,
            ("novel", "03_plot", "chapters"),
        ):
            errors.append("spine 必须位于 novel/03_plot/chapters")
        if previous_excerpt is not None and not _path_has_prefix(
            previous_excerpt.relative_path,
            ("novel", "05_manuscript"),
        ):
            errors.append("previous_excerpt.path 必须位于 novel/05_manuscript")
        for recent in recent_chapters:
            if not _path_has_prefix(
                recent.relative_path,
                ("novel", "05_manuscript"),
                ("novel", "03_plot", "chapters"),
            ):
                errors.append(
                    f"recent_chapters 只能使用正文或章节龙骨：{recent.relative_path}"
                )

        _validate_job_role_boundaries(chapter_sources, "chapter_sources", errors)
        _validate_job_role_boundaries(recent_chapters, "recent_chapters", errors)
        reserved_files = [config_file, *global_canon.values(), *review_principles]
        if approval_file is not None:
            reserved_files.append(approval_file)
        if job_file is not None:
            reserved_files.append(job_file)
        if chapter_spine is not None:
            reserved_files.append(chapter_spine)
        reserved_writer_targets = {_file_identity(file) for file in reserved_files}
        for source in chapter_sources:
            source_key = _file_identity(source)
            if source_key in reserved_writer_targets:
                errors.append(
                    f"chapter_sources 不得把控制文件、全局正本、章节 spine 或审稿原则重复作为本章来源："
                    f"{source.relative_path}"
                )
        recent_paths = {_file_identity(file) for file in recent_chapters}
        writer_source_paths = {_file_identity(file) for file in chapter_sources}
        overlap = recent_paths & writer_source_paths
        for source in chapter_sources:
            if _file_identity(source) in overlap:
                errors.append(
                    "recent_chapters 的全文不得同时进入 writer 的 chapter_sources："
                    f"{source.relative_path}"
                )
        if (
            previous_excerpt is not None
            and _file_identity(previous_excerpt) in writer_source_paths
        ):
            errors.append("previous_excerpt 的原文件不得同时全文进入 chapter_sources")

    if errors:
        raise ValidationFailure(errors)
    assert job_data is not None
    assert job_file is not None
    assert chapter_spine is not None
    assert draft_relative is not None
    assert draft_path is not None
    return ValidatedProject(
        root=root,
        config=config,
        config_file=config_file,
        blocked_paths=blocked_paths,
        global_canon=global_canon,
        review_principles=tuple(review_principles),
        architecture_version=global_version,
        approval_file=approval_file,
        job=job_data,
        job_file=job_file,
        chapter_spine=chapter_spine,
        chapter_sources=tuple(chapter_sources),
        previous_excerpt=previous_excerpt,
        recent_chapters=tuple(recent_chapters),
        draft_relative_path=draft_relative,
        draft_path=draft_path,
    )


def _atomic_write_bytes(path: Path, data: bytes, *, overwrite: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not overwrite and os.path.lexists(path):
        raise NovelForgeError(f"拒绝覆盖已有文件：{path}")

    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if not overwrite and os.path.lexists(path):
            raise NovelForgeError(f"拒绝覆盖并发创建的文件：{path}")
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _atomic_write_text(path: Path, text: str, *, overwrite: bool) -> None:
    _atomic_write_bytes(path, text.encode("utf-8"), overwrite=overwrite)


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def approve_project(
    project: os.PathLike[str] | str,
    confirmation: str,
) -> Path:
    if not isinstance(confirmation, str) or not confirmation.strip():
        raise NovelForgeError("approve 必须提供非空 --confirmation 文本；命令本身不能推断用户授权")
    validated = validate_project(project, require_approval=False)
    if validated.architecture_version is None:
        raise NovelForgeError("四份全局正本没有可批准的同一非空架构版本")

    record = {
        "schema_version": SCHEMA_VERSION,
        "architecture_version": validated.architecture_version,
        "approved_at": _utc_iso(),
        "confirmation": confirmation.strip(),
        "canon": {
            key: {
                "path": validated.global_canon[key].relative_path,
                "sha256": validated.global_canon[key].sha256,
            }
            for key in GLOBAL_CANON_KEYS
        },
    }
    target = validated.root / APPROVAL_NAME
    if os.path.lexists(target):
        try:
            resolved = target.resolve(strict=True)
        except (FileNotFoundError, OSError) as exc:
            raise NovelForgeError(f"已有架构批准记录无法安全解析：{target}（{exc}）") from exc
        if not _is_within(resolved, validated.root) or not resolved.is_file():
            raise NovelForgeError(f"架构批准记录不是项目内普通文件：{target}")
    _atomic_write_text(
        target,
        json.dumps(record, ensure_ascii=False, indent=2) + "\n",
        overwrite=True,
    )
    return target


def _ensure_internal_parent(root: Path, path: Path) -> Path:
    if not path.is_absolute():
        path = root / path
    absolute = Path(os.path.abspath(path))
    existing = absolute.parent
    missing_parts: list[str] = []
    while not existing.exists():
        if existing == existing.parent:
            raise NovelForgeError(f"无法定位输出目录的项目内父目录：{path}")
        missing_parts.append(existing.name)
        existing = existing.parent
    try:
        existing_resolved = existing.resolve(strict=True)
    except OSError as exc:
        raise NovelForgeError(f"输出目录父路径无法解析：{existing}（{exc}）") from exc
    canonical_parent = existing_resolved.joinpath(*reversed(missing_parts))
    canonical = canonical_parent / absolute.name
    if not _is_within(canonical, root) or canonical == root:
        raise NovelForgeError(f"输出目录经符号链接解析后越出项目：{path}")
    canonical_parent.mkdir(parents=True, exist_ok=True)
    parent_resolved = canonical_parent.resolve(strict=True)
    if not _is_within(parent_resolved, root):
        raise NovelForgeError(f"输出目录经符号链接解析后越出项目：{path}")
    return parent_resolved / absolute.name


def _selected_spine_text(spine: TextFile) -> str:
    sections = _markdown_h2_sections(spine.text)
    return "\n\n".join(sections[name][0] for name in WRITER_SPINE_SECTIONS).rstrip() + "\n"


def _excerpt_text(file: TextFile) -> str:
    assert file.start_line is not None and file.end_line is not None
    lines = file.text.splitlines(keepends=True)
    return "".join(lines[file.start_line - 1 : file.end_line])


def _material_block(title: str, file: TextFile, content: str | None = None) -> str:
    body = file.text if content is None else content
    range_text = ""
    if file.start_line is not None:
        range_text = f"（第 {file.start_line}-{file.end_line} 行）"
    if body and not body.endswith(("\n", "\r")):
        body += "\n"
    return (
        f"## {title}\n\n"
        f"来源：{file.relative_path}{range_text}\n\n"
        "--- NOVELFORGE SOURCE BEGIN ---\n"
        f"{body}"
        "--- NOVELFORGE SOURCE END ---"
    )


_CANON_TITLES = {
    "brief": "全局正本：项目简报",
    "book_spine": "全局正本：全书龙骨",
    "outline": "全局正本：剧情总纲",
    "style_canon": "全局正本：文风正本",
}


def _common_material_blocks(validated: ValidatedProject) -> list[str]:
    assert validated.chapter_spine is not None
    blocks = [
        _material_block(_CANON_TITLES[key], validated.global_canon[key]) for key in GLOBAL_CANON_KEYS
    ]
    blocks.append(
        _material_block(
            "章节 spine：故事相关章节",
            validated.chapter_spine,
            _selected_spine_text(validated.chapter_spine),
        )
    )
    for index, source in enumerate(validated.chapter_sources, 1):
        blocks.append(_material_block(f"本章显式来源 {index}", source))
    if validated.previous_excerpt is not None:
        blocks.append(
            _material_block(
                "上一章精确衔接片段",
                validated.previous_excerpt,
                _excerpt_text(validated.previous_excerpt),
            )
        )
    return blocks


def _render_writer_task(validated: ValidatedProject) -> str:
    assert validated.job is not None
    chapter = validated.job["chapter"]
    instruction = f"""# {chapter} 独立写作任务

你是本章全新启动的独立写作进程。只能使用本任务内显式提供的材料，不得搜索项目、读取其他文件或补造未给出的事实。

只向标准输出写章节标题与小说正文，不要附解释、自评或工作过程。若材料不足，停止写作，并让输出严格以 `NOVELFORGE_MISSING_CONTEXT:` 开头，随后列出最小缺口。
"""
    return instruction.rstrip() + "\n\n" + "\n\n".join(_common_material_blocks(validated)) + "\n"


def _render_reviewer_task(validated: ValidatedProject, draft: TextFile) -> str:
    assert validated.job is not None
    chapter = validated.job["chapter"]
    instruction = f"""# {chapter} 独立审稿任务

你是与写作者隔离的全新审稿进程。只依据本任务提供的正本快照、故事材料、正文、显式近章材料和审查原则判断；这里不包含写作者的推理或自评。

必须按以下顺序审查：

1. 先通读整章，再整章复述各主要人物的目的、阻力、选择与代价，并概括读者最可能记住的场面和变化。
2. 再与所提供的近章材料比较叙事功能、解法、冲突传播、关系变化载体和结尾压力，指出有文本证据的同构或差异。
3. 最后才审语言、节奏和自然度，并把修改建议落到具体场面。

禁止用关键词扫描、词频命中或物件计数代替整章判断。只输出审稿意见，不重写正文。
"""
    blocks = _common_material_blocks(validated)
    blocks.append(_material_block("待审正文", draft))
    for index, recent in enumerate(validated.recent_chapters, 1):
        blocks.append(_material_block(f"显式近章材料 {index}", recent))
    for index, principle in enumerate(validated.review_principles, 1):
        blocks.append(_material_block(f"审查原则 {index}", principle))
    return instruction.rstrip() + "\n\n" + "\n\n".join(blocks) + "\n"


def _all_locked_sources(validated: ValidatedProject) -> list[TextFile]:
    assert validated.job_file is not None
    assert validated.chapter_spine is not None
    assert validated.approval_file is not None
    files = [validated.config_file, validated.approval_file, validated.job_file]
    files.extend(validated.global_canon[key] for key in GLOBAL_CANON_KEYS)
    files.append(validated.chapter_spine)
    files.extend(validated.chapter_sources)
    if validated.previous_excerpt is not None:
        files.append(validated.previous_excerpt)
    files.extend(validated.recent_chapters)
    files.extend(validated.review_principles)
    return files


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def _manifest(validated: ValidatedProject, created_at: str, writer_task: str) -> dict[str, Any]:
    assert validated.job is not None
    assert validated.job_file is not None
    assert validated.draft_relative_path is not None
    sources = [file.manifest_entry() for file in _all_locked_sources(validated)]
    return {
        "schema_version": SCHEMA_VERSION,
        "chapter": validated.job["chapter"],
        "created_at_utc": created_at,
        "job_path": validated.job_file.relative_path,
        "draft_path": validated.draft_relative_path,
        "sources": sources,
        "state": "prepared",
        "state_history": [{"state": "prepared", "at": _utc_iso()}],
        "writer_task": {
            "path": "writer-task.md",
            "sha256": hashlib.sha256(writer_task.encode("utf-8")).hexdigest(),
        },
    }


def _resolve_new_run_path(root: Path, output: os.PathLike[str] | str | None, name: str) -> Path:
    if output is None:
        run_path = root / ".novelforge" / "runs" / name
    else:
        value = Path(output).expanduser()
        run_path = value if value.is_absolute() or value.drive else root / value
    run_path = _ensure_internal_parent(root, Path(os.path.abspath(run_path)))
    if os.path.lexists(run_path):
        raise NovelForgeError(f"run 目录已存在，拒绝覆盖：{run_path}")
    try:
        run_path.mkdir()
    except OSError as exc:
        raise NovelForgeError(f"无法创建 run 目录：{run_path}（{exc}）") from exc
    resolved = run_path.resolve(strict=True)
    if not _is_within(resolved, root):
        raise NovelForgeError(f"run 目录经符号链接解析后越出项目：{run_path}")
    return resolved


def prepare_project(
    project: os.PathLike[str] | str,
    job: os.PathLike[str] | str,
    output: os.PathLike[str] | str | None = None,
) -> Path:
    validated = validate_project(project, job)
    writer_task = _render_writer_task(validated)
    created_at = _utc_timestamp()
    fingerprint = hashlib.sha256(
        json.dumps(
            [file.manifest_entry() for file in _all_locked_sources(validated)],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()[:12]
    run_name = f"{validated.job['chapter']}-{created_at}-{fingerprint}"
    run_path = _resolve_new_run_path(validated.root, output, run_name)

    manifest = _manifest(validated, created_at, writer_task)
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    try:
        _atomic_write_text(run_path / "writer-task.md", writer_task, overwrite=False)
        _atomic_write_text(run_path / "manifest.json", manifest_text, overwrite=False)
    except Exception:
        shutil.rmtree(run_path, ignore_errors=True)
        raise
    return run_path


def _resolve_existing_run(root: Path, run: os.PathLike[str] | str) -> Path:
    value = Path(run).expanduser()
    candidate = value if value.is_absolute() or value.drive else root / value
    try:
        resolved = candidate.resolve(strict=True)
    except (FileNotFoundError, OSError) as exc:
        raise NovelForgeError(f"run 目录不存在或无法解析：{candidate}（{exc}）") from exc
    if not _is_within(resolved, root) or resolved == root:
        raise NovelForgeError(f"run 目录必须位于项目内：{candidate}")
    if not resolved.is_dir():
        raise NovelForgeError(f"run 路径不是目录：{resolved}")
    return resolved


def _read_run_json(root: Path, run_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    manifest_path = run_path / "manifest.json"
    try:
        resolved = manifest_path.resolve(strict=True)
    except (FileNotFoundError, OSError) as exc:
        raise NovelForgeError(f"run 缺少可读 manifest.json：{exc}") from exc
    if not _is_within(resolved, root) or not resolved.is_file():
        raise NovelForgeError("run/manifest.json 经解析后不是项目内普通文件")
    try:
        raw = resolved.read_bytes()
    except OSError as exc:
        raise NovelForgeError(f"无法读取 run/manifest.json：{exc}") from exc
    text = _decode_utf8(raw, "run/manifest.json", errors)
    if text is None:
        raise ValidationFailure(errors, "manifest 校验失败")
    pseudo = TextFile("manifest", "manifest.json", resolved, raw, text, ("control",))
    manifest = _parse_json_file(pseudo, "run/manifest.json", errors)
    if manifest is None:
        raise ValidationFailure(errors, "manifest 校验失败")
    _check_schema(manifest, "run/manifest.json", errors)
    if errors:
        raise ValidationFailure(errors, "manifest 校验失败")
    return manifest


def _write_run_manifest(run_path: Path, manifest: dict[str, Any]) -> None:
    _atomic_write_text(
        run_path / "manifest.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        overwrite=True,
    )


def _set_run_state(
    run_path: Path,
    manifest: dict[str, Any],
    state: str,
    *,
    artifact_name: str | None = None,
    artifact_text: str | None = None,
) -> None:
    if state not in RUN_STATES:
        raise NovelForgeError(f"非法 run 状态：{state}")
    current = manifest.get("state")
    if current not in RUN_TRANSITIONS or state not in RUN_TRANSITIONS[current]:
        raise NovelForgeError(f"非法 run 状态转换：{current!r} -> {state!r}")
    history = manifest.setdefault("state_history", [])
    if not isinstance(history, list):
        raise NovelForgeError("manifest.state_history 已损坏")
    manifest["state"] = state
    history.append({"state": state, "at": _utc_iso()})
    if artifact_name is not None:
        assert artifact_text is not None
        manifest[artifact_name] = {
            "path": f"{artifact_name.replace('_', '-')}.md",
            "sha256": hashlib.sha256(artifact_text.encode("utf-8")).hexdigest(),
        }
    _write_run_manifest(run_path, manifest)


def _validate_manifest_shape(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    errors: list[str] = []
    if not isinstance(manifest.get("chapter"), str) or not manifest["chapter"]:
        errors.append("manifest.chapter 必须是非空字符串")
    if not isinstance(manifest.get("job_path"), str):
        errors.append("manifest.job_path 必须是相对路径字符串")
    if not isinstance(manifest.get("draft_path"), str):
        errors.append("manifest.draft_path 必须是相对路径字符串")
    if manifest.get("state") not in RUN_STATES:
        errors.append(f"manifest.state 非法：{manifest.get('state')!r}")
    history = manifest.get("state_history")
    if not isinstance(history, list) or not history:
        errors.append("manifest.state_history 必须是非空数组")
    elif any(
        not isinstance(item, dict)
        or item.get("state") not in RUN_STATES
        or not isinstance(item.get("at"), str)
        or not item["at"].strip()
        for item in history
    ):
        errors.append("manifest.state_history 含有非法状态记录")
    elif history[-1]["state"] != manifest.get("state"):
        errors.append("manifest.state 与 state_history 最后一项不一致")
    elif history[0].get("state") != "prepared":
        errors.append("manifest.state_history 必须从 prepared 开始")
    else:
        for previous, current in zip(history, history[1:]):
            if current["state"] not in RUN_TRANSITIONS.get(previous["state"], set()):
                errors.append(
                    f"manifest.state_history 含有非法转换：{previous['state']} -> {current['state']}"
                )
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        errors.append("manifest.sources 必须是数组")
        sources = []
    valid_sources: list[dict[str, Any]] = []
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"manifest.sources[{index}] 必须是对象")
            continue
        role = source.get("role")
        path = source.get("path")
        digest = source.get("sha256")
        stages = source.get("stages")
        if role not in ALLOWED_MANIFEST_ROLES:
            errors.append(f"manifest.sources[{index}].role 非法：{role!r}")
        if not isinstance(path, str) or not path:
            errors.append(f"manifest.sources[{index}].path 必须是非空字符串")
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            errors.append(f"manifest.sources[{index}].sha256 格式非法")
        if not isinstance(stages, list) or not all(isinstance(stage, str) for stage in stages):
            errors.append(f"manifest.sources[{index}].stages 必须是字符串数组")
        start_line = source.get("start_line")
        end_line = source.get("end_line")
        if (start_line is None) != (end_line is None):
            errors.append(f"manifest.sources[{index}] 的行区间不完整")
        elif start_line is not None and (
            type(start_line) is not int
            or type(end_line) is not int
            or start_line < 1
            or end_line < start_line
        ):
            errors.append(f"manifest.sources[{index}] 的行区间非法")
        valid_sources.append(source)
    if errors:
        raise ValidationFailure(errors, "manifest 校验失败")
    return valid_sources


def _source_identity(source: dict[str, Any]) -> tuple[Any, ...]:
    return (
        source["role"],
        source["path"],
        source.get("start_line"),
        source.get("end_line"),
    )


def _verify_locked_inputs(root: Path, manifest: dict[str, Any]) -> None:
    sources = _validate_manifest_shape(manifest)
    config, _, blocked_paths = _load_config_only(root)
    del config
    errors: list[str] = []

    for index, source in enumerate(sources):
        role = source["role"]
        if role == "novelforge_config":
            if source["path"] != CONFIG_NAME:
                errors.append(f"manifest.sources[{index}] 的配置路径必须是 {CONFIG_NAME}")
                continue
            file = _read_fixed_file(root, CONFIG_NAME, "锁定配置", errors)
        else:
            file = _read_input_file(
                root,
                source["path"],
                f"锁定输入 {role}",
                role,
                tuple(source["stages"]),
                blocked_paths,
                errors,
                start_line=source.get("start_line"),
                end_line=source.get("end_line"),
            )
        if file is not None and file.sha256 != source["sha256"]:
            errors.append(
                f"{role} 的 sha256 已变化：{source['path']}（锁定 {source['sha256']}，当前 {file.sha256}）"
            )
    if errors:
        raise ValidationFailure(errors, "锁定输入核验失败")


def _compare_manifest_to_validation(manifest: dict[str, Any], validated: ValidatedProject) -> None:
    assert validated.job is not None
    assert validated.job_file is not None
    assert validated.draft_relative_path is not None
    errors: list[str] = []
    expected = Counter(_source_identity(file.manifest_entry()) for file in _all_locked_sources(validated))
    actual = Counter(_source_identity(source) for source in manifest["sources"])
    if actual != expected:
        errors.append("manifest.sources 与当前锁定的配置/章节任务白名单不一致")
    if manifest["job_path"] != validated.job_file.relative_path:
        errors.append("manifest.job_path 与章节任务路径不一致")
    if manifest["draft_path"] != validated.draft_relative_path:
        errors.append("manifest.draft_path 与章节任务 draft 不一致")
    if manifest["chapter"] != validated.job["chapter"]:
        errors.append("manifest.chapter 与章节任务 chapter 不一致")
    if errors:
        raise ValidationFailure(errors, "manifest 校验失败")


def _read_existing_draft(validated: ValidatedProject) -> TextFile:
    assert validated.draft_path is not None
    assert validated.draft_relative_path is not None
    if not validated.draft_path.exists():
        raise NovelForgeError(f"待审正文不存在：{validated.draft_relative_path}")
    try:
        resolved = validated.draft_path.resolve(strict=True)
        raw = resolved.read_bytes()
    except (FileNotFoundError, OSError) as exc:
        raise NovelForgeError(f"待审正文无法读取：{validated.draft_relative_path}（{exc}）") from exc
    errors: list[str] = []
    text = _decode_utf8(raw, "待审正文", errors)
    if text is None:
        raise ValidationFailure(errors)
    if not text.strip():
        raise NovelForgeError(f"待审正文为空：{validated.draft_relative_path}")
    return TextFile(
        role="draft",
        relative_path=validated.draft_relative_path,
        absolute_path=resolved,
        raw=raw,
        text=text,
        stages=("reviewer",),
    )


def prepare_review(project: os.PathLike[str] | str, run: os.PathLike[str] | str) -> Path:
    root = _project_root(project)
    run_path = _resolve_existing_run(root, run)
    manifest = _read_run_json(root, run_path)
    _verify_locked_inputs(root, manifest)
    if manifest.get("state") not in {"prepared", "drafted"}:
        raise NovelForgeError(
            f"当前 run 状态不能准备审稿：{manifest.get('state')!r}；请重新 prepare 本章"
        )
    validated = validate_project(root, manifest["job_path"])
    _compare_manifest_to_validation(manifest, validated)
    draft = _read_existing_draft(validated)
    reviewer_task = _render_reviewer_task(validated, draft)
    output = run_path / "reviewer-task.md"
    _atomic_write_text(output, reviewer_task, overwrite=False)
    manifest["review_draft"] = {
        "path": draft.relative_path,
        "sha256": draft.sha256,
    }
    _set_run_state(
        run_path,
        manifest,
        "review_prepared",
        artifact_name="reviewer_task",
        artifact_text=reviewer_task,
    )
    return output


def _read_task_file(
    root: Path,
    run_path: Path,
    name: str,
    expected_sha256: str | None,
) -> str:
    path = run_path / name
    try:
        resolved = path.resolve(strict=True)
    except (FileNotFoundError, OSError) as exc:
        raise NovelForgeError(f"run 缺少 {name}：{exc}") from exc
    if not _is_within(resolved, root) or not resolved.is_file():
        raise NovelForgeError(f"run/{name} 经解析后不是项目内普通文件")
    try:
        raw = resolved.read_bytes()
    except OSError as exc:
        raise NovelForgeError(f"无法读取 run/{name}：{exc}") from exc
    errors: list[str] = []
    text = _decode_utf8(raw, f"run/{name}", errors)
    if text is None:
        raise ValidationFailure(errors)
    if not text.strip():
        raise NovelForgeError(f"run/{name} 为空")
    digest = hashlib.sha256(raw).hexdigest()
    if expected_sha256 is None or digest != expected_sha256:
        raise NovelForgeError(
            f"run/{name} 的 sha256 与 manifest 不一致：锁定 {expected_sha256 or '空'}，当前 {digest}"
        )
    return text


_CHILD_ENVIRONMENT_KEYS = (
    "PATH",
    "PATHEXT",
    "SYSTEMROOT",
    "WINDIR",
    "COMSPEC",
    "TEMP",
    "TMP",
    "HOME",
    "USERPROFILE",
    "HOMEDRIVE",
    "HOMEPATH",
    "APPDATA",
    "LOCALAPPDATA",
    "PROGRAMDATA",
    "LANG",
    "LC_ALL",
    "TZ",
    "SSL_CERT_FILE",
    "SSL_CERT_DIR",
)


def _minimal_child_environment() -> dict[str, str]:
    environment = {key: os.environ[key] for key in _CHILD_ENVIRONMENT_KEYS if key in os.environ}
    environment["PYTHONIOENCODING"] = "utf-8"
    environment["PYTHONUTF8"] = "1"
    return environment


def _run_command(
    root: Path,
    command: Sequence[str],
    task: str,
    timeout: float | None,
) -> subprocess.CompletedProcess[str]:
    if not command:
        raise NovelForgeError("invoke 缺少 COMMAND")
    if any(not isinstance(part, str) or not part for part in command):
        raise NovelForgeError("COMMAND 的每个参数都必须是非空字符串")
    executable = shutil.which(command[0]) or command[0]
    executable_name = Path(executable).name.casefold()
    if Path(executable).suffix.casefold() in {".cmd", ".bat"} or executable_name in {
        "cmd",
        "cmd.exe",
        "command.com",
        "powershell",
        "powershell.exe",
        "pwsh",
        "pwsh.exe",
        "sh",
        "bash",
        "zsh",
        "fish",
    }:
        raise NovelForgeError(
            "invoke 只接受直接可执行程序，不接受批处理文件或命令解释器；"
            "请使用不经 shell 的原生包装器"
        )
    try:
        return subprocess.run(
            list(command),
            input=task,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            cwd=root,
            env=_minimal_child_environment(),
            encoding="utf-8",
            errors="strict",
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise NovelForgeError(f"独立进程超过 timeout={timeout:g} 秒，已终止且未写入阶段输出") from exc
    except FileNotFoundError as exc:
        raise NovelForgeError(f"无法启动命令：{command[0]!r}") from exc
    except (OSError, UnicodeError) as exc:
        raise NovelForgeError(f"独立进程启动或 UTF-8 通信失败：{exc}") from exc


def invoke_stage(
    project: os.PathLike[str] | str,
    run: os.PathLike[str] | str,
    stage: str,
    command: Sequence[str],
    *,
    overwrite: bool = False,
    timeout: float | None = None,
) -> Path:
    if stage not in {"writer", "reviewer"}:
        raise NovelForgeError("stage 必须是 writer 或 reviewer")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0):
        raise NovelForgeError("timeout 必须是大于 0 的秒数")
    root = _project_root(project)
    run_path = _resolve_existing_run(root, run)
    manifest = _read_run_json(root, run_path)
    _validate_manifest_shape(manifest)
    _verify_locked_inputs(root, manifest)
    validated = validate_project(root, manifest["job_path"])
    _compare_manifest_to_validation(manifest, validated)

    artifact_key = "writer_task" if stage == "writer" else "reviewer_task"
    artifact = manifest.get(artifact_key)
    if not isinstance(artifact, dict):
        raise NovelForgeError(f"manifest 缺少 {artifact_key} 锁定记录")
    expected_name = "writer-task.md" if stage == "writer" else "reviewer-task.md"
    if artifact.get("path") != expected_name:
        raise NovelForgeError(f"manifest.{artifact_key}.path 必须是 {expected_name}")
    expected_digest = artifact.get("sha256")
    if not isinstance(expected_digest, str) or re.fullmatch(r"[0-9a-f]{64}", expected_digest) is None:
        raise NovelForgeError(f"manifest.{artifact_key}.sha256 格式非法")

    if stage == "writer":
        if manifest.get("state") not in {"prepared", "missing_context", "drafted"}:
            raise NovelForgeError(
                f"当前 run 状态不能再次写作：{manifest.get('state')!r}；请重新 prepare 本章"
            )
        task = _read_task_file(root, run_path, "writer-task.md", expected_digest)
        expected_task = _render_writer_task(validated)
        if task != expected_task:
            raise NovelForgeError("writer-task.md 不是由当前已批准 job 和锁定来源派生")
        assert validated.draft_path is not None
        output = validated.draft_path
    else:
        if manifest.get("state") not in {"review_prepared", "reviewed"}:
            raise NovelForgeError(
                f"当前 run 状态不能执行审稿：{manifest.get('state')!r}；请先 prepare-review"
            )
        task = _read_task_file(root, run_path, "reviewer-task.md", expected_digest)
        draft = _read_existing_draft(validated)
        review_draft = manifest.get("review_draft")
        if not isinstance(review_draft, dict):
            raise NovelForgeError("manifest 缺少 prepare-review 锁定的 review_draft")
        if review_draft.get("path") != draft.relative_path or review_draft.get("sha256") != draft.sha256:
            raise NovelForgeError("待审正文已在 prepare-review 后变化；请重新 prepare 本章")
        expected_task = _render_reviewer_task(validated, draft)
        if task != expected_task:
            raise NovelForgeError("reviewer-task.md 不是由当前锁定正本和正文派生")
        output = run_path / "review.md"

    if not overwrite and os.path.lexists(output):
        target = "正文" if stage == "writer" else "审稿结果"
        raise NovelForgeError(f"{target}已存在，拒绝覆盖：{output}")

    result = _run_command(root, command, task, timeout)
    stdout = result.stdout
    marker_view = stdout.lstrip("\ufeff")
    if stage == "writer" and marker_view.startswith("NOVELFORGE_MISSING_CONTEXT:"):
        missing_path = run_path / "missing-context.md"
        _atomic_write_text(missing_path, stdout, overwrite=True)
        _set_run_state(run_path, manifest, "missing_context")
        raise NovelForgeError(f"写作进程报告资料缺口，正文未写入：{missing_path}")

    if result.returncode != 0:
        stderr = result.stderr.strip()
        detail = f"；stderr：{stderr[:4000]}" if stderr else ""
        raise NovelForgeError(f"独立进程退出码为 {result.returncode}{detail}")
    if not stdout.strip():
        raise NovelForgeError("独立进程输出为空，未写入任何文件")

    _atomic_write_text(output, stdout, overwrite=overwrite)
    _set_run_state(run_path, manifest, "drafted" if stage == "writer" else "reviewed")
    return output


def _copy_tree_atomic(source: Path, target: Path, skipped_root_names: set[str]) -> None:
    for current, directories, files in os.walk(source, followlinks=False):
        current_path = Path(current)
        for directory in list(directories):
            if (current_path / directory).is_symlink():
                raise NovelForgeError(f"模板包含符号链接目录，拒绝复制：{current_path / directory}")
        relative_dir = current_path.relative_to(source)
        (target / relative_dir).mkdir(parents=True, exist_ok=True)
        for name in files:
            source_file = current_path / name
            if source_file.is_symlink():
                raise NovelForgeError(f"模板包含符号链接文件，拒绝复制：{source_file}")
            relative_file = source_file.relative_to(source)
            if len(relative_file.parts) == 1 and name in skipped_root_names:
                continue
            _atomic_write_bytes(target / relative_file, source_file.read_bytes(), overwrite=False)


def init_project(
    target: os.PathLike[str] | str,
    *,
    repository_root: os.PathLike[str] | str | None = None,
) -> Path:
    source_root = (
        Path(repository_root).resolve(strict=True)
        if repository_root is not None
        else Path(__file__).resolve().parents[1]
    )
    template = source_root / "templates" / "novel-project"
    root_files = (
        "AGENTS.md",
        "Claude.md",
        "AIGC_DETECTION_PRINCIPLES.md",
        "NOVEL_REVIEW_PROTOCOL.md",
    )
    missing = [str(path) for path in (template, *(source_root / name for name in root_files)) if not path.exists()]
    if missing:
        raise NovelForgeError("init 所需源文件缺失：" + "，".join(missing))
    if not template.is_dir():
        raise NovelForgeError(f"空项目模板不是目录：{template}")

    destination = Path(target).expanduser()
    destination_absolute = Path(os.path.abspath(destination))
    if _is_within(destination_absolute, template.resolve(strict=True)):
        raise NovelForgeError("TARGET 不能位于源模板目录内")
    if destination.exists():
        if not destination.is_dir():
            raise NovelForgeError(f"TARGET 已存在且不是目录：{destination}")
        try:
            nonempty = next(destination.iterdir(), None) is not None
        except OSError as exc:
            raise NovelForgeError(f"无法检查 TARGET：{destination}（{exc}）") from exc
        if nonempty:
            raise NovelForgeError(f"TARGET 已存在且非空，拒绝覆盖：{destination}")
    else:
        destination.mkdir(parents=True)
    destination = destination.resolve(strict=True)

    _copy_tree_atomic(template, destination, set(root_files))
    for name in root_files:
        _atomic_write_bytes(destination / name, (source_root / name).read_bytes(), overwrite=False)
    return destination
