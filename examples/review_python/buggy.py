"""レビュー演習用の実装。仕様はspec.mdを参照。"""

from __future__ import annotations


def select_tasks(
    tasks: list[dict], *, done: bool = False, limit: int = 10
) -> list[dict]:
    if limit < 0:
        raise ValueError("limit must not be negative")
    tasks.sort(key=lambda task: task["id"])
    matches = [task for task in tasks if task["done"] == done]
    first = matches[0]
    return [first, *matches[1 : limit + 1]]
