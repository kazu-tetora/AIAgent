# Pythonから始めるレビュー環境の作成・実習ガイド

## 1. このプロジェクトを思い出す

元の教材は、JSONに学習タスクを保存するPython CLIです。
`learning_tasks/core.py` が保存と操作、`cli.py` が表示、`tests/test_core.py` が振る舞いを担当します。
`id`・`title`・`done` の互換性を守る題材として残しています。

| 部品 | 役割 |
|---|---|
| `AGENTS.md` | このリポジトリで常時守る作業規約 |
| `skills/plan-learning-task/` | 従来の計画Skill教材。パスを指定して読む |
| `subagents/roles/` | 従来の役割プロンプト例。自動起動設定ではない |
| `.agents/skills/review-source/` | 今回追加した、再利用するレビュー手順 |
| 同Skillの `agents/openai.yaml` | Skillの表示情報。レビュー担当の定義ではない |
| `.codex/agents/source_reviewer.toml` | 親が呼び出すレビュー担当の定義 |
| `examples/review_python/` | 既存CLIと分離したレビュー演習 |

Skillは「どの手順で調べるか」、エージェントは「誰にどの範囲を任せるか」です。
親は対象と仕様を渡し、返された根拠を確認して報告書にまとめます。

## 2. 前提と初期確認

Python 3.10以上、Git、ログイン済みのCodexを使用します。Python教材の実行に外部パッケージやAPIキーは不要です。
Codex自体の利用にはアカウントまたは利用環境の認証が必要です。
以下のコマンドはすべてリポジトリルートで実行します。

```bash
python3 --version
git status --short
codex --version
python3 -m unittest discover -s tests -v
```

欠陥版の4テストは `expected failure` と表示されます。空入力と一致なしは同じ欠陥を別々に確認しています。
意図した失敗を記録しながら通常のテストを成功させるための `unittest.expectedFailure` です。
想定外の失敗や、欠陥版を直して生じる `unexpected success` はテスト全体を失敗させます。

## 3. どう作ったか

1. 既存README・指示・実装・テストを読み、CLIを変更しないと決めました。最初の7テストは成功していました。
2. 入出力、入力を変更しないこと、空入力、上限の契約を先に定義しました。これで好みによる指摘と仕様違反を区別できます。
3. `review-source` のfrontmatterには名前と発火条件を置き、本文には対象確定→調査→検証→報告の短い手順を書きました。
4. `references/common.md` に言語共通の基準と重要度、`python.md` にPythonの観点を分けました。言語ごとの全文を毎回読む必要をなくしています。
5. `report-template.md` で場所・条件・影響・根拠・再現・改善案を揃えました。質問や未実行の検証は別に記録します。
6. `agents/openai.yaml` に日本語の表示名と `$review-source` を含む依頼例を追加しました。通常の自動選択は無効にしていません。
7. `source_reviewer.toml` に担当名・説明・役割指示を定義しました。Skillを参照することで基準の二重管理を避け、モデルも固定していません。
8. 同じ仕様テストを欠陥版と修正版に適用し、欠陥の再現と改善を確認しました。レビュー担当には答えを渡さず、別途演習しました。

