# 7日間の学習計画

1日30〜60分を想定します。短縮する場合は Day 1、2、4、7 を行います。

## Day 1: 指示ファイルの地図

- `docs/instruction-files.md` を読む。
- `AGENTS.md`、Copilot 指示、`SKILL.md` の対象と発火条件を比べる。
- `AGENT.md` と `skill.md` が正式名ではない理由を説明する。

成果物: 3行の比較メモ。

## Day 2: ベースライン

```bash
python3 -m unittest discover -s tests -v
python3 -m learning_tasks.cli --help
```

`learning_tasks/core.py` とテストを対応づけ、壊してはいけない振る舞いを3つ挙げます。

## Day 3: 指示を改善

`AGENTS.md` の曖昧な表現を1つ、実行コマンドまたは観測可能な完了条件へ直します。

## Day 4: Skill を使う

```text
$plan-learning-task を使い、「期限フィールドを追加する」を
検証可能な実装計画にしてください。
```

frontmatter が発火、本文が実行手順を担当することを確認します。

## Day 5: 1担当へ委譲

`subagents/roles/reviewer.md` を使い、変更なしのレビューを依頼します。返答を採用・保留・却下に分類し、親が根拠を再確認します。

## Day 6: 並列化を設計

`docs/subagents.md` を読み、調査・実装・テストの依存関係とファイル競合を図にします。実際の並列起動は任意です。

## Day 7: 総合演習

`docs/exercises.md` の総合課題を行います。

完了条件:

- 変更理由を説明できる。
- 全テストが成功する。
- 指示と実装が矛盾しない。
- 委譲した場合、各担当の入力・出力・採否を記録する。

## 毎日の振り返り

1. どの指示が結果に最も効いたか。
2. エージェントが推測した点は何か。
3. 次回、指示・Skill・委譲境界のどれを改善するか。

