# Issue011: NBA_Draft_DBの公開作業記録生成元契約への対応

## 背景

`NBA_Draft_DB` の作業記録を、公開リポジトリ `tj-999-comp/sandbox-pages` へ安全に受け渡せる生成元リポジトリとして整備する。公開側のrendererがHTMLを生成する `a_rendered` 方式を採用し、生成元から公開リポジトリを編集しない。

## 決定事項

- `project_id` は `NBA_Draft_DB` とする。
- `main` の `work-records/` を入力源とし、Markdownとmetadataを共通basenameで管理する。
- 作業記録番号はこのproject内で `work_record_001` から独立採番する。
- metadataは `schema_version`、`title`、`date`、`project_id`、`tags`、`publish` の6項目だけを許可する。
- `a_rendered` のため、HTML、CSS、designファイル、support fileは生成元に置かない。
- `push`、Pull Request、手動実行でvalidatorを実行する。
- 公開要求は手動実行のみとし、`project_id`、`source_commit_sha`、`target_basename` の3入力に限定する。
- 指定SHAのcheckout、対象ファイル、project_id、`publish: true` の検証に成功した場合だけ、公開側の `accept-source.yml` へdispatchする。
- `SANDBOX_PAGES_DISPATCH_TOKEN` をdispatch専用Secretとして使用し、ログへtoken、Secret、作業記録本文を出力しない。
- 既存の `docs/Issue/` は公開作業記録へ自動移行しない。

## 対象範囲

- `work-records/md/work_record_###.md`
- `work-records/metadata/work_record_###.yml`
- 依存パッケージなしのvalidatorとテスト
- GitHub Actionsのvalidator workflowと公開要求workflow

HTMLの生成、公開リポジトリのregistry・Pages成果物の変更、公開リポジトリのcheckout・commit・pushは対象外とする。

## 完了条件

- 正規命名、Markdown・metadata対応、metadata schema、日付、tags、project_id、publish値をvalidatorが検証する。
- validatorの正常系・異常系テストがある。
- workflowがpush、Pull Request、手動実行でvalidatorを実行する。
- 公開要求workflowが検証成功時のみ公開側へ3入力をdispatchする。
- 全テスト、workflow YAML構文、命名・metadata確認、`git diff --check` が成功する。

## 未決事項

- 公開リポジトリ側で `NBA_Draft_DB` をregistryへ登録し、受入を有効化する時期。
- 人間承認後にどの作業記録を `publish: true` にするか。
- 公開リポジトリ側の手動E2EとPages公開確認。
