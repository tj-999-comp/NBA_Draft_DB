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

現在の候補は `work_record_001` だが、`publish: false` のため公開要求はまだ実行しない。

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

## 現在の状態

- 生成元側の標準構成、validator、CI、固定SHA公開要求workflowはPR #17で`main`へ反映済み。
- 生成元Secret `PUBLISH_APP_ID` と `PUBLISH_APP_PRIVATE_KEY` の登録名は確認済み。公開側の`NBA_Draft_DB` source registry登録、受入dry-run、手動E2E、Pages公開、Slack通知は未完了。
- `publish: true`化と実公開は、人間承認後に別途実施する。
