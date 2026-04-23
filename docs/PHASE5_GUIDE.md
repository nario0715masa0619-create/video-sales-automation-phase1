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


## 実行結果（2026-04-24）

### 最終統計

処理完了: 1,589 items
電話番号検出: 866 件（67.4%）
invalid: 415 件
skipped: 4 件
実行時間: 約 7 時間

### 出力先

Google Sheet Phase 5: 866 行（header 除く）
- Column A: company_name
- Column B: website_url
- Column C: phone
- Column D: email
- Column E: source_page
- Column F: status（ready_to_contact）
- Column G: scraped_at

Database: logs/phase5_data.db
- テーブル: phase5_data
- レコード数: 866
- 主キー: id
- UNIQUE 制約: url

ログファイル: logs/website_scraper.log
- 全処理詳細
- エラー記録
- パフォーマンス統計

### DB 確認コマンド

統計確認:
python -c "import sqlite3; conn = sqlite3.connect('logs/phase5_data.db'); cursor = conn.cursor(); cursor.execute('SELECT status, COUNT(*) FROM phase5_data GROUP BY status'); [print(f'{row[0]}: {row[1]} 件') for row in cursor.fetchall()]; conn.close()"

最後の 5 件確認:
python -c "import sqlite3; conn = sqlite3.connect('logs/phase5_data.db'); cursor = conn.cursor(); cursor.execute('SELECT company_name, phone_number, status FROM phase5_data ORDER BY id DESC LIMIT 5'); [print(f'{row[0]} | {row[1]} | {row[2]}') for row in cursor.fetchall()]; conn.close()"

ready_to_contact の件数確認:
python -c "import sqlite3; conn = sqlite3.connect('logs/phase5_data.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM phase5_data WHERE status=\"ready_to_contact\"'); print(f'ready_to_contact: {cursor.fetchone()[0]} 件'); conn.close()"

### パフォーマンス実績

実行時間: 約 7 時間
平均: 1 URL あたり 15.9 秒（7 時間 ÷ 1,589 URL）
ネットワーク遅延とページ量により変動

### 次ステップ

Phase 5 データ（866 件の企業連絡先）を活用したフェーズを設計中
Phase 6 以降を同一リポジトリ内で準備予定

