# Architecture & Workflow

## System Overview

Phase 1 は以下のコンポーネントで構成:

1. CRM Manager (crm_manager.py)
   - CRM シートから URL・メール・企業名を読み込み
   - Phase 5 シートへデータを追記

2. Website Scraper (website_scraper.py)
   - バッチ処理でウェブサイトをクロール
   - 電話番号・メール抽出を実行
   - DB にデータを保存

3. Database Manager (db_manager_phase5.py)
   - Phase 5 用 SQLite DB を管理
   - URL 重複チェック
   - スクレイピング結果を保存

4. Tools (tools/)
   - phone_extractor.py: 電話番号抽出
   - email_extractor.py: メールアドレス抽出
   - website_crawler.py: HTML クロール
   - company_info_extractor.py: 企業名抽出
   - cache_manager.py: HTML キャッシュ

5. Configuration (config.py)
   - Google Sheets ID・シート名
   - 抽出パターン・設定値

## Data Flow

CRM Sheet
  │
  └─→ read_website_urls_from_crm(limit)
      返り値: [(row_idx, url, email, company), ...]
  │
  └─→ website_scraper.py main
      for each url_data:
        check_url_exists() → 重複チェック
        crawl_domain() → HTML 取得
        extract_company_name() → 企業名抽出
        extract_phone() → 電話番号抽出
        extract_email() → メール抽出
        append_phase5_data() → DB 保存
        append_to_gsheet_phase5() → Sheet 追記

## Database Schema (Phase 5)

Table: phase5_data
  - id: INTEGER PRIMARY KEY
  - url: TEXT UNIQUE (重複キー)
  - company_name: TEXT
  - phone_number: TEXT
  - email: TEXT
  - status: TEXT (success/invalid/skipped)
  - scraped_at: DATETIME

## Error Handling

- HTML 取得失敗: status = "invalid"
- 電話番号未検出: status = "invalid"
- URL 重複: スキップログ出力
- API エラー: 例外捕捉・ログ出力・続行

## Caching Strategy

html_cache.db に HTML を保存
同一 URL の再クロールを回避
キャッシュ有効期限: なし（手動削除）

