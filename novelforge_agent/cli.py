from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .core import (
    NovelForgeError,
    ValidationFailure,
    approve_project,
    init_project,
    invoke_stage,
    prepare_project,
    prepare_review,
    validate_project,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="novelforge",
        description="以显式输入白名单隔离章节写作与审稿进程。",
    )
    commands = parser.add_subparsers(dest="subcommand", required=True)

    init_parser = commands.add_parser("init", help="从仓库空模板初始化小说项目")
    init_parser.add_argument("target", metavar="TARGET", help="必须为空或尚不存在的目标目录")

    validate_parser = commands.add_parser("validate", help="校验项目配置、架构闸门和章节任务")
    validate_parser.add_argument("project", metavar="PROJECT")
    validate_parser.add_argument("--job", metavar="JOB", help="项目内章节任务 JSON")

    approve_parser = commands.add_parser("approve", help="在用户明确批准后锁定四份全局正本")
    approve_parser.add_argument("project", metavar="PROJECT")
    approve_parser.add_argument(
        "--confirmation",
        required=True,
        metavar="TEXT",
        help="用户明确批准的非空文本依据；CLI 不会自行推断授权",
    )

    prepare_parser = commands.add_parser("prepare", help="生成锁定 manifest 与独立写作任务")
    prepare_parser.add_argument("project", metavar="PROJECT")
    prepare_parser.add_argument("--job", metavar="JOB", required=True, help="项目内章节任务 JSON")
    prepare_parser.add_argument("--output", metavar="DIR", help="项目内、尚不存在的 run 目录")

    review_parser = commands.add_parser("prepare-review", help="核对锁定输入并生成独立审稿任务")
    review_parser.add_argument("project", metavar="PROJECT")
    review_parser.add_argument("--run", metavar="RUN", required=True, help="项目内 run 目录")

    invoke_parser = commands.add_parser(
        "invoke",
        help="用任务文本的 stdin 启动独立新进程",
        description=(
            "用 shell=False 启动独立新进程。此处的进程隔离不构成文件系统或网络沙箱，"
            "COMMAND 仍拥有其操作系统账户本来的权限。"
        ),
    )
    invoke_parser.add_argument("project", metavar="PROJECT")
    invoke_parser.add_argument("--run", metavar="RUN", required=True, help="项目内 run 目录")
    invoke_parser.add_argument("--stage", choices=("writer", "reviewer"), required=True)
    invoke_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="显式允许覆盖该阶段已有输出；正文默认拒绝覆盖",
    )
    invoke_parser.add_argument(
        "--timeout",
        type=float,
        metavar="SECONDS",
        help="大于 0 的进程超时秒数；超时后终止且不写入阶段输出",
    )
    invoke_parser.add_argument(
        "command",
        metavar="COMMAND",
        nargs="+",
        help="在 -- 之后提供可执行程序及参数",
    )
    return parser


def _configure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def main(argv: Sequence[str] | None = None) -> int:
    _configure_utf8_output()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.subcommand == "init":
            target = init_project(args.target)
            print(f"项目已初始化：{target}")
        elif args.subcommand == "validate":
            result = validate_project(args.project, args.job)
            suffix = f"；章节任务 {result.job_file.relative_path}" if result.job_file else ""
            print(f"验证通过：{result.root}{suffix}")
        elif args.subcommand == "approve":
            approval = approve_project(args.project, args.confirmation)
            print(f"架构批准记录已更新：{approval}")
        elif args.subcommand == "prepare":
            run = prepare_project(args.project, args.job, args.output)
            print(f"写作 run 已创建：{run}")
        elif args.subcommand == "prepare-review":
            task = prepare_review(args.project, args.run)
            print(f"审稿任务已创建：{task}")
        elif args.subcommand == "invoke":
            command = list(args.command)
            if command and command[0] == "--":
                command = command[1:]
            output = invoke_stage(
                args.project,
                args.run,
                args.stage,
                command,
                overwrite=args.overwrite,
                timeout=args.timeout,
            )
            print(f"{args.stage} 输出已写入：{output}")
        else:
            parser.error("未知命令")
    except ValidationFailure as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except NovelForgeError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
