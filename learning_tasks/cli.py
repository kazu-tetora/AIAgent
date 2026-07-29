"""Command-line interface for the learning task manager."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .core import TaskStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="学習タスクを管理します")
    parser.add_argument("--file", type=Path, default=Path(".learning-tasks.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="タスクを追加")
    add.add_argument("title")
    commands.add_parser("list", help="タスクを一覧表示")
    complete = commands.add_parser("complete", help="タスクを完了")
    complete.add_argument("id", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = TaskStore(args.file)
    try:
        if args.command == "add":
            task = store.add(args.title)
            print(f"追加: {task.id} {task.title}")
        elif args.command == "list":
            for task in store.list_tasks():
                print(f"[{'x' if task.done else ' '}] {task.id}: {task.title}")
        elif args.command == "complete":
            task = store.complete(args.id)
            print(f"完了: {task.id} {task.title}")
    except ValueError as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

