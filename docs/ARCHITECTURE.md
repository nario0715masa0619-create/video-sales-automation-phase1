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



## Phase 6 アーキテクチャ

### システム図

Google Sheet Phase 5（866 行）
  ├─ Column A: company_name
  ├─ Column B: website_url
  └─ Column D: email
    ↓
crm_updater.py
  ├─ read_phase5_emails()
  │   └─ email != "None" の行のみ抽出
  ├─ read_crm_leads()
  │   └─ Column A, B, C, Z, AA～AE を抽出
  ├─ match_and_update()
  │   └─ company_name + website_url で突合 → Column C 上書き
  ├─ reset_send_history()
  │   └─ Column Z > 0 の場合 → Z を 0 に & AA～AE をクリア
  └─ log_statistics()
      └─ logs/phase6_crm_updater.log に記録
    ↓
CRM Sheet "Leads"
  ├─ Column C: email（上書き完了）
  ├─ Column Z: メール送信回数（0 にリセット）
  └─ Column AA～AE: 送信日時（クリア）
    ↓
既存パイプライン
  ├─ daily_operations.py（定時実行）
  ├─ send_email.py（Column Z == 0 を検知）
  └─ get_pending_leads()（新しいメールアドレスに送信）

### データフロー

Phase 5 メール抽出
  ↓
Phase 6: CRM 反映 & リセット
  ↓
既存パイプライン: 自動メール送信
  ↓
営業サイクル完了

### 外部システムとの連携

#### Google Sheets API

Phase 5 読込: read_phase5_emails()
  ├─ GET: SPREADSHEET_ID_PHASE5 Sheet
  └─ 読込: Column A, B, D

CRM 読込: read_crm_leads()
  ├─ GET: CRM_SPREADSHEET_ID Sheet "Leads"
  └─ 読込: Column A, B, C, Z, AA～AE

CRM 更新: match_and_update(), reset_send_history()
  ├─ UPDATE: Column C（メール上書き）
  ├─ UPDATE: Column Z（リセット）
  └─ UPDATE: Column AA～AE（クリア）

#### 既存パイプラインとの連携

daily_operations.py
  ├─ Phase 6 完了後、定時実行
  ├─ send_email.py を呼び出し
  └─ Column Z == 0 の企業にメール送信

send_email.py
  ├─ get_pending_leads() で対象抽出
  ├─ Column Z == 0 を検知
  └─ 新しいメールアドレスへ送信

### エラーハンドリング

Phase 6 エラー
  ├─ credentials.json not found
  ├─ Sheet not found
  ├─ Access Denied
  ├─ Network Error
  └─ すべてを logs/phase6_crm_updater.log に記録

エラー発生時
  ├─ 該当行をスキップ
  ├─ 次の行を処理
  └─ 最終統計でエラー件数を表示

### パフォーマンス特性

読込: 1～2 秒（Phase 5: 866 行、CRM: 1705 行）
マッチング: 1～2 秒（866 行 × 1705 行のマッチング）
更新: 2～3 秒（Google Sheets API リクエスト）
リセット: 1～2 秒（Column Z & AA～AE 更新）
合計: 5～10 秒

### 設定管理

config.py に以下を定義:
  SPREADSHEET_ID_PHASE5
  SHEET_NAME_PHASE5
  CRM_SPREADSHEET_ID
  CRM_SHEET_NAME = "Leads"（固定）

credentials.json
  Google Sheets API 認証情報

logs/phase6_crm_updater.log
  処理ログ、エラー、統計

