# Documentation Index

## ドキュメント一覧

README.md
  プロジェクト概要・使用方法・Phase 5 スキーマ

docs/INDEX.md
  ドキュメント一覧・クイックリファレンス

docs/ARCHITECTURE.md
  システム全体構成・データフロー・DB スキーマ

docs/IMPLEMENTATION.md
  各モジュールの実装詳細・関数説明

docs/PHASE5_GUIDE.md
  Phase 5 の実装ガイド・抽出フロー

docs/EXTRACTION_GUIDE.md
  電話番号とメール抽出の仕様・パターン

docs/CONFIGURATION.md
  config.py の全設定項目の説明

docs/API_REFERENCE.md
  phone_extractor・email_extractor の API

docs/EXAMPLES.md
  実行例・期待出力・ログサンプル

docs/FAQ.md
  よくある質問と回答

docs/TROUBLESHOOTING.md
  エラー原因と解決方法

## ドキュメント読む順序

新規参加者向け:
  1. README.md を読む
  2. docs/ARCHITECTURE.md で構成を理解
  3. docs/EXAMPLES.md で実行例を確認

実装者向け:
  1. docs/IMPLEMENTATION.md で関数詳細を確認
  2. docs/API_REFERENCE.md で API を確認
  3. docs/CONFIGURATION.md で設定を確認

トラブル発生時:
  1. docs/TROUBLESHOOTING.md でエラーを検索
  2. docs/FAQ.md で一般的な質問を検索
  3. logs/website_scraper.log でログ確認

## クイックコマンド

全件実行:
  python website_scraper.py

テスト実行（3件）:
  python website_scraper.py --limit=3

ログ最後50行表示:
  Get-Content logs/website_scraper.log -Tail 50

ログから "エラー" を検索:
  Select-String -Path logs/website_scraper.log -Pattern "ERROR"

キャッシュとDB初期化:
  rm logs/html_cache.db
  rm logs/phase5_data.db

## Phase 5 Google Sheet スキーマ

Column A: company_name
  説明: 企業名
  型: text
  出典: CRM から取得

Column B: website_url
  説明: ウェブサイト URL
  型: URL
  出典: CRM から取得

Column C: phone
  説明: 電話番号
  型: text
  値: 電話番号 or "None"

Column D: email
  説明: メールアドレス
  型: text
  値: メールアドレス or "None"

Column E: source_page
  説明: 抽出元ページ URL
  型: URL
  値: 現在は空文字列

Column F: status
  説明: スクレイピング結果ステータス
  型: text
  値: "success" または "invalid"

Column G: scraped_at
  説明: スクレイピング実行日時
  型: datetime
  形式: YYYY-MM-DD HH:MM:SS

## Status 判定ロジック

status = "success"
  条件: 電話番号が見つかった
  email: 見つかったメール or "None"

status = "invalid"
  条件: 電話番号が見つからなかった
  email: 見つかったメール or "None"

注記: email の有無は status に影響しない

## ファイル構成

video-sales-automation-phase1/
├── website_scraper.py
├── crm_manager.py
├── db_manager_phase5.py
├── config.py
├── tools/
│   ├── phone_extractor.py
│   ├── email_extractor.py
│   ├── website_crawler.py
│   ├── company_info_extractor.py
│   └── cache_manager.py
├── logs/
│   ├── website_scraper.log
│   ├── phase5_data.db
│   ├── html_cache.db
│   └── send_log.db
├── docs/
│   ├── INDEX.md
│   ├── ARCHITECTURE.md
│   ├── IMPLEMENTATION.md
│   ├── PHASE5_GUIDE.md
│   ├── EXTRACTION_GUIDE.md
│   ├── CONFIGURATION.md
│   ├── API_REFERENCE.md
│   ├── EXAMPLES.md
│   ├── FAQ.md
│   └── TROUBLESHOOTING.md
└── README.md



## Phase 5 ステータス

✅ **完了**（2026-04-24）

### 実行結果

- 1,589 URL をクロール
- 866 件の電話番号を抽出
- Google Sheet Phase 5 に同期
- DB に永続化（status: ready_to_contact）

### 統計

| ステータス | 件数 |
|-----------|------|
| ready_to_contact | 866 |
| invalid | 415 |
| skipped | 4 |

### 出力データ

- Google Sheet Phase 5：866 行（企業名、電話、メール付き）
- Database：logs/phase5_data.db（866 レコード）
- ログ：logs/website_scraper.log（全処理履歴）

### 次フェーズ

Phase 6 を同一リポジトリ内で準備予定



## Phase 6 ドキュメント

### PHASE6_PLAN.md

Phase 6 実装計画書。仕様、処理フロー、マッチングロジック、テストケースを記載。

内容:
- ミッション: Phase 5 メール反映 & 送信履歴リセット
- 入力: Phase 5 から 45～100 件のメールアドレス
- 処理: company_name + website_url で突合、Column C 上書き、Column Z リセット、Column AA～AE クリア
- マッチング: 完全一致のみ
- リセット条件: Column Z > 0 の場合
- テスト: 5 パターン（基本、既営業、混合、一致なし、email=None）

### PHASE6_GUIDE.md

Phase 6 実装ガイド。関数リファレンス、設定項目、実行フローを記載。

内容:
- 関数: get_google_sheets_client, read_phase5_emails, read_crm_leads, match_and_update, reset_send_history, main
- 設定: SPREADSHEET_ID_PHASE5, SHEET_NAME_PHASE5, CRM_SPREADSHEET_ID, CRM_SHEET_NAME
- ログ: logs/phase6_crm_updater.log に記録
- パフォーマンス: 5～10 秒（推定）
- 既存パイプライン連携: daily_operations.py が自動メール送信開始
- トラブルシューティング: credentials.json, Sheet not found, Access Denied, Network Error

## クイックリファレンス

### Phase 6 実行

python crm_updater.py

### ログ確認

Get-Content logs/phase6_crm_updater.log -Tail 50

### 処理の順序

Phase 5 完了 → Phase 6 実行 → CRM 更新 → daily_operations 自動実行 → メール送信開始

