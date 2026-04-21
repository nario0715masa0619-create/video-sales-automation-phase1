# WEBSITE_URL_FETCHER_DESIGN.md

## 概要

複数のソースから company_name と website_url を統一インターフェイスで取得するモジュール。

Phase 5 以降で、Google 検索、ファイル読み込みなど複数ソースに対応予定。

## 目的

現在の Phase 1 では、CRM または YouTube チャンネルから website_url を取得しているが、

Phase 5 では以下の複数ソースから URL を取得する必要がある：

- CRM（現在実装済み）
- Google 検索（仮実装）
- CSV/JSON ファイル（仮実装）

**このモジュールは、URL 取得ソースを統一インターフェイスで切り替え可能にする設計。**

## アーキテクチャ

### 統一インターフェイス

\\\python
from tools.website_url_fetcher import get_website_urls

# CRM から取得
urls = get_website_urls(source='crm', limit=10)

# Google 検索から取得（将来実装）
urls = get_website_urls(source='google_search', company_names=['Cybozu', 'Example'])

# ファイルから取得（将来実装）
urls = get_website_urls(source='file', filepath='companies.csv')
\\\

### 戻り値形式

\\\python
List[Tuple[int, str, str]]
# [(idx, website_url, company_name), ...]
\\\

## 実装状況

### ✅ 実装済み

**source='crm'**
- CRM の read_website_urls_from_crm() を使用
- チャンネルURL など任意の列から URL 取得可能
- パラメータ:
  - limit: 取得件数上限
  - url_column: URL 列名（デフォルト: 'チャンネルURL'）
  - name_column: 会社名列名（デフォルト: '会社名'）

### ⏳ 仮実装（Phase 5 で実装予定）

**source='google_search'**
- ログに「未実装」と出力するだけ
- パラメータ:
  - company_names: 検索する会社名リスト
  - max_results: 1 検索あたりの結果数
- 実装予定：Playwright/Selenium で Google 検索を自動化

**source='file'**
- ログに「未実装」と出力するだけ
- パラメータ:
  - filepath: ファイルパス
  - url_column: URL 列名
  - name_column: 会社名列名
- 実装予定：CSV/JSON 読み込み

## 使用例

### Phase 1（現在）

collect.py では YouTube チャンネルから URL を抽出しているため、このモジュールは使用しない。

### Phase 5（将来）

\\\python
# 新規スクリプト: scrape_websites.py

from tools.website_url_fetcher import get_website_urls
from tools.email_extractor import get_email_from_website
from tools.phone_extractor import extract_phone

# CRM から URL を取得
urls = get_website_urls(source='crm', limit=100)

# 各 URL から email + phone を抽出
for idx, website_url, company_name in urls:
    email = get_email_from_website(website_url)
    phone = extract_phone(website_url)
    
    # Google Sheets Phase 5 に保存
    save_to_phase5(company_name, phone, email, website_url)
\\\

## 拡張性

新しいソースを追加する場合：

1. _fetch_from_xxx() 関数を追加
2. get_website_urls() の if-elif に条件を追加

\\\python
elif source == 'new_source':
    return _fetch_from_new_source(**kwargs)
\\\

## ファイル構成

- tools/website_url_fetcher.py - 統一インターフェイス
- tools/google_search_scraper.py - Google 検索実装（未作成）
- tools/csv_reader.py - CSV/JSON 読み込み（未作成）

## 関連モジュール

- crm_manager.py - CRM 操作（read_website_urls_from_crm）
- email_extractor.py - メール抽出（YouTube チャンネル用）
- phone_extractor.py - 電話番号抽出
