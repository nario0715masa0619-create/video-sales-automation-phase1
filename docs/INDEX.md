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

