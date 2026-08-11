# Issue002: ローカルIssueとGitHub Issueの連携運用方針

## 背景

このプロジェクトでは、セッション内で決まった要件・設計方針・優先順位・保留事項をローカルのIssue文書に記録する。必要な場合だけ、実装や調査の作業状況をGitHub Issueでも管理する。

ローカルIssueとGitHub Issueを併用する場合に、対応関係や最新の判断が分からなくならないよう、両者の役割と同期方法を定める。また、すべてのローカルIssueをGitHub Issueへ起票する必要はないことを明確にする。

## 決定事項

### 1. 役割の分担

- ローカルIssue（`docs/Issue/IssueNNN.md`）を、プロジェクト内の判断・合意・設計記録の正本とする
- GitHub Issueを作成した場合は、作業の可視化、担当、進捗、レビュー、完了状態を管理する場所とする
- ローカルIssueはGitHub Issueに起票しなくてもよく、ローカルIssue単独で完結できる
- README.mdには詳細な議論を重複して記載せず、必要な場合だけIssue文書やロードマップへリンクする

### 2. 対応関係

- GitHub Issueを作成すると決めた場合は、原則として1つのローカルIssueに対して対応するGitHub Issueを1件作成する
- GitHub Issueの作成は、ユーザーが明示的に依頼した場合、または作業開始時に起票方針が明示されている場合に限る
- ローカルIssue番号とGitHub Issue番号は別の番号体系として扱う
- GitHub Issueのタイトルには必ずローカルIssue番号を含める
  - 例: `[Issue002] ローカルIssueとGitHub Issueの連携運用方針`
- GitHub Issueを作成した場合だけ、ローカルIssueにGitHub Issue番号とURLを追記する
- GitHub Issueを作成した場合は、本文に対応するローカルIssueのパスと目的を記載する

### 3. 作成・更新の順序

1. セッションで扱う目的、背景、完了条件、未決事項をローカルIssueに記録する
2. GitHub Issueの起票が明示されている場合だけ、ローカルIssueの内容を要約してGitHub Issueを作成する
3. GitHub Issueを作成した場合だけ、番号とURLをローカルIssueに追記する
4. GitHub Issueを作成した場合は、実装・調査の進捗をローカルIssueの記録更新後にGitHub Issueにも要約する
5. 完了時は、ローカルIssueに完了条件と検証結果を記録する。GitHub Issueを作成していた場合は、そちらにも反映してクローズする

### 4. 更新内容の粒度

- ローカルIssueには、決定事項、理由、対象範囲、完了条件、未決事項、検証結果を記録する
- GitHub Issue本文には、目的、対象範囲、完了条件、対応するローカルIssueへの参照を記載する
- GitHub Issueのコメントには、作業の進捗、確認結果、レビュー上の論点など、作業中に共有する情報を記録する
- 重要な判断がコメントで決まった場合は、ローカルIssueへ反映して正本化する

## 対象範囲

- `docs/Issue/IssueNNN.md`で管理するプロジェクトの要件、設計、調査、実装、検証に関するIssue
- 明示的に依頼された場合に限るGitHub Issueの起票、対応リンクの記録、進捗同期、完了時のクローズ

## 完了条件

- ローカルIssueとGitHub Issueの役割分担が文書化されている
- ローカルIssue番号とGitHub Issue番号を相互参照できる
- GitHub Issueを作成する場合の手順と条件が定義されている
- 今後のIssueで同じ作成・更新順序を適用できる

## GitHub連携

- GitHub Issue: 本Issueでは作成しない。GitHub Issue起票が明示されたIssueに限り、起票後に番号とURLを追記する

## 未決事項

- GitHub Issueのラベル体系（`area:*`、`type:*`、`priority:*`など）をいつ導入するか
- 複数のローカルIssueにまたがる横断作業を、単一のGitHub IssueまたはProjectでどう表現するか
- GitHub Issueの本文を、ローカルIssueの更新ごとにどの範囲まで同期するか

## セッション記録

### 2026-08-11

- AGENTS.mdと既存の`Issue001`を確認した
- `Issue001`はプロジェクト目的とMVP要件の記録として維持し、連携運用方針は`Issue002`として分離する方針とした
- ローカルIssueを判断・合意の正本とし、GitHub Issueは明示的に起票する場合だけ作業の可視化・進捗管理に使う方針へ修正した
- ローカルIssueをGitHub Issueへ自動的・機械的に起票する運用は採用しない
