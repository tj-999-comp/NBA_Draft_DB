# 正本データスキーマの設計
ドキュメント：[Issue004.md](https://github.com/tj-999-comp/NBA_Draft_DB/blob/main/docs/Issue/Issue004.md)

## 背景

ドラフト情報、NBAキャリア、オールスター情報を一貫して管理するため、正本データの構造を実装可能な形にする。

## 対象範囲

- `players`
- `draft_picks`
- `player_seasons`
- `player_honors`
- SQLiteまたはCSVの採用形式
- player_id、外部ID、出典情報の制約

## 完了条件

- スキーマとキー・制約が定義されている
- drafted / undrafted と選出・出場の区別を表現できる
- サンプルデータを投入できる

## 未決事項

- 実データ取得時の外部ソースごとの採用項目

## GitHub Issue

- #1: https://github.com/tj-999-comp/NBA_Draft_DB/issues/1

## 決定事項・実装

- MVPの正本データ形式はSQLiteとする。CSV/JSONはSQLiteから生成する出力とし、手入力で更新しない。
- `players`、`draft_picks`、`player_seasons`、`player_honors`を実装した。
- 外部IDと`player_id`の対応を`player_external_ids`で管理する。
- すべての正本レコードに`source_name`、`source_url`、`retrieved_at`を保持する。
- `draft_status = undrafted`の場合、`draft_year`、`draft_round`、`overall_pick`、`draft_team`はNULLに限定する。
- `player_honors`では`appeared <= selected`を制約し、選出と実出場を区別する。
- スキーマは[db/schema.sql](../../db/schema.sql)、サンプルは[db/sample_data.sql](../../db/sample_data.sql)、初期化は[scripts/init_db.py](../../scripts/init_db.py)で再現できる。

## 検証結果

2026-08-11にサンプルSQLiteを生成し、[scripts/validate_schema.py](../../scripts/validate_schema.py)を実行した。

- player_id重複、外部キー欠落、負のgames_played、undrafted項目、selected/appeared整合性の6チェックがすべて成功
- undraftedにドラフト年を設定するINSERTを拒否
- selected=falseかつappeared=trueのINSERTを拒否
