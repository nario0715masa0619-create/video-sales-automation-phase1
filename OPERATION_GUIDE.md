# 営業自動化プロジェクト - 運用ガイド

## Phase 2 ウォームアップ & バウンス管理

### 📊 実装完了確認

| 項目 | ファイル | 状態 |
|------|---------|------|
| SQLite ログ管理 | db_manager.py | ✅ |
| ウォームアップスケジュール | send_email.py / config.py | ✅ |
| バウンス監視 & 集計 | bounce_checker.py | ✅ |
| 週次レビュー & 判定 | weekly_report.py | ✅ |

---

## 📅 日次運用スケジュール

| 時刻 | スクリプト | 説明 |
|------|-----------|------|
| 09:00 | `python send_email.py --limit 10` | メール送信（日次） |
| 01:00 | `python bounce_checker.py` | バウンスチェック（深夜） |
| 月朝 | `python weekly_report.py` | 週次レビュー |

---

## 🔄 実行手順

### 1. メール送信実行

`python send_email.py --limit 10`

**オプション:**
- `--limit N`: 送信件数を指定（デフォルト: 10）
- `--dry-run`: テスト実行（実際には送信しない）

### 2. バウンスチェック実行

`python bounce_checker.py`

毎日深夜 01:00 に自動実行推奨

### 3. 週次レビュー実行

`python weekly_report.py`

毎週月曜朝に実行

---

## ⚙️ 設定確認

### .env に必須項目

YOUTUBE_API_KEY=xxx
GOOGLE_SHEETS_ID=xxx
GEMINI_API_KEY=xxx
SMTP_USER=marketing@luvira-biz.jp
SMTP_PASSWORD=xxx
IMAP_HOST=sv16675.xserver.jp
IMAP_PORT=993
IMAP_USER=marketing@luvira-biz.jp
IMAP_PASSWORD=xxx

---

## 🚨 トラブルシューティング

### SMTP エラー: Client host rejected

原因: ドメイン運用初期段階で IP ブロック
対策: test_email.py で単体テスト実行

### IMAP エラー: NoneType object

原因: IMAP_PASSWORD が .env に設定されていない
対策: .env に IMAP_PASSWORD を設定

---

## 📊 ウォームアップスケジュール

| 週 | 期間 | 上限 |
|---|------|------|
| 1週目 | 運用開始～7日 | 10件/日 |
| 2週目 | 8～14日 | 15件/日 |
| 3週目 | 15～21日 | 20件/日 |
| 4週目 | 22～28日 | 25件/日 |
| 5週目～ | 29日以降 | 25件/日 |

バウンス率 2% 未満の場合のみ次週に進める
