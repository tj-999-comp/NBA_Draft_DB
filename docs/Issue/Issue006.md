# 正本データの収集・登録
ドキュメント：[Issue006.md](https://github.com/tj-999-comp/NBA_Draft_DB/blob/main/docs/Issue/Issue006.md)

## 背景

MVPの対象となるドラフト指名選手、ドラフト外選手、シーズン情報、オールスター情報を正本データへ登録する。

## 対象範囲

- player_idを中心とした選手・外部ID対応
- ドラフト情報とdrafted / undrafted区分
- NBAレギュラーシーズン情報
- オールスターのselected / appeared
- 出典情報の保存

## 完了条件

- MVP対象データが正本へ登録されている
- ドラフト外選手のドラフト項目がNULLになっている
- サンプルから本番対象へ再実行可能な登録手順がある

## 未決事項

- データ取得の具体的な自動化範囲

## GitHub Issue

- #2: https://github.com/tj-999-comp/NBA_Draft_DB/issues/2
