# NBA Draft DB

NBAでドラフトされた選手と、NBAでプレーしたドラフト外選手を対象に、ドラフト情報、NBAでのキャリア、オールスター選出などを蓄積・集計するプロジェクトです。

最終的には、ドラフト年や指名順位ごとの傾向をLooker Studioで分析し、そのレポートを静的ページに埋め込んで公開することを目指します。MVPではCloudflare D1を使わず、リポジトリ内の正本データから可視化用データと静的ページ用データを生成します。

## Documents

- [MVPロードマップ](docs/mvp-roadmap.md): 最初の可視化・公開までの目的、構成、要件、作業手順
- [将来ロードマップ](docs/future-roadmap.md): MVP後のD1、Workers、API、自動更新などの拡張方針
- [ポートフォリオ公開運用](docs/portfolio-publication.md): 作業記録の候補準備、公開要求、停止、再送手順

## 作業記録の受け渡し

公開作業記録の正本は、次の構成で管理します。

```text
work-records/
├── md/work_record_###.md
└── metadata/work_record_###.yml
```

このリポジトリは `tj-999-comp/sandbox-pages` の `NBA_Draft_DB` project向け生成元です。公開側のrendererがHTMLを生成する `a_rendered` 方式のため、生成元へ公開用HTML、CSS、designファイルは追加しません。既存の `docs/Issue/` は作業記録の公開対象ではありません。

依存パッケージなしの検証は次で実行できます。

```bash
python3 scripts/validate_work_records.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

公開要求は `.github/workflows/request-publish.yml` の手動実行だけで行います。対象commit、basename、metadataの `publish: true` を検証した後、`PUBLISH_APP_ID` と `PUBLISH_APP_PRIVATE_KEY` から発行した短期Installation tokenを使って公開リポジトリの受入workflowへ要求を送ります。公開要求には `project_id`、固定 `source_commit_sha`、`target_basename` の3項目だけを渡します。
