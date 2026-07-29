from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from learning_tasks.core import TaskStore


class TaskStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "tasks.json"
        self.store = TaskStore(self.path)

    def test_missing_file_has_no_tasks(self) -> None:
        self.assertEqual(self.store.list_tasks(), [])

    def test_add_assigns_ids_and_trims_title(self) -> None:
        first = self.store.add("  指示ファイルを読む  ")
        second = self.store.add("テストする")
        self.assertEqual((first.id, first.title), (1, "指示ファイルを読む"))
        self.assertEqual(second.id, 2)
        self.assertEqual(self.store.list_tasks(), [first, second])

    def test_add_rejects_empty_title(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            self.store.add("   ")

    def test_complete_updates_only_selected_task(self) -> None:
        first = self.store.add("計画する")
        second = self.store.add("実装する")
        self.assertTrue(self.store.complete(first.id).done)
        tasks = self.store.list_tasks()
        self.assertTrue(tasks[0].done)
        self.assertFalse(tasks[1].done)
        self.assertEqual(tasks[1].title, second.title)

    def test_complete_rejects_unknown_id(self) -> None:
        with self.assertRaisesRegex(ValueError, "task 99 was not found"):
            self.store.complete(99)

    def test_old_record_without_done_field_is_supported(self) -> None:
        self.path.write_text(
            json.dumps([{"id": 1, "title": "古いタスク"}]), encoding="utf-8"
        )
        self.assertFalse(self.store.list_tasks()[0].done)

    def test_invalid_json_is_reported(self) -> None:
        self.path.write_text("{", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "could not read task file"):
            self.store.list_tasks()


if __name__ == "__main__":
    unittest.main()
