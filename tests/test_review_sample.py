from __future__ import annotations

from copy import deepcopy
import unittest

from examples.review_python import buggy, fixed


def make_tasks() -> list[dict]:
    return [
        {"id": 3, "title": "検証", "done": False},
        {"id": 1, "title": "調査", "done": False},
        {"id": 4, "title": "完了", "done": True},
        {"id": 2, "title": "実装", "done": False},
    ]


class SelectionContract:
    """両実装に同じ期待値を適用する振る舞いテスト。"""

    def test_empty_input(self) -> None:
        self.assertEqual(self.select([]), [])

    def test_no_match(self) -> None:
        self.assertEqual(self.select([make_tasks()[2]]), [])

    def test_input_is_unchanged(self) -> None:
        tasks = make_tasks()
        before = deepcopy(tasks)
        self.select(tasks)
        self.assertEqual(tasks, before)

    def test_limit_boundaries(self) -> None:
        for limit in (0, 1, 2, 3, 10):
            with self.subTest(limit=limit):
                result = self.select(make_tasks(), limit=limit)
                self.assertEqual([task["id"] for task in result], [1, 2, 3][:limit])

    def test_done_filter_and_new_list(self) -> None:
        tasks = make_tasks()
        result = self.select(tasks, done=True)
        self.assertEqual([task["id"] for task in result], [4])
        self.assertIsNot(result, tasks)

    def test_negative_limit(self) -> None:
        with self.assertRaises(ValueError):
            self.select(make_tasks(), limit=-1)


class FixedSelectionTests(SelectionContract, unittest.TestCase):
    select = staticmethod(fixed.select_tasks)


class BuggySelectionTests(SelectionContract, unittest.TestCase):
    select = staticmethod(buggy.select_tasks)

    @unittest.expectedFailure
    def test_empty_input(self) -> None:
        super().test_empty_input()

    @unittest.expectedFailure
    def test_no_match(self) -> None:
        super().test_no_match()

    @unittest.expectedFailure
    def test_input_is_unchanged(self) -> None:
        super().test_input_is_unchanged()

    @unittest.expectedFailure
    def test_limit_boundaries(self) -> None:
        super().test_limit_boundaries()


if __name__ == "__main__":
    unittest.main()
