# Implementation Details

## website_scraper.py

### Main Functions

setup_logging()
  - LOG_FILE に情報をログ
  - コンソール出力（UTF-8）
  - ログレベル: INFO

should_skip_url(website_url)
  - CRM から URL リストを読み込み
  - 重複チェック
  - skip するなら True

scrape_website(url_data)
  - url_data = (row_idx, url, email, company_name)
  - HTML クロール
  - 企業名抽出
  - 電話番号抽出
  - メール抽出
  - result dict を返す

run_batch_scraping(limit=None)
  - DB 初期化
  - CRM から URL リスト読み込み
  - 各 URL をスクレイピング
  - DB と Sheet に保存
  - 統計情報をログ出力

### Result Dictionary

{
  'company_name': str,
  'phone_number': str or None,
  'email': str or "None",
  'status': str,
  'url': str
}

## crm_manager.py

### read_website_urls_from_crm(limit=None)

入力: limit (オプション)
処理:
  - Google Sheets client を取得
  - CRM シートを開く
  - 各行から URL・メール・企業名を抽出
  - (row_idx, url, email, company) タプルを返す
出力: リスト or エラー時 []

### append_to_gsheet_phase5(company_name, phone_number, status, website_url, email="")

入力: 企業名・電話・ステータス・URL・メール
処理:
  - Phase 5 シートを開く
  - row_data を組立 (7列)
  - append_row() で追記
  - ログ出力
出力: True/False

## db_manager_phase5.py

### init_phase5_db()

処理:
  - logs/ フォルダを確認
  - phase5_data.db を作成
  - テーブル作成（URL を UNIQUE キーに）
出力: なし

### check_url_exists(url)

入力: URL
処理: DB で URL 検索
出力: True (存在) / False (未存在)

### append_phase5_data(url, company, phone, email, status)

入力: URL・企業名・電話・メール・ステータス
処理: テーブルに行を追記
出力: True/False

