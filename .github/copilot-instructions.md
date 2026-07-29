# Copilot repository instructions

このリポジトリは AI エージェントの指示設計を学ぶ Python 教材です。

## 実装

- Python 3.10 以上と標準ライブラリだけを使う。
- ドメイン処理は `learning_tasks/core.py`、CLI 表示は `learning_tasks/cli.py` に置く。
- 公開関数には型ヒントを付ける。
- JSON フィールド `id`、`title`、`done` を互換性なく変更しない。
- 例外を握りつぶさず、利用者が修正できる短いメッセージにする。

## テストと回答

- 振る舞いを変えるときは `tests/test_core.py` も更新する。
- `python3 -m unittest discover -s tests -v` を実行する。
- 変更点と実際に行った検証を日本語で説明する。
- 未実行の検証を成功したと書かない。
