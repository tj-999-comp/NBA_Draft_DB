# Issue012: GitHub CLIのサンドボックス外実行ルール

## 背景

GitHub CLIによるPull Request、Issue、GitHub APIへの通信は、通常のサンドボックス内ではネットワーク制限により失敗する場合がある。CodexからGitHub操作を再現可能かつ誤解なく実行できるよう、リポジトリ固有の実行ルールを明文化する。

## 決定事項

- GitHub CLI（`gh pr`、`gh issue`、`gh api`など）でGitHubへ通信する場合は、権限付きのサンドボックス外実行を使用する。
- ネットワーク制限で失敗したコマンドを、通常のサンドボックス内で繰り返し実行しない。
- 実行前に対象リポジトリ、ブランチ、IssueまたはPull Request、操作内容を確認する。
- 権限付き実行が承認されない場合は、GitHub操作を完了扱いにせず、未実施として報告する。

## 対象範囲

- GitHub CLIによるGitHub API通信
- Pull Request、Issue、ラベル、レビュー、コメント、GitHub Actionsの操作
- GitHub通信を伴う読み取りおよび書き込み

## 完了条件

- `AGENTS.md`にGitHub CLIのサンドボックス外実行ルールが記載されている。
- 実行失敗時に、GitHub上の操作状態を誤って完了報告しない方針が記載されている。

## 未決事項

- GitHub CLIとGitHubコネクタの使い分けを、今後必要に応じて補足する。

## 検証結果

- `AGENTS.md`へのルール追加を確認した。
- 本Issueを次のローカルIssue番号 `Issue012` として記録した。
