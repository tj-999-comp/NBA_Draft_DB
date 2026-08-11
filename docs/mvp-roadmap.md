# NBA Draft DB MVPロードマップ

## 1. MVPの目的

NBAドラフトの指名選手と、NBAでプレーしたドラフト外選手について、ドラフト情報とNBAキャリアの基本統計を集計する。

集計結果をLooker Studioで分析できる状態にし、そのレポートを静的ページへ埋め込んで公開することをMVPの完了条件とする。

## 2. MVPの対象範囲

### 対象

- NBAドラフトで指名された選手
- NBAで公式戦に出場したドラフト外選手
- NBAのレギュラーシーズンを基本対象とする
- 現役選手を含む

### MVPでは対象外とするもの

- ABAや海外リーグの詳細実績
- NBA以外のリーグ成績
- 高度な選手評価指標
- 管理画面からのデータ編集
- 完全自動の定期スクレイピング
- Cloudflare D1を利用したオンラインDB

## 3. 基本指標

### ドラフト情報

- ドラフト年
- ドラフトラウンド
- 全体指名順位
- 指名チーム
- ドラフト区分（drafted / undrafted）

### NBAキャリア

- NBA初出場シーズン
- NBA最終出場シーズン
- NBA公式戦に出場したシーズン数
- キャリア期間
- 通算出場試合数

「何年残ったか」は、MVPではNBA公式戦に出場したシーズン数を主指標とする。初出場から最終出場までの期間は別指標として保持し、途中離脱のある選手も区別できるようにする。

### オールスター

- オールスター選出回数
- オールスター出場回数（取得できる場合）

選出されたが欠場した選手は、選出回数には含め、出場回数には含めない。

## 4. データの正本と出力

MVPでは、リポジトリ内のSQLiteまたはCSVを正本データとする。Google Sheets、Looker Studio、静的ページは正本から生成する出力先として扱う。

```text
正本データ（SQLiteまたはCSV）
        ├─ 集計CSVまたはGoogle Sheets
        │       └─ Looker Studio
        │
        └─ 静的JSON / CSV
                └─ Cloudflare Pages上の静的ページ
```

同じ情報を複数の場所で手入力しない。データを更新する場合は、正本を更新してから各出力を再生成する。

## 5. MVPの論理データ構成

### players

選手の基本情報を保持する。

- `player_id`
- `display_name`
- `birth_date`
- `country`
- `position`
- `source_name`
- `source_url`
- `retrieved_at`

### draft_picks

ドラフト結果とドラフト外区分を保持する。

- `player_id`
- `draft_year`
- `draft_round`
- `overall_pick`
- `draft_team`
- `draft_status`
- `source_name`
- `source_url`
- `retrieved_at`

ドラフト外選手は `draft_status = undrafted` とし、ドラフト年・指名順位はNULLとする。MVPでは、ドラフト外選手をNBA初出場シーズン別に集計する。

### player_seasons

選手のシーズン単位のNBA活動を保持する。

- `player_id`
- `season`
- `team`
- `games_played`
- `starts`
- `minutes`
- `points`
- `rebounds`
- `assists`
- `source_name`
- `source_url`
- `retrieved_at`

MVPの主要集計に不要なスタッツは、データ取得の負担を見ながら追加する。

### player_honors

オールスターなどの選出・受賞情報を保持する。

- `player_id`
- `season`
- `honor_type`
- `selected`
- `appeared`
- `source_name`
- `source_url`
- `retrieved_at`

### 集計出力

Looker Studio用には、以下のような集計済みデータを出力する。

- 選手別キャリアサマリー
- ドラフト年別サマリー
- 指名順位別サマリー
- drafted / undrafted 比較
- オールスター選手一覧

## 6. MVPで作成する可視化

- ドラフト年ごとの選手数
- ドラフト年ごとの平均NBA活動シーズン数
- 指名順位と通算出場試合数の関係
- 1巡目、2巡目、ドラフト外の比較
- ドラフト年別のオールスター選出人数
- ドラフト外からオールスターに選出された選手
- 選手別のキャリアサマリー

## 7. 公開構成

静的ページはCloudflare Pagesに配置する。Looker Studioのレポートは公開設定を確認したうえで、生成された埋め込み用iframeをページに配置する。

静的ページ側には、必要に応じて以下を配置する。

- プロジェクトの概要
- Looker Studioレポート
- データの対象範囲と指標の定義
- データの最終更新日時
- データソースと注意事項

## 8. ロードマップ

### Phase 1: 要件と小規模データ

- 対象範囲と指標定義を確定する
- 代表的なドラフト年のサンプルを作る
- 選手IDと出典情報の方針を決める
- SQLiteまたはCSVの形式を決める

### Phase 2: 正本データと集計

- 基本テーブルを作る
- ドラフト情報を登録する
- シーズン単位の情報を登録する
- オールスター情報を登録する
- キャリア集計を生成する
- 集計結果を検証する

### Phase 3: Looker Studio

- Looker Studio用のCSVまたはGoogle Sheetsを生成する
- データソースを接続する
- 基本チャートとフィルターを作る
- 選手名、ドラフト年、指名順位、ドラフト区分で絞り込めるようにする

### Phase 4: 静的ページと公開

- 埋め込み用の静的ページを作る
- レポートをiframeで埋め込む
- 更新日時と出典を表示する
- Cloudflare Pagesへデプロイする
- 公開環境でレポートが閲覧できることを確認する

## 9. MVP完了条件

- 正本データから集計結果を再生成できる
- drafted / undrafted を区別できる
- ドラフト年、指名順位、NBA活動シーズン数、通算出場試合数、オールスター選出回数を確認できる
- Looker Studioで基本的な比較・絞り込みができる
- Looker Studioレポートを静的ページに埋め込める
- Cloudflare Pagesで静的ページを公開できる
- データの出典と最終更新日時を確認できる

## 10. MVPで保留する判断

- 選手の詳細プロフィール項目
- 通算・平均スタッツの範囲
- プレーオフ成績
- All-NBAなどオールスター以外の賞
- ドラフト年のないドラフト外選手を、どの年の集計に含めるか
- 古い時代のチーム名・フランチャイズ統合の扱い
