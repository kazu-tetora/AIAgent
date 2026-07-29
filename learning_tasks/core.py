"""Core task operations and JSON persistence."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    done: bool = False

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Task":
        task_id = value.get("id")
        title = value.get("title")
        done = value.get("done", False)
        if not isinstance(task_id, int) or isinstance(task_id, bool):
            raise ValueError("task id must be an integer")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("task title must be a non-empty string")
        if not isinstance(done, bool):
            raise ValueError("task done must be a boolean")
        return cls(id=task_id, title=title, done=done)


class TaskStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list_tasks(self) -> list[Task]:
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"could not read task file: {exc}") from exc
        if not isinstance(raw, list):
            raise ValueError("task file must contain a JSON array")
        if not all(isinstance(item, dict) for item in raw):
            raise ValueError("each task must be a JSON object")
        return [Task.from_dict(item) for item in raw]

    def add(self, title: str) -> Task:
        normalized = title.strip()
        if not normalized:
            raise ValueError("title must not be empty")
        tasks = self.list_tasks()
        task = Task(max((item.id for item in tasks), default=0) + 1, normalized)
        self._save([*tasks, task])
        return task

    def complete(self, task_id: int) -> Task:
        tasks = self.list_tasks()
        completed: Task | None = None
        updated: list[Task] = []
        for task in tasks:
            if task.id == task_id:
                completed = Task(task.id, task.title, True)
                updated.append(completed)
            else:
                updated.append(task)
        if completed is None:
            raise ValueError(f"task {task_id} was not found")
        self._save(updated)
        return completed

    def _save(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps([asdict(task) for task in tasks], ensure_ascii=False, indent=2)
            + "\n",
            encoding="utf-8",
        )

