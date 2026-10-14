"""仕様に従う修正版。"""

from __future__ import annotations


def select_tasks(
    tasks: list[dict], *, done: bool = False, limit: int = 10
) -> list[dict]:
    if limit < 0:
        raise ValueError("limit must not be negative")
    matches = sorted(
        (task for task in tasks if task["done"] == done),
        key=lambda task: task["id"],
    )
    return matches[:limit]
