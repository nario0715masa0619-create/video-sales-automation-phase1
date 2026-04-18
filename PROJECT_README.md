# video-sales-automation-phase1 設計書  
最終更新：2026-04-18

---

## ディレクトリ

D:\AI_スクリプト成果物\営業自動化プロジェクト\video-sales-automation-phase1

---

## 主要ファイル

| ファイル名          | 役割                                               |
|--------------------|----------------------------------------------------|
| orchestrator.py    | メイン実行（--mode run / dry-run / email-only）    |
| target_scraper.py  | YouTubeスクレイピング（最新動画タイトル取得含む） |
| scorer.py          | ICPスコアリング（A/B/Cランク付け、CRM向けdict生成）|
| crm_manager.py     | Google Sheets（ミニCRM）操作                       |
| email_generator.py | Geminiによる営業メール本文生成（1〜4通目）        |
| email_sender.py    | メール送信管理（get_email_sender(\"xserver\")）    |
| smtp_sender.py     | Xserver SMTP送信テスト                             |
| config.py          | 環境変数・設定値管理                               |
| PROJECT_README.md  | 本ファイル（設計・運用メモ）                       |

---

## 認証ファイル

| ファイル                          | 用途              |
|----------------------------------|-------------------|
| credentials/service_account.json | Google Sheets用   |
| credentials/gmail_credentials.json | Gmail OAuth用   |
| credentials/gmail_token.json     | Gmail OAuthトークン |

---

## .env 確定設定（現状）

> ※ SMTP パスワード名は `SMTP_PASSWORD` に統一すること

```env
GEMINI_MODEL=gemini-2.0-flash

# Xserver SMTP設定
SMTP_HOST=sv16675.xserver.jp
SMTP_PORT=587
SMTP_USER=biz@luvira.co.jp
SMTP_PASSWORD=（実際のパスワード）
MAIL_FROM=biz@luvira.co.jp

# メール送信上限（テスト時は 1、本番は 20 推奨）
EMAIL_MAX_SEND_PER_RUN=20

# Google Sheets
SPREADSHEET_ID=1rDy0s25zJreMIlmePgT7CNnhOOHDvcue0_RbXdQdhRg

# 自社情報（署名用）
MYCOMPANYNAME=株式会社ルヴィラ
MYNAME=成相
MYTITLE=マーケティング担当
MYPHONE=070-5595-9523
MYWEBSITE=https://luvira.co.jp

---

## パイプライン統合情報（2026-04-17 更新）

### 3 つのメインパイプライン

#### パイプライン 1: YouTube チャンネル収集 (collect.py)
**役割:** YouTube から営業対象チャンネルを検索・フィルタ・スコアリングして CRM に登録

**入力:** config.py の KEYWORDS（12 個）
**出力:** Google Sheets CRM シート（新規行）

**実行コマンド:**
- python collect.py --dry-run (テスト実行)
- python collect.py (本番実行)

**処理ステップ:**
1. Step 1: YouTube 検索（API quota: 100 pt/keyword × 12 = 1,200 pt）
2. Step 2: チャンネル詳細情報取得（50 pt）
3. Step 3: ICP フィルタリング（ローカル処理）
4. Step 4: 重複排除（ローカル処理）
5. Step 5: A/B/C スコアリング（ローカル処理）
6. Step 6: メール・公式サイト URL 抽出（ローカル処理）
7. Step 7: Google Sheets CRM に upsert

**本日実績:** 215 件新規追加（重複除外）

---

#### パイプライン 2: 営業メール自動送信 (send_email.py)
**役割:** CRM のペンディングリードに対して営業メールを自動生成・送信

**入力:** Google Sheets CRM（ペンディングリード）
**出力:** メール送信ログ + Google Sheets メール履歴タブ

**実行コマンド:**
- python send_email.py --limit 3 --dry-run (テスト実行)
- python send_email.py --limit 3 (本番実行)
- python daily_operations.py (自動スケジューラ)

**処理ステップ:**
1. get_pending_leads() で CRM から全ペンディングリード取得
2. [:daily_limit] でスライス（日次上限を適用）
3. ループで 1 件ずつ処理：
   - Gemini で営業メール本文生成
   - Xserver SMTP で送信
   - 送信ログを SQLite DB に記録
   - 待機（デフォルト: 20 分 ± 50%）

**本日実績:** 3 件送信成功（SMTP: Xserver）

---

#### パイプライン 3: 電話番号スクレイピング (website_scraper.py)
**役割:** CRM の公式サイト URL から電話番号を抽出し Phase 5 シートに保存

**入力:** Google Sheets CRM（公式サイト URL）
**出力:** Google Sheets Phase 5 シート（電話番号）

**実行コマンド:**
- python website_scraper.py --limit 50 (テスト実行)
- python website_scraper.py (本番実行)

**処理ステップ:**
1. CRM から公式サイト URL を取得
2. Requests / Playwright でサイトをスクレイピング
3. 正規表現で電話番号を抽出
4. Phase 5 シートに保存

**過去実績:** 863 件の電話番号を抽出（1,511 件サイト処理）
**ステータス:** 実装済みだが、send_email.py 統合パイプラインに未組込

---

## 主要スクリプト一覧（2026-04-17）

| スクリプト | 役割 | ステータス | 最終実行日 |
|-----------|------|----------|---------|
| collect.py | YouTube 検索 → CRM 保存 | 動作中 | 2026-04-17 |
| send_email.py | CRM 読取 → メール送信 | 動作中 | 2026-04-17 |
| website_scraper.py | サイトスクレイピング → Phase 5 | 実装済 | 過去 |
| daily_operations.py | 日次自動化スケジューラ | 動作中 | 2026-04-17 |
| bounce_checker.py | バウンスメール検出 | 動作中 | 2026-04-17 |
| email_generator.py | Gemini で営業メール生成 | 警告あり | 2026-04-17 |
| crm_manager.py | Google Sheets 操作 | 復元済 | 2026-04-17 |
| cache_manager.py | キャッシュ管理（JSON） | 復元済 | 2026-04-17 |

---

## 既知の問題・改善待ち（2026-04-17）

| 問題 | ファイル | 優先度 | 対応方法 |
|------|---------|------|--------|
| google.generativeai 非推奨警告 | email_generator.py (line 25) | 高 | google.genai への移行 |
| Gemini API ResourceExhausted | email_generator.py | 高 | リトライロジック・レート制限改善 |
| email_extractor.py SyntaxWarning | email_extractor.py (line 103, 106) | 中 | エスケープシーケンス修正 |
| Phase 5 パイプライン未統合 | website_scraper.py | 中 | send_email.py との統合設計 |