配置は[公式Skillガイド](https://learn.chatgpt.com/docs/build-skills)、担当定義は[公式サブエージェントガイド](https://learn.chatgpt.com/docs/agent-configuration/subagents)に基づきます（2026年10月14日確認）。
実際に認識されるかは使用中のCodexバージョン・設定にも依存します。

## 4. まずSkill単独でレビューする

```bash
codex --sandbox read-only
```

開始したCodexに入力します。

```text
$review-source を使ってレビューしてください。
仕様: examples/review_python/spec.md
対象: examples/review_python/buggy.py のみ
修正版、テスト、期待レビュー例は読まないでください。
コードは変更せず、必要な再現は許可された一時領域だけで行ってください。
報告書は日本語Markdownで画面に返してください。
```

認識されないときはCodexを再起動し、`/skills` で確認します。
それでも使えない場合は「`.agents/skills/review-source/SKILL.md` を読んで、その手順でレビュー」とパスを明示します。

## 5. レビュー担当へ委譲する

同じリポジトリを開いた新しいCodexセッションで依頼します。

```text
source_reviewer を1担当起動し、.agents/skills/review-source/SKILL.md を使って
examples/review_python/spec.md と examples/review_python/buggy.py のみをレビューさせてください。
修正版、テスト、期待レビュー例は読ませず、編集を禁止してください。
結果を待ち、親が場所と根拠を確認して日本語Markdownにまとめてください。
```

設定ファイルを置くだけで自動起動するわけではありません。
担当を利用できない環境では、親が同じSkillを読み、同じ範囲を順番にレビューします。
この場合は独立した担当による検証ではないことを記録します。

担当の「編集しない」は指示です。子の権限は親から継承され、担当ファイルに独立したread-only権限を設定していません。
CLIでは親を `--sandbox read-only` で起動して制限します。この状態では親もリポジトリへ報告書を保存できません。
画面の報告を手動保存するか、書き込み可能な別セッションで親へ次のように依頼します。

```text
確認済みのレビュー結果を docs/my-review.md に保存してください。
対象ソースやテストは変更しないでください。
```

## 6. 答え合わせする

レビュー後に初めて `examples/review_python/expected-review.md` と `fixed.py` を開きます。
指摘の文章や件数の一致より、条件・影響・根拠が合っているかを確認します。

```bash
python3 -m unittest discover -s tests -p test_review_sample.py -v
```

修正版にも同じSkillでレビューを依頼し、元の指摘が解消していることを確かめます。
型が不正な入力の検証や、辞書の深いコピーは仕様にないため、欠落だけで不具合としません。

## 7. 自分のコードで使う

ファイル単位の例：

```text
$review-source を使い learning_tasks/core.py と learning_tasks/cli.py をレビューしてください。
READMEと関連テストを仕様の根拠にし、JSON互換性とCLIのエラー処理を確認してください。
コードは変更せず、報告書は画面に返してください。
```

差分単位の例（`main` が実在する場合）：

```text
$review-source を使い main...HEAD のコミット差分をレビューしてください。
未コミット変更は対象外です。関連する呼び出し元とテストも読み、回帰と既存問題を区別してください。
```

未コミット変更も含めるなら、その範囲を明記します。比較元を指定しなかった場合は確認してから進めます。
別リポジトリでは `.agents/skills/review-source/` と `.codex/agents/source_reviewer.toml` を同じ配置でコピーし、
対象側の指示・Pythonバージョン・テスト手順を確認します。既存の同名設定がある場合は内容を比較してから統合します。
ユーザー共通設定へのインストールは不要です。

## 8. Cへ拡張する手順

1. Cの規格、対象OS、コンパイラ、ビルド方法を対象プロジェクトで確定します。
2. Skillの `references/c.md` に境界外アクセス、寿命・所有権、未定義動作、整数変換、資源解放の観点を追加します。
3. `SKILL.md` にCのときだけその資料を読む分岐を追加します。共通基準や報告形式は再利用します。
4. `examples/review_c/` に仕様・欠陥版・修正版・検証を用意します。コンパイラ警告や利用できるSanitizerの手順を対象環境に合わせて決めます。
5. 実行確認後に対応言語の説明を更新します。それまでは「C対応済み」としません。

今回、Cのチェックリスト・教材・コンパイラ導入は行っていません。

## 9. 検証記録

今回の実施結果と制限は [review-validation.md](review-validation.md) に記録します。
構造チェックだけではレビューの品質やCodexの自動認識を保証しません。構造・テスト・実際の指摘を分けて確認します。

Skillの公式バリデーターが利用できる環境では、次を実行します（ユーザー名は環境に合わせて変更）。

```bash
python3 /Users/terakadokazuya/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/review-source
```

利用できない場合はフォルダ名と `name` の一致、frontmatterが `name`・`description` のみであること、
参照リンクの実在、`openai.yaml` の名前と依頼例の一致を確認します。バリデーター用依存は教材の必須環境に追加しません。
