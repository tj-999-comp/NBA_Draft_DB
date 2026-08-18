# データソース・取得範囲の確定
ドキュメント：[Issue003.md](https://github.com/tj-999-comp/NBA_Draft_DB/blob/main/docs/Issue/Issue003.md)

## 背景

MVPの正本データを再現可能に作成するため、対象データと外部データソースを確定する。

## 対象範囲

- 選手、ドラフト、NBAレギュラーシーズン、オールスターの情報源を決定する
- 外部IDとplayer_idの対応方針を決める
- `source_name`、`source_url`、`retrieved_at` の記録方法を決める
- MVPで取得する基本スタッツの範囲を決める

## 完了条件

- 対象範囲と採用ソースが文書化されている
- 取得項目と出典記録のルールが確定している
- 小規模サンプルの対象範囲が決まっている

## 未決事項

- 古い時代のチーム名・フランチャイズ統合の扱い

## GitHub Issue

- #6: https://github.com/tj-999-comp/NBA_Draft_DB/issues/6
