# video-sales-automation-phase1 設計書  
最終更新：2026-03-20

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
