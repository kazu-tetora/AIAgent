# AI エージェント指示ファイル学習ラボ

## 今回はここから：コードレビュー環境

内容を忘れていても、[レビュー環境の作成・実習ガイド](docs/review-workshop.md)から再開できます。
Pythonの専用教材で試し、自分のコードへ適用し、将来Cへ拡張する構成です。

```bash
python3 -m unittest discover -s tests -v
codex --sandbox read-only
```

Codexで次の依頼を入力します。

```text
$review-source を使い、examples/review_python/spec.md を仕様として
examples/review_python/buggy.py のみをレビューしてください。
修正版・テスト・期待レビュー例は読まず、コードは変更しないでください。
```

- `.agents/skills/review-source/`：Codexが発見するレビュー手順。
- `.codex/agents/source_reviewer.toml`：親から明示的に委譲するレビュー担当。
- `examples/review_python/`：仕様、欠陥版、修正版、答え合わせ用の報告例。

以下は従来の教材です。`skills/plan-learning-task/` は配置を学ぶサンプルで、
現在のCodexのリポジトリSkill探索先ではありません。明示的にパスを渡して利用できます。
`subagents/roles/` もプロンプト例であり、新しいエージェント設定とは区別してください。

小さな Python CLI を題材に、次の4つを実際に変更・実行して学ぶサンプルプロジェクトです。

- GitHub Copilot の指示: `.github/copilot-instructions.md`
- Codex などの階層型指示: `AGENTS.md`
- 再利用可能な手順: `skills/plan-learning-task/SKILL.md`
- サブエージェントへの委譲: `subagents/roles/`

## 正式名に注意

| 書き方 | 位置づけ |
|---|---|
| `.github/copilot-instructions.md` | GitHub Copilot 用のリポジトリ指示 |
| `AGENTS.md` | Codex 系ツールで使われる正式名（複数形） |
| `AGENT.md` | よくある書き間違いを説明する案内 |
| `SKILL.md` | Skill の正式名（大文字） |
| `skill.md` | 大文字小文字を区別する環境では別ファイル |

詳細は [docs/instruction-files.md](docs/instruction-files.md) を参照してください。

## 5分で動かす

Python 3.10 以上だけで動きます。

```bash
python3 -m unittest discover -s tests -v
python3 -m learning_tasks.cli --file /tmp/agent-lab-tasks.json add "指示ファイルを読む"
python3 -m learning_tasks.cli --file /tmp/agent-lab-tasks.json list
```

## おすすめの順番

1. [LEARNING_PLAN.md](LEARNING_PLAN.md) の Day 1 から始める。
2. `AGENTS.md` と `.github/copilot-instructions.md` を比較する。
3. `skills/plan-learning-task/SKILL.md` で発火条件と手順本文の違いを確認する。
4. [docs/subagents.md](docs/subagents.md) のテンプレートで分担を設計する。
5. [docs/exercises.md](docs/exercises.md) の課題を進める。

## 構成

```text
.
├── subagents/roles/               # サブエージェント用プロンプト
├── .github/copilot-instructions.md
├── skills/plan-learning-task/     # Skill の完成例
├── learning_tasks/                # JSON 保存型タスク CLI
├── tests/
├── AGENT.md                       # 命名ミスを学ぶ案内
├── AGENTS.md                      # 実際のリポジトリ指示
├── LEARNING_PLAN.md
└── docs/
```

## 学習ゴール

- 常時適用する指示と、必要時だけ読む Skill を使い分ける。
- 指示を目的・制約・検証・完了条件に分解する。
- 独立した仕事だけをサブエージェントへ渡す。
- 親エージェントが結果を統合し、最終検証する。
