# Video Sales Automation - Phase 1～7

営業自動化プロジェクト Phase 1～7

## 主な機能
- CRM シートから企業 URL を読み込み
- ウェブサイトをクロール
- 電話番号とメールアドレスを自動抽出
- ZeroBounce でメール検証
- 検証結果に基づいてメール送信
- 結果を Phase 5 Google Sheet に保存

## 使用方法

### Phase 5: ウェブスクレイピング

python website_scraper.py
python website_scraper.py --limit=3

### Phase 6: ZeroBounce メール検証

python bounce_checker.py 10
python bounce_checker.py 1589

### Phase 7: メール送信

python send_email.py --dry-run --limit=5
python send_email.py --limit=20

### 日次メトリクス記録

python daily_metrics_logger.py
python daily_metrics_logger.py "テスト実行、○○業界多め"

### 送信対象リスト作成

python create_sendable_list.py

## Phase 5 Google Sheet スキーマ

列A: company_name (企業名)
列B: website_url (ウェブサイト URL)
列C: phone_number (電話番号または None)
列D: email (メールアドレスまたは None)
列E: source_page (抽出元ページ)
列F: status (ready_to_contact または invalid)
列G: scraped_at (実行日時 YYYY-MM-DD HH:MM:SS)

## Email 抽出機能

tools/email_extractor.py で実装
優先順位: mailto リンク → JSON-LD → meta タグ → regex
ドメイン検証: テスト用ドメイン除外、画像ファイル除外、localhost 除外
未検出時は None 文字列を保存

## パフォーマンス

1 URL あたり 10-30 秒
全 1,589 URL で約 4-8 時間（シングルスレッド）

---

## Phase 5 実行結果（2026-04-24 完了）

✅ ミッション完了

### 統計サマリー

| 項目 | 結果 |
|------|------|
| 入力 URL | 1,589 件 |
| 電話番号検出 | 866 件（54.6%） |
| invalid | 415 件 |
| skipped | 4 件 |
| 実行時間 | 約 7 時間 |
| 保存先 | Google Sheet Phase 5 + phase5_data.db |

### 処理内容

- ✅ 1,589 件の企業ウェブサイトをクロール
- ✅ 優先度順で電話番号を抽出
- ✅ メールアドレスも同様に抽出
- ✅ 866 件を phase5_data.db に永続化
- ✅ Google Sheet Phase 5 に同期完了
- ✅ ステータス「ready_to_contact」でマーク

### 成果物

- 📊 Google Sheet Phase 5：866 行
- 💾 Database：logs/phase5_data.db（1,589 レコード）
- 📝 ログ：logs/website_scraper.log
- 📚 ドキュメント：docs/ フォルダ

---

## Phase 6: ZeroBounce メール検証（完成）

### 役割

Phase 5 で抽出したメールアドレスを ZeroBounce API で検証し、バウンスリスク除外

### 検証結果

- valid: 約 800 件
- catch-all: 約 200 件
- invalid: 約 400 件
- do_not_mail: 約 150 件（スパムリスト登録）
- test_email: 約 39 件（テスト用ドメイン）

### クレジット管理

- 無料枠: 月 100 件
- 使用状況: 99/100
- クレジット切れ時: スクリプト中断 → https://zerobounce.net/ で課金 → 再実行

### DB スキーマ追加

- validation_status: 検証結果（valid/catch-all/invalid/do_not_mail等）
- validation_score: 信頼スコア（0-100）
- validation_at: 検証実行日時

### 実行コマンド

python bounce_checker.py 10      # テスト（10 件）
python bounce_checker.py 1589    # 本番（全件、クレジット消費）

### クレジット切れ時の対応

1. ZeroBounce にアクセス: https://www.zerobounce.net/
2. Billing → Add Credits で追加
3. 再実行: python bounce_checker.py 1589

---

## Phase 7: メール送信改善（完成）

### 改善内容

- Phase 6 検証結果で invalid/do_not_mail/insufficient_credits を送信対象から除外
- send_email.py に検証結果チェック機能追加
- crm_manager.py の get_pending_leads() にフィルタ機能追加

### 除外ロジック

検証ステータスが以下の場合はスキップ＆ログ:
- invalid
- do_not_mail
- abuse
- test_email
- error
- insufficient_credits

### 送信対象判定基準

以下をすべて満たす場合に送信:
1. ランク A または B
2. NGフラグ = FALSE
3. バウンスフラグ = FALSE
4. 営業ステータスが「失注」「成約」「NG」でない
5. メールアドレス有効
6. Phase 6 検証結果が valid または catch-all
7. 送信回数 = 0 または 最終送信日から 4 日以上経過かつ送信回数 < 4

### 実行コマンド

python send_email.py --dry-run --limit=20   # 確認
python send_email.py --limit=20              # 実行

---

## セットアップ

### 前提条件

- Python 3.9 以上
- Windows 10/11 PowerShell
- Google Cloud サービスアカウント

### パッケージインストール

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install google-auth google-api-python-client gspread requests beautifulsoup4 selenium google-generativeai python-dotenv

### 環境変数設定 (.env)

GOOGLE_SERVICE_ACCOUNT_JSON=credentials/service_account.json
GMAIL_SENDER_ADDRESS=marketing@luvira-biz.jp
SPREADSHEET_ID=<CRM スプシ ID>
SPREADSHEET_ID_PHASE5=<Phase 5 スプシ ID>
GEMINI_API_KEY=<Gemini キー>
YOUTUBE_API_KEY=<YouTube キー>
ZEROBOUNCE_API_KEY=52ed2d2a55b349efa630d2b99fd40475
SMTP_PASSWORD=<パスワード>
IMAP_PASSWORD=<パスワード>
LOG_LEVEL=INFO

---

## トラブルシューティング

### ZeroBounce クレジット切れ

https://www.zerobounce.net/ でチャージし再実行

### Google API 認証エラー

- credentials/service_account.json の存在確認
- .env の GOOGLE_SERVICE_ACCOUNT_JSON パス確認
- サービスアカウントメール権限確認

### メール送信エラー

Get-Content logs/send_email.log | Select-String "error"

---

## ドキュメント

- docs/INDEX.md - ドキュメント一覧
- docs/CURRENT_STATUS.md - プロジェクト状況
- docs/PHASE5_GUIDE.md - Phase 5 ガイド
- docs/PHASE6_GUIDE.md - Phase 6 ガイド
- docs/OPERATION_GUIDE.md - 運用ガイド

---

**最終更新:** 2026‑04‑24
**ステータス:** ✅ Phase 1～7 完成、本番運用準備完了
