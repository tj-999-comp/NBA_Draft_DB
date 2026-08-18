# 集計・検証処理の実装
ドキュメント：[Issue007.md](https://github.com/tj-999-comp/NBA_Draft_DB/blob/main/docs/Issue/Issue007.md)

## 背景

正本データからキャリア指標と比較用集計を再生成し、データ品質を確認できるようにする。

## 対象範囲

- 初出場・最終出場シーズン
- NBA活動シーズン数、キャリア期間、通算出場試合数
- 選手別、ドラフト年別、指名順位別集計
- drafted / undrafted比較
- オールスター選出回数・出場回数
- 必須の整合性検証

## 完了条件

- 同じ正本データから同じ集計結果を再生成できる
- AGENTS.mdに定めた検証項目を確認できる
- サンプルデータの期待結果と一致する

## 未決事項

- 欠損値や古いチーム名の扱い

## GitHub Issue

- #5: https://github.com/tj-999-comp/NBA_Draft_DB/issues/5
