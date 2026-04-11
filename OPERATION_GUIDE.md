# 営業自動化プロジェクト - 運用ガイド

## Phase 2 ウォームアップ & バウンス管理

### 📊 実装完了確認

| 項目 | ファイル | ステータス | 確認日 |
|------|---------|----------|------|
| SQLite ログ管理 | db_manager.py | ✅ | 2026-04-08 |
| ウォームアップスケジュール | send_email.py / config.py | ✅ | 2026-04-08 |
| バウンス監視 & 集計 | bounce_checker.py | ✅ | 2026-04-11 |
| 週次レビュー & 判定 | weekly_report.py | ✅ | 2026-04-08 |
| 日次運用自動化 | daily_operations.py | ✅ | 2026-04-11 |
| メール間隔ランダム化 | send_email.py | ✅ | 2026-04-11 |

---

## 📅 日次運用スケジュール

| 時刻 | スクリプト | 説明 | 実行方式 |
|------|-----------|------|--------|
| 09:00 | python daily_operations.py | バウンスチェック → メール送信 | Task Scheduler 自動 |
| 01:00 | python bounce_checker.py | バウンスメール集計・DB更新 | 手動/Task Scheduler |
| 月朝 | python weekly_report.py | バウンス率分析・上限決定 | 手動/Task Scheduler |

---

## 🔄 実行手順

### 1. メール送信実行

**基本コマンド**:
\\\
python send_email.py --limit 10
\\\

**オプション詳細**:
- \--limit N\: 送信件数を指定（デフォルト: 自動計算）
- \--wait N\: メール間隔を秒単位で指定（デフォルト: 1200秒=20分）
- \--dry-run\: テスト実行（実際には送信しない、待機は実行される）

**実行例**:
\\\powershell
python send_email.py --limit 10                    # 日次10件、20分間隔（ランダム±50%）
python send_email.py --limit 5 --wait 1800        # 5件送信、30分間隔（ランダム±50%）
python send_email.py --limit 3 --dry-run --wait 60  # ドライラン、60秒間隔テスト
\\\

### 2. バウンスチェック実行

\\\
python bounce_checker.py
\\\

**動作**:
- IMAP で本日のバウンスメール（Mail Delivery Subsystem など）を自動検出
- 検出メールに **フラグを付与**（フォルダ移動なし）
- SQLite DB に日次統計を記録（送信数・バウンス数・バウンス率）

毎日深夜 01:00 に自動実行推奨（本番環境では Task Scheduler 対応予定）

### 3. 週次レビュー実行

\\\
python weekly_report.py
\\\

**動作**:
- 直近 7 日間のバウンス統計を集計
- バウンス率に基づいて次週の上限を判定
- Aggressive mode の推奨判定

毎週月曜朝に実行推奨

---

## ⏱️ メール送信間隔（2026-04-11 更新）

### 基本設定
- **基本間隔**: 1200秒 (20分)
- **ランダムばらつき**: ±50% (0.5倍～1.5倍)
- **最短間隔**: 600秒 (10分)
- **最長間隔**: 1800秒 (30分)

### ランダムばらつきの仕組み
各メール送信間に、基本間隔にランダムな倍数（0.5～1.5）を掛けることで、より自然な送信パターンを実現し、スパム判定を回避します。

**実行例**:
- メール 1 → メール 2: 55秒（基本60秒 × 0.917倍）
- メール 2 → メール 3: 83秒（基本60秒 × 1.383倍）

### 修正履歴
- **2026-04-11**: 基本間隔 10分 → 20分、ランダムばらつき ±50% を実装

---

## 📊 ウォームアップスケジュール

| 週 | 開始日 | 終了日 | 上限 | 進捗条件 |
|----|-------|-------|------|--------|
| 1 | 2026-04-07 | 2026-04-13 | 10件/日 | - |
| 2 | 2026-04-14 | 2026-04-20 | 15件/日 | バウンス率 < 2% |
| 3 | 2026-04-21 | 2026-04-27 | 20件/日 | バウンス率 < 2% |
| 4 | 2026-04-28 | 2026-05-04 | 25件/日 | バウンス率 < 2% |
| 5+ | 2026-05-05～ | - | 25件/日 | 固定（Aggressive mode で最大 30件/日） |

