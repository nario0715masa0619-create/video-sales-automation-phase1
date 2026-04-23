# Examples & Sample Output

## 実行例 1: テスト実行（3 URL）

コマンド:
  python website_scraper.py --limit=3

期待される出力:
  ================================================================================
  🚀 batch scraping 開始
  ================================================================================
  📦 Phase 5 DB を初期化しました
  📥 CRM から 1705 件の URL を読み込みました
  ✅ limit=3 を適用: 3 件に限定
  
  Row 2 → https://example.com
     ✅ HTML 取得: 5 ページ
     🏢 企業名: Example Corp
     📞 電話番号: 03-1234-5678
     📧 メール: contact@example.com
     💾 DB に保存
     💾 Phase 5 に保存: Example Corp | 03-1234-5678 | success
  
  Row 3 → https://sample.jp
     ⏭️  スキップ（既に DB に存在）
  
  Row 4 → https://test.co.jp
     ❌ HTML 取得失敗
     💾 Phase 5 に保存: test corp | None | invalid
  
  ================================================================================
  ✅ 完了
  処理数: 3 / スキップ: 1 / 保存: 2
  実行時間: 45 秒
  ================================================================================

## 実行例 2: 全件実行（1589 URL）

コマンド:
  python website_scraper.py

期待される出力:
  🚀 batch scraping 開始
  📥 CRM から 1705 件の URL を読み込みました
  ✅ limit なし: 1589 件を処理
  
  Progress: 1/1589 → https://example1.com
  Progress: 2/1589 → https://example2.com
  Progress: 3/1589 → https://example3.com
  ...
  Progress: 1589/1589 → https://example1589.com
  
  ================================================================================
  📊 最終統計
  ================================================================================
  総処理数: 1589
  電話番号検出: 234 (14.7%)
  メール検出: 89 (5.6%)
  ステータス success: 234
  ステータス invalid: 1355
  実行時間: 6 時間 42 分
  DB 行数: 234
  Phase 5 シート行数: 234
  ================================================================================

## ログ例

ログファイル: logs/website_scraper.log

2026-04-23 21:00:00,123 INFO: ========== batch scraping 開始 ==========
2026-04-23 21:00:01,456 INFO: 📦 Phase 5 DB を初期化
2026-04-23 21:00:02,789 INFO: 📥 CRM から 1705 件読込
2026-04-23 21:00:03,012 INFO: Row 2 → https://example.com
2026-04-23 21:00:05,345 INFO: ✅ HTML 取得: 5 ページ
2026-04-23 21:00:06,678 INFO: 🏢 企業名: Example Corp
2026-04-23 21:00:07,901 INFO: 📞 tel リンク: 03-1234-5678
2026-04-23 21:00:08,234 INFO: 📧 mailto リンク: contact@example.com
2026-04-23 21:00:09,567 INFO: 💾 DB に保存
2026-04-23 21:00:10,890 INFO: 💾 Phase 5 に保存

## エラーログ例

2026-04-23 21:15:30,123 ERROR: ❌ HTML 取得失敗: Timeout
2026-04-23 21:15:31,456 WARNING: ⏭️  スキップ（短縮 URL）
2026-04-23 21:15:32,789 ERROR: ❌ Google Sheets API エラー



## Phase 5 実行例（2026-04-24 実績）

### 実行例 1：テスト実行（limit=3）

コマンド:
python website_scraper.py --limit=3

期待出力:
バッチ開始 → Phase 5 DB 初期化 → CRM から 1705 件読込 → limit=3 適用 → 3 件処理

Row 2 (https://example.com):
HTML 取得 5 ページ
企業名: Example Corp
電話: 03-1234-5678
メール: contact@example.com
DB 保存 ✓
Phase 5 保存 (ready_to_contact) ✓

Row 3 (https://sample.jp):
スキップ（既に DB に存在）

Row 4 (https://test.co.jp):
HTML 取得失敗
Phase 5 保存 (invalid) ✓

結果: 処理数 3, スキップ 1, 保存 2, 実行時間 45 秒

### 実行例 2：全件実行（実績）

コマンド:
python website_scraper.py

期待出力:
1705 件読込 → 1589 件処理 → プログレス表示

最終統計:
総処理数: 1589
電話番号検出: 866 (54.5%)
invalid: 415
skipped: 4
実行時間: 約 7 時間
DB 行数: 866
Phase 5 シート行数: 866

### ログ出力例

2026-04-24 00:24:19.307 | INFO | 💾 Phase 5 に保存: ビジネスサクセスアカデミー / クサマ社長 | 03-3515-3660 | ready_to_contact
2026-04-24 00:24:19,307 - INFO - Progress: 1588/1589 (既存スキップ: 304)
2026-04-24 00:24:19,308 - INFO - Completed: 1589 items, 866 with phone numbers, 305 skipped
2026-04-24 00:24:19,308 - INFO - ✅ キャッシュをクリーンアップしました

### DB 統計確認例

実行結果:
ready_to_contact: 866 件
invalid: 415 件
skipped: 4 件

### エラーログ例

HTML 取得失敗: Timeout
スキップ: 短縮 URL (developers.google.com/youtube)
Google Sheets API エラー: Access Denied

