# 答え合わせ用のレビュー例

レビューを終えてから読んでください。重要度はいずれも、この小さな教材での影響を前提にP2としています。

## 対象と前提

対象は `buggy.py` の `select_tasks`、仕様は `spec.md`。入力の型・フィールドは仕様を満たす前提です。

## 指摘

### [P2] 入力リストの順序が変わる

- 場所：`examples/review_python/buggy.py:11`、`select_tasks`
- 発生条件：入力がID昇順でない。
- 影響：呼び出し元が保持しているリストの並び順を変え、入力不変の契約に反する。
- 根拠：`tasks.sort(...)` は元のリストを直接更新する。
- 再現：ID `[2, 1]` の入力が、呼び出し後に `[1, 2]` になる（実行済み）。
- 改善案：`sorted` で新しいリストを作る。

### [P2] 空入力・一致なしで例外になる

- 場所：`examples/review_python/buggy.py:13`、`select_tasks`
- 発生条件：空入力、または指定の `done` と一致するタスクがない。
- 影響：空リストを返す契約に反し、`IndexError` で停止する。
- 根拠：空になり得る `matches` の先頭要素を無条件に取得している。
- 再現：`select_tasks([])` と完了済みタスクだけの入力で `IndexError`（実行済み）。
- 改善案：先頭要素の個別取得をなくし、空リストにも適用できるスライスを使う。

### [P2] 指定した最大件数を超える

- 場所：`examples/review_python/buggy.py:14`、`select_tasks`
- 発生条件：一致するタスクがあり、`limit=0`、または一致件数が正の `limit` を超える。
- 影響：0件指定で1件、1件指定で最大2件を返す。
- 根拠：先頭の1件に最大 `limit` 件を足している。
- 再現：一致2件に `limit=0` で1件、`limit=1` で2件（実行済み）。
- 改善案：返却全体を `matches[:limit]` で制限する。

## 再現コマンド

リポジトリルートで実行します。ファイルの書き込みは行いません。

```bash
python3 -B - <<'PY'
from examples.review_python.buggy import select_tasks

tasks = [
    {"id": 2, "title": "実装", "done": False},
    {"id": 1, "title": "調査", "done": False},
]
select_tasks(tasks)
print("呼び出し後の入力:", [task["id"] for task in tasks])
for label, items in (
    ("空入力", []),
    ("一致なし", [{"id": 1, "title": "完了", "done": True}]),
):
    try:
        select_tasks(items)
    except IndexError as exc:
        print(label, type(exc).__name__)
for limit in (0, 1):
    print("limit:", limit, "実際の件数:", len(select_tasks(tasks, limit=limit)))
PY
```

## 質問・検証と残るリスク

仕様の曖昧さに関する質問はありません。再現コマンドと共通仕様テストで3種類の欠陥を確認しました。
修正版では同じ指摘が解消しています。仕様外の不正な型、並行実行、実運用のデータ量は評価していません。
これらの指摘が出ることだけで、あらゆるコードへのレビュー品質を保証するものではありません。