### バウンス率判定ロジック
- **< 2%**: ✅ 次週 +5件/日 に増加
- **2～5%**: ⚠️ 次週据え置き（リスト精査推奨）
- **> 5%**: 🔴 次週 -5件/日 に減少（SMTP/DNS 確認推奨）

---

## 🔧 バウンス管理

### 自動処理フロー
1. 毎日 01:00: \ounce_checker.py\ 実行
2. IMAP でバウンスメール（以下の条件）を自動検出:
   - 送信元: Mail Delivery Subsystem / Mailer-Daemon
   - 件名: Mail delivery failed / Undelivered Mail / Returned mail など
   - ステータスヘッダ: 5.x.x
3. 検出メールに **Flagged フラグを付与**
4. SQLite DB (\logs/send_log.db\) に統計を記録

### バウンスメール確認方法
\\\powershell
python -c "
import sqlite3
conn = sqlite3.connect('logs/send_log.db')
c = conn.cursor()
c.execute('SELECT date, sent_count, bounce_count, bounce_rate FROM bounce_log ORDER BY date DESC LIMIT 7')
for row in c.fetchall():
    print(f'{row[0]}: 送信{row[1]}件 → バウンス{row[2]}件 ({row[3]:.2f}%)')
conn.close()
"
\\\

---

## ⚙️ 環境設定

### .env に必須項目

\\\
# YouTube & Google API
YOUTUBE_API_KEY=（YouTube Data API v3 キー）
GOOGLE_SHEETS_ID=（Google Sheets ID）
GEMINI_API_KEY=（Google Gemini API キー）

# SMTP 設定（送信）
SMTP_USER=marketing@luvira-biz.jp
SMTP_PASSWORD=（Xserver メールパスワード）

# IMAP 設定（バウンス監視）
IMAP_HOST=sv16675.xserver.jp
IMAP_PORT=993
IMAP_USER=marketing@luvira-biz.jp
IMAP_PASSWORD=（同上パスワード）
\\\

### 確認コマンド
\\\powershell
Get-Content ".env" -Encoding UTF8 | Select-String "IMAP|SMTP"
\\\

---

## 🚨 トラブルシューティング

### SMTP エラー: "Client host rejected: Access denied"

**原因**: IP ウォームアップ初期段階でドメイン/IP がブロック
**対処**:
1. \python test_email.py\ で単体テスト送信
2. エラーが続く場合は Xserver サポート確認
3. 数時間～1日待機後に再試行

### IMAP エラー: "NoneType object has no attribute 'replace'"

**原因**: \IMAP_PASSWORD\ が .env に設定されていない
**対処**:
1. \
otepad .env\ で .env を開く
2. \IMAP_PASSWORD=（パスワード）\ を追加
3. \python bounce_checker.py\ で再実行

### ドライラン時に待機が実行されない

**原因**: 旧バージョン使用
**対処**: \git pull origin main\ で最新版を取得（コミット 89ee952 以降）

---

## 📝 Git コミット履歴

| コミット | メッセージ | 日時 |
|---------|----------|------|
| 89ee952 | fix: enable wait_between_sends for dry-run mode to verify random intervals | 2026-04-11 |
| dd5c25c | feat: increase email interval to 20min with ±50% randomness | 2026-04-11 |
| 3207c74 | fix: bounce_checker.py - add dotenv load_dotenv for proper .env loading | 2026-04-11 |
| 5ea08eb | feat: add daily_operations.py for automated bounce check and email sending | 2026-04-11 |
| a2200de | docs: add operation guide for warmup and bounce management | 2026-04-11 |

---

## ✅ 本番運用開始（2026-04-11 確認）

- ✅ Task Scheduler 設定完了: \DailyEmailOperations\ 毎日 09:00 実行
- ✅ ランダム間隔動作確認: ±50% ばらつき実装・テスト済み
- ✅ ドライラン動作確認: 待機実行確認済み
- ✅ バウンスチェック動作確認: IMAP 接続 & DB 記録確認済み

**明日 (2026-04-12) 09:00** から本番運用開始予定。
