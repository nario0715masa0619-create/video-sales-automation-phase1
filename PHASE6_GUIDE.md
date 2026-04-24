# Phase 6 実行ガイド：ZeroBounce メール検証

## 概要

Phase 6 は、Phase 5 で抽出したメールアドレスを ZeroBounce API で検証し、有効/無効を判定します。

検証結果は `phase5_data.db` の 3 つのカラムに保存されます：
- `validation_status`：検証結果（valid, invalid, catch-all, do_not_mail など）
- `validation_score`：信頼度スコア（0-100）
- `validation_at`：検証日時

---

## 前提条件

### 1. ZeroBounce アカウント登録 ✅ 完了

- **登録メール**: tech@luvira-biz.jp
- **API キー**: 52ed2d2a55b349efa630d2b99fd40475
- **プラン**: 無料枠（月 100 件）
- **保存場所**: .env ファイルに `ZEROBOUNCE_API_KEY=52ed2d2a55b349efa630d2b99fd40475`

### 2. Phase 5 が完了 ⏳ 進行中

現在 68%（1,089/1,589 件）
推定完了時間：数時間

### 3. Python 環境に requests をインストール

python -m pip install requests

---

## 実行方法

### ステップ 1: Phase 5 完了を待つ

python -c "import sqlite3; conn=sqlite3.connect('logs/phase5_data.db'); cur=conn.cursor(); cur.execute('SELECT COUNT(*) FROM phase5_data'); print(f'進捗: {cur.fetchone()[0]}/1589'); conn.close()"

完了目標：1589/1589

---

### ステップ 2: DB スキーマ確認

検証結果を保存するカラムが存在するか確認：

python -c "import sqlite3; conn=sqlite3.connect('logs/phase5_data.db'); cur=conn.cursor(); cur.execute('PRAGMA table_info(phase5_data)'); [print(col[1]) for col in cur.fetchall()]; conn.close()"

出力例：
- id
- company_name
- website_url
- phone_number
- email
- status
- scraped_at
- updated_at
- validation_status ← 必須
- validation_score ← 必須
- validation_at ← 必須

---

### ステップ 3: テスト実行（最初の 10 件）

python bounce_checker.py 10

出力例：
2026-04-24 16:00:00 | INFO | 📧 10 件のメールアドレスを検証開始
2026-04-24 16:00:01 | INFO | [1/10] 会社A | email1@example.com
2026-04-24 16:00:02 | INFO |    ✅ 有効 (status: valid, スコア: 0)
2026-04-24 16:00:03 | INFO | [2/10] 会社B | email2@example.com
2026-04-24 16:00:04 | INFO |    ❌ 無効 (do_not_mail, スコア: 0)
...
2026-04-24 16:00:20 | INFO | ================================================================================
2026-04-24 16:00:20 | INFO | ✅ 検証完了: 有効 5件 / 無効 5件 / エラー 0件 / テスト除外 0件

---

### ステップ 4: 本格実行（全件検証）

python bounce_checker.py 1589

⚠️ 注意：月額クレジット（無料枠 100 件）を消費します。
推定時間：1589 件 × 1 秒 = 約 26 分

---

## 検証結果の確認

### 検証結果を集計

python -c "import sqlite3; conn=sqlite3.connect('logs/phase5_data.db'); cur=conn.cursor(); cur.execute('SELECT validation_status, COUNT(*) FROM phase5_data WHERE validation_status IS NOT NULL GROUP BY validation_status'); [print(f'{r[0]}: {r[1]} 件') for r in cur.fetchall()]; conn.close()"

出力例：
valid: 800 件
catch-all: 200 件
invalid: 400 件
do_not_mail: 150 件
test_email: 39 件

### 送信対象の有効メール件数

python -c "import sqlite3; conn=sqlite3.connect('logs/phase5_data.db'); cur=conn.cursor(); cur.execute('SELECT COUNT(*) FROM phase5_data WHERE validation_status IN ("valid", "catch-all")'); print(f'送信対象メール: {cur.fetchone()[0]} 件'); conn.close()"

---

## クレジット切れの場合

### 症状

2026-04-24 16:30:00 | ERROR | 🚨 ZeroBounce クレジット切れで中断しました

### 対応

1. ZeroBounce ダッシュボードにログイン
   https://www.zerobounce.net/

2. Billing → Add Credits からクレジットをチャージ

3. 検証を再開
   python bounce_checker.py 1589

---

## Phase 7（メール送信）への影響

### 送信前のチェック

send_email.py 実行時、以下の条件で送信対象を自動フィルタリング：

- validation_status = 'valid' → 送信 OK
- validation_status = 'catch-all' → 送信 OK
- validation_status = 'invalid' → 送信 NG（除外）
- validation_status = 'do_not_mail' → 送信 NG（除外）
- validation_status = 'insufficient_credits' → 送信 NG（クレジット切れ検証待ち）
- validation_status = None（未検証） → 送信 OK（検証待ち）

### 実行コマンド

Phase 6 検証完了後：

python send_email.py --limit 20

---

## トラブルシューティング

### Q: テストメール（sample@xx.co.jp など）も検証されている

A: bounce_checker.py で自動除外されています。
   output: ⚠️ テスト用メールアドレス（除外）

### Q: validation_status が NULL のメールが多い

A: Phase 5 でメールアドレスが抽出されなかった、または検証がまだです。
   確認: SELECT COUNT(*) FROM phase5_data WHERE email IS NULL

### Q: ZeroBounce API エラーが出た

A: ネットワーク接続またはタイムアウトの可能性。
   対応: python bounce_checker.py 10 で少数件から再試行

---

**更新日**: 2026-04-24
**ステータス**: 実行準備完了
