# Phase 5 Implementation Guide

## アーキテクチャ
CRM Sheet
  ↓
website_scraper.py
  ├─ read_website_urls_from_crm()
  ├─ crawl_domain()
  ├─ extract_phone()
  ├─ extract_email()
  └─ append_to_gsheet_phase5()
  ↓
Phase 5 Google Sheet

## 抽出フロー
1. CRM から URL リストを読み込み
2. 各 URL に対して複数ページをクロール
3. 電話番号を抽出（見つかったら即座に次の URL へ）
4. メールアドレスを抽出（見つかったら即座に次の URL へ）
5. 結果を DB に保存
6. 結果を Phase 5 シートに追記

## Status 判定
status = "success" → 電話番号が見つかった
status = "invalid" → 電話番号が見つからなかった
（email の有無は status に影響しない）

## Troubleshooting
Google Sheets 認証エラー: credentials.json を確認
メモリ不足: --limit オプションで分割実行
キャッシュクリア: rm logs/html_cache.db logs/phase5_data.db

## 今後の拡張予定
- 複数メール抽出
- SNS 検出
- WHOIS 統合
- 並列処理
