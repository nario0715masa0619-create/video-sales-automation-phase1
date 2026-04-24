# 電話番号・メール・会社名抽出パイプライン設計書

## 1. 概要
CRM、Google 検索、ファイルなど複数のソースから URL を取得し、
汎用的にスクレイピングして以下の情報を抽出する：
- 会社名
- 電話番号
- メールアドレス
結果を Google Sheets に保存する。

## 2. アーキテクチャ図
【URL ソース層】
├─ CRM から URL + 既存データ取得
├─ Google 検索から URL 取得
└─ CSV/JSON ファイルから URL 読み込み
        ↓ URL リスト
【汎用スクレイピング層】
├─ HTML ダウンロード
├─ 会社名抽出
├─ 電話番号抽出
├─ メールアドレス抽出
└─ キャッシング・リトライ
        ↓ 結果
【保存層】
├─ Google Sheets 保存
└─ ローカル DB 保存

## 3. モジュール構成
ルート
├── phone_extractor_core.py
├── phone_extractor_crm.py
├── phone_extractor_google.py
├── phone_extractor_file.py
└── phone_sheet_saver.py

## 4. Google Sheets スキーマ
company_name | website_url | phone | email | source_page | status
Cybozu Inc.  | https://... | 03... | c... | crm | success
Example AI   | https://... | 050..| i... | google | partial
