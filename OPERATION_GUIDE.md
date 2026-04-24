# 日次運用マニュアル（OPERATION_GUIDE）

営業自動化プロジェクトの日次運用フロー、実行コマンド、監視方法をまとめたガイドです。

---

## 日次運用フロー

### 朝（9:00）：daily_operations.py で自動実行開始

Windows タスクスケジューラまたは手動で以下を実行：

python daily_operations.py

**実行内容:**
1. bounce_checker.py：昨日のバウンスメール検出
2. send_email.py：本日のペンディングリードにメール送信（20～30 件）
3. daily_metrics_logger.py：本日の送信結果を記録

**実行時間:**
- 初回実行：約 30 分（20 件送信 × 20 分待機）
- 推定完了：9:30 頃

---

### 昼（12:00）～夜（18:00）：手動確認

#### 1. 送信ログ確認

Get-Content logs/send_email.log | Select-Object -Last 50

確認項目：
- 本日の送信件数
- バウンスリスク除外件数
- エラーの有無

#### 2. 日次メトリクス確認

python daily_metrics_logger.py

出力：
📊 Daily Metrics for 2026-04-24
  Raw: 18 | Valid: 10 | Sent: 20 | Replies: 2 | Deals: 0

#### 3. バウンス率確認

python -c "import sqlite3; conn=sqlite3.connect('logs/send_email.db'); cur=conn.cursor(); cur.execute('SELECT COUNT(*) FROM send_log WHERE status="bounce" AND DATE(sent_at) = DATE("now")'); print(f'本日バウンス: {cur.fetchone()[0]} 件'); conn.close()"

---

### 夜（20:00）：日次レポート確認

#### 1. 本日の統計

Get-Content logs/daily_metrics.jsonl | Select-Object -Last 1

#### 2. Google Sheet の日次ログシート確認

- 「日次ログシート」タブで本日のデータ確認
- Raw取得数、有効数、送信数が期待値か確認

---

## 週次運用（金曜 18:00）

### 1. 週次メトリクス集計

python weekly_analytics.py

出力：
📊 Weekly Report (Week 1: 2026-04-22 ~ 2026-04-26)
- 送信件数: 150 件
- バウンス率: 12%
- 開封率: 18%
- 返信率: 2.1%

### 2. A/B テスト結果確認

- 件名 A/B：どちらの開封率が高かったか
- 送信時間帯：夜間 vs 朝間
- 配分比率：1 回目 70% / 2 回目以降 30% の効果

### 3. 週次レポート作成

テンプレート使用：
- タイトル：「営業メール週次ログ (Week X)」
- 施策・軌道修正セクション
- 来週のテーマ決定

---

## 月次運用（月末 17:00）

### 1. 月次 KPI 集計

python monthly_review_generator.py

出力：
📊 Monthly Review (2026-04-01 ~ 2026-04-30)

| KPI | 4月 | 目標 | 達成度 |
|-----|-----|------|--------|
| 実送信件数 | 650 件 | 500-800 | ✅ 達成 |
| 総バウンス率 | 14% | 10-20% | ✅ 達成 |
| 開封率 | 19% | 15-25% | ✅ 達成 |
| 返信率 | 2.2% | 1-3% | ✅ 達成 |
| 商談化率 | 0.4% | 0.2-1% | ✅ 達成 |

### 2. 所感・改善アクション記述

- 4 月の成果：「返信率 2.2%、目標達成」
- 改善点：「初回メール の開封率が 18%（目標 15%）で安定」
- 来月の注力：「2 回目メールの返信率向上テスト」

### 3. 月次レポート確定・共有

Google Sheet「月次レビュー」タブにコピー&ペースト

---

## トラブル対応フロー

### パターン 1：送信がスキップされる場合

#### 原因チェック

1. バウンスリスク除外か確認
   python -c "import sqlite3; conn=sqlite3.connect('logs/phase5_data.db'); cur=conn.cursor(); cur.execute('SELECT email, validation_status FROM phase5_data WHERE email="your-email@example.com" LIMIT 1'); print(cur.fetchone()); conn.close()"

   結果が (email, 'invalid') や (email, 'do_not_mail') なら除外対象

2. CRM のフラグを確認
   - NG フラグ = FALSE
   - バウンスフラグ = FALSE
   - 営業ステータス ≠ 失注/成約/NG

#### 対応

- バウンス判定が誤っている場合：CRM で validation_status をクリア
- NG フラグが間違っている場合：CRM で修正

---

### パターン 2：ZeroBounce クレジット切れ

#### 症状

2026-04-24 16:30:00 | ERROR | 🚨 ZeroBounce クレジット切れで中断しました

#### 対応

1. https://www.zerobounce.net/ にログイン
2. Billing → クレジットをチャージ
3. 再実行：python bounce_checker.py 1589

---

### パターン 3：メール送信がエラー

#### 症状

❌ 会社A へメール送信失敗

#### 原因チェック

Get-Content logs/send_email.log | Select-String "会社A"

#### 対応

- SMTP 接続エラー：ネットワーク確認
- Gemini API エラー：API キー確認、リトライ
- メール本文生成エラー：email_generator.py ログ確認

---

## 監視項目チェックリスト

### 毎日確認

- [ ] 送信ログにエラーがないか
- [ ] 本日の送信件数が期待値か（ウォームアップスケジュール準拠）
- [ ] バウンス率が 20% を超えていないか

### 毎週確認

- [ ] 返信数が期待値か
- [ ] 返信の質は良好か（ポジティブ率 40% 以上）
- [ ] A/B テスト結果は出ているか

### 毎月確認

- [ ] 商談化件数は期待値か
- [ ] KPI は全て達成目標内か
- [ ] 改善アクションは実行できたか

---

## よくあるコマンド集

### 送信ログ確認

Get-Content logs/send_email.log | Select-String "✅" | Measure-Object -Line

### バウンス数確認

python -c "import sqlite3; conn=sqlite3.connect('logs/phase5_data.db'); cur=conn.cursor(); cur.execute('SELECT COUNT(*) FROM phase5_data WHERE validation_status = "do_not_mail"'); print(f'do_not_mail: {cur.fetchone()[0]}'); conn.close()"

### 本日の送信件数確認

python daily_metrics_logger.py | Select-String "Sent:"

### Google Sheet に記録されているか確認

# CRM から最新 5 行を取得
python -c "from crm_manager import get_crm; leads = get_crm().get_all_leads(); [print(f'{lead.get("会社名")}: {lead.get("最終送信日")}') for lead in leads[-5:]]"

---

## 参考：ウォームアップスケジュール

| 週 | 日次上限 | 推定月間 | 開始予定 |
|---|---------|---------|---------|
| 1 | 10 件 | 70 件 | 2026-04-07 |
| 2 | 15 件 | 105 件 | 2026-04-14 |
| 3 | 20 件 | 140 件 | 2026-04-21 |
| 4+ | 25-30 件 | 175-210 件 | 2026-04-28 |

---

**更新日**: 2026-04-24
**対象者**: 営業チーム・オペレーター
**ステータス**: 本番運用開始準備完了
