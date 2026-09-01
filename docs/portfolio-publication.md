# ポートフォリオ作業記録の公開運用

この文書は、`NBA_Draft_DB` の作業記録を `tj-999-comp/sandbox-pages` へ公開要求する際の生成元側手順を定める。公開リポジトリ側の受入、Pages、provenance、Slack通知の正本は、公開リポジトリの契約文書とIssue #70および子Issueとする。

## 所有境界

- このリポジトリは、Markdown、metadata、自己検証、公開要求のdispatchだけを担当する。
- `sandbox-pages`をcheckout、編集、commit、pushしない。
- 公開リポジトリのsource registry、公開承認、Pages成果物、provenance、Slack通知は公開リポジトリ側で管理する。
- `docs/Issue/`はプロジェクトの判断記録であり、自動公開対象ではない。

## 公開候補の準備

1. `work-records/md/work_record_###.md` と `work-records/metadata/work_record_###.yml` のbasenameが一致していることを確認する。
2. 作業記録の内容にSecret、token、Webhook URL、個人情報、非公開データが含まれないことを確認する。
3. `python3 scripts/validate_work_records.py` とテストを実行する。
4. 人間の明示承認を得るまで、metadataの `publish` は `false` のままにする。
5. 承認後、`publish: true` の変更だけを含むコミットを作成し、検証してから `main` へ反映する。
6. 公開要求に使用する40桁の固定commit SHAと対象basenameを記録する。

初期候補は `work_record_001` で、内容確認と明示承認後に `publish: true` へ変更した。承認済み固定commitは `055dec2165c3d67363338de48172206af7ed6b2b` である。

## 公開要求

`.github/workflows/request-publish.yml` を手動実行し、次の3項目だけを入力する。

- `project_id`: `NBA_Draft_DB`
- `source_commit_sha`: `main`上の40桁の固定commit SHA
- `target_basename`: `work_record_###`

workflowは、固定SHAが`main`の祖先であること、対象ファイル、`project_id`、`publish: true`を検証する。検証成功後、`PUBLISH_APP_ID` と `PUBLISH_APP_PRIVATE_KEY` から発行した短期GitHub App Installation tokenで、公開リポジトリの受入workflowへdispatchする。

Secretの値をログ、Issue、作業記録、artifactへ出力しない。公開要求のdispatch成功は公開完了を意味せず、公開側の受入・provenance・Pages deploy・Slack通知の完了を確認する。

## 停止と再送

- 公開側の受入を止める場合は、公開リポジトリ側で `enabled: false` と実行中workflowの停止を行う。生成元から公開リポジトリを直接変更しない。
- `publish: false`への変更や生成元ファイルの削除だけで、公開済み成果物を取り下げない。
- 公開済み成果物の取り下げは、公開リポジトリ側のwithdraw手順でdry-runを確認してから行う。
- Slack通知だけが失敗した場合は、公開側で同じ`publication_id`の通知jobを再実行する。Pages公開を重複実行しない。
- 同じ公開要求を再送する場合は、固定SHA、対象basename、直前の受入結果、`publication_id`を照合してから行う。

## 作業記録のGitHub Issue状況

作業記録を作成する直前に、Pull Requestを除く `tj-999-comp/NBA_Draft_DB` の全Open IssueをGitHub APIから再取得する。取得日時（JST）、取得範囲、取得件数を記録し、優先順位表のIssue行数と取得件数を一致させる。各Issueの番号、タイトル、URL、state、state reason、作業記録との関係・着手条件を個別に記載する。親子関係はGitHubのsub-issues APIで確認できたものだけを記載し、Issue本文から推測しない。外部リポジトリのIssueは一覧へ混在させず、必要な場合だけ補足する。API取得に失敗した場合は状態を推測せず、未確認範囲と再取得手順を記録する。

取得と親子関係確認の例:

```bash
gh issue list --repo tj-999-comp/NBA_Draft_DB --state open --json number,title,state,stateReason,url --limit 100
gh api repos/tj-999-comp/NBA_Draft_DB/issues/<番号>/sub_issues
```

取得結果は作業記録末尾の`## GitHub Issue状況`へ反映し、件数と一覧行数を確認してからcommitする。

## 作業記録HTMLの共通デザイン

公開HTMLの正本は、公開リポジトリの [`work-records/design.md`](https://github.com/tj-999-comp/sandbox-pages/blob/main/work-records/design.md) とA側の `a_rendered` renderer/CSSである。生成元ではHTML・CSS・designを管理せず、全生成元で `record-page`、`shell`、`topbar`、`record-header`、`record-meta`、番号付き`record-section`、共通footerを使う同一の詳細ページ形式を利用する。新規・更新時は1280pxと320pxで横overflow、console/page error、failed requestがなく、生成元間の主要構造・スタイルが一致することを確認する。不一致が残る場合は公開導入を完了扱いにしない。

## 2026-08-31 E2E実績

`work_record_001`について、次の実行結果を確認済みである。

- source-side公開要求: [run 33369387551](https://github.com/tj-999-comp/NBA_Draft_DB/actions/runs/33369387551)（固定SHA、対象basename、validator、GitHub App認証、公開側dispatchが成功）。
- 公開側full E2E: [run 33369404796](https://github.com/tj-999-comp/sandbox-pages/actions/runs/33369404796)（A側validator、`a_rendered` renderer、apply、provenance、Pages build/deploy、公開URL確認、Slack通知が成功）。
- 公開側commit: `3d02a57cbfb1360f4a62c99b13471cb58e904b82`。
- publication_id: `accept-33369404796-1-NBA_Draft_DB-work_record_001`。
- 公開URL: <https://tj-999-comp.github.io/sandbox-pages/projects/NBA_Draft_DB/work_record_001.html>。
- 同一要求の再送: source-side [run 33369593130](https://github.com/tj-999-comp/NBA_Draft_DB/actions/runs/33369593130) と公開側 [run 33369607800](https://github.com/tj-999-comp/sandbox-pages/actions/runs/33369607800) が成功。公開側applyはno-op、Pages deployとSlack通知はskipとなり、重複公開・重複通知は発生しなかった。

恒久自動公開triggerは設定しない。通常の公開は、内容確認・明示承認・source-side validator・固定SHA・3入力dispatch・公開側受入結果の確認を経て行う。

## 現在の状態

- 生成元側の標準構成、validator、CI、固定SHA公開要求workflowはPR #17で`main`へ反映済み。
- 生成元Secret `PUBLISH_APP_ID` と `PUBLISH_APP_PRIVATE_KEY` の登録名は確認済み。公開側の`NBA_Draft_DB` source registry登録、受入dry-run、手動E2E、Pages公開、Slack通知は完了済み。
- `work_record_001`の承認付き公開、Pages表示、Slack通知、同一要求再送のno-opは完了済み。今後はこの手順で個別の作業記録を公開し、停止時は公開側で`enabled:false`へ戻して実行中workflowとprovenanceを確認する。
