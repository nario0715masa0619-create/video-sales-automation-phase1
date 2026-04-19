# Website Scraper v2 - モジュール構成ドキュメント

## 概要
複数モジュールに分割された Web スクレイピングシステム。各モジュールは独立した役割を持つ。

---

## 1. config.py - 設定ファイル

**役割**: 設定値と定数を一元管理

**含まれる内容**:
- Google Sheets ID・シート名
- スキップ対象 URL パターン
- 優先クロールパス
- 電話番号正規表現パターン（拡張版）
- クロール設定（MAX_PAGES=20）
- HTTP ヘッダー設定

**使用例**: from config import PHONE_PATTERNS, MAX_PAGES
---

## 2. phone_extractor.py - 電話番号抽出

**役割**: HTML から電話番号を抽出

**主要関数**:
- is_valid_phone(phone_str) — 10桁以上チェック
- extract_phone_from_tel_link(soup) — tel: リンクから抽出
- extract_phone_from_regex(html_text) — 正規表現で抽出
- extract_phone_from_jsonld(soup) — JSON-LD から抽出
- extract_phone_from_meta(soup) — メタタグから抽出
- extract_phone(html_text) — 複合的に抽出（優先度順）

**優先度**: tel リンク > JSON-LD > メタタグ > 正規表現

**デバッグ**: ログから「📞」の出力を確認
---

## 3. html_fetcher.py - HTML 取得

**役割**: URL から HTML を取得（複数方法対応）

**主要関数**:
- fetch_html_requests(url) — Requests 使用（高速）
- fetch_html_playwright(url) — Playwright 使用（JS レンダリング）
- fetch_html(url, use_playwright=False) — 統合関数

**使い分け**:
- Requests: 静的コンテンツ、高速処理
- Playwright: JavaScript 実行が必要な場合

**エラーハンドリング**:
- 404 Not Found → None
- タイムアウト → None
- 接続エラー → None
---

## 4. website_crawler.py - クロール処理

**役割**: 同一ドメイン内を深くクロール

**主要関数**:
- crawl_domain(base_url, max_pages=None) — ドメイン内をクロール

**動作**:
1. ベース URL を訪問
2. HTML から全リンクを抽出
3. 同一ドメインのリンクを再訪問
4. max_pages（デフォルト 20）に達するまで繰り返す
5. リンク抽出時は 0.3 秒の遅延を挟む（サーバー負荷軽減）

**戻り値**: 訪問した HTML テキストのリスト
---

## 5. company_info_extractor.py - 企業情報抽出

**役割**: 企業名・説明などのメタ情報を抽出

**主要関数**:
- extract_company_name(html_text, url, crm_company_name=None) — 企業名抽出
- extract_description(html_text) — ディスクリプション抽出

**企業名抽出の優先度**:
1. CRM のデータ（最優先）
2. og:site_name メタタグ
3. og:title メタタグ
4. title タグ
5. H1 タグ
6. ドメイン名から推測（フォールバック）

**ディスクリプション抽出**:
- og:description メタタグ
- description メタタグ
---

## 6. crm_manager.py - Google Sheets 連携

**役割**: Google Sheets API との通信を管理

**主要関数**:
- get_gsheet_client() — クライアント初期化
- read_website_urls_from_crm(limit=None) — CRM から URL リスト読み込み
- append_to_gsheet_phase5(...) — Phase 5 シートにデータ保存

**認証**:
- credentials/service_account.json を使用
- スコープ: https://www.googleapis.com/auth/spreadsheets

**読み込み項目** (CRM):
- Row 0: 企業名
- Row 1: メール
- Row 4: Website URL

**書き込み項目** (Phase 5):
- Column A: 企業名
- Column B: 電話番号
- Column C: Status (ready_to_contact / invalid / skipped)
- Column D: Website URL
- Column E: 処理日時---

## 7. website_scraper_v2.py - メインスクリプト

**役割**: すべてのモジュールを統合して実行

**主要関数**:
- setup_logging() ロギング初期化とRequestsの警告抑制
- should_skip_url(url) スキップ対象URL判定
- scrape_website(url_data) 1つのウェブサイトをスクレイピング
- run_batch_scraping(limit=None) URL全件のバッチ処理
- main() コマンドライン引数解析とエントリーポイント

**処理フロー詳細**:
1. CRM Sheet から Website URL リストを読み込み
2. オプションで limit パラメータで件数を制限
3. 各 URL に対して順序に以下を実行:
   - should_skip_url()でスキップ対象確認
   - fetch_html()でHTML取得
   - crawl_domain()で同一ドメイン内をクロール
   - extract_company_name()で企業名抽出
   - extract_phone()で電話番号抽出
**処理フロー詳細（続き）**:
4. 抽出した情報をもとにStatus判定:
   - 電話番号あり → status = 'ready_to_contact'
   - 電話番号なし → status = 'invalid'
   - スキップ対象 → status = 'skipped'
5. append_to_gsheet_phase5()でPhase 5 Sheetに結果保存:
   - 企業名、電話番号、Status、URL、処理日時を記録
6. 全URL処理後に統計情報を出力:
   - 処理件数
   - 電話番号取得件数
   - 成功率（%）

**実行方法**:
- 全件処理: python website_scraper_v2.py
- 制限あり: python website_scraper_v2.py --limit 10
- 制限あり: python website_scraper_v2.py --limit 50

**ログ出力**:
- website_scraper_v2.log に全ログ記録
- コンソールにもリアルタイム出力
- 各処理ステップが記録される
---

## 依存関係図

website_scraper_v2.py (メイン)
  ├── config.py (設定読み込み)
  ├── phone_extractor.py (電話番号抽出)
  │   └── config.py
  ├── html_fetcher.py (HTML 取得)
  │   └── config.py
  ├── website_crawler.py (クロール)
  │   ├── html_fetcher.py
  │   └── config.py
  ├── company_info_extractor.py (企業情報)
  └── crm_manager.py (Sheets連携)
      └── config.py

---

## デバッグのコツ

**電話番号が抽出されない場合**:
- phone_extractor.py の extract_phone() 関数の優先度を変更
- config.py の PHONE_PATTERNS に新しいパターンを追加
- ログから「📞」の出力を確認して、どのパターンで抽出されたかを確認
- 正規表現をテストして、マッチしているか確認
**HTML が取得できない場合**:
- html_fetcher.py で Playwright を有効にするか検討
- HTTP ステータスコードをログで確認
- User-Agent を変更（config.py の DEFAULT_HEADERS）
- タイムアウト時間を延長（config.py の REQUEST_TIMEOUT）
- リトライロジックを追加することを検討

**クロール深度が足りない場合**:
- config.py の MAX_PAGES を増加（現在 20 ページ）
- website_scraper_v2.py の crawl_domain() 呼び出しで max_pages を指定
- クロールのスリープ時間を短縮（config.py の SLEEP_TIME）
- ただしサーバー負荷に注意

**企業名が取得できない場合**:
- company_info_extractor.py の優先度を調整
- ターゲットサイトの HTML 構造を確認
- og:site_name、title タグなどが存在するか確認
- og:title を優先度に追加することを検討
---

## ファイル一覧と役割

| ファイル | 役割 | 重要度 |
|---------|------|--------|
| config.py | 設定値・定数管理 | 高 |
| phone_extractor.py | 電話番号抽出 | 高 |
| html_fetcher.py | HTML取得 | 高 |
| website_crawler.py | クロール処理 | 高 |
| company_info_extractor.py | 企業情報抽出 | 中 |
| crm_manager.py | Sheets連携 | 高 |
| website_scraper_v2.py | メイン処理 | 高 |

---

## 改善案（将来実装）

1. Playwright の統合実行 - 全サイトでJavaScript実行
2. リトライロジック - 失敗時の自動再試行
3. キャッシング - 取得HTML の一時保存
4. マルチプロセッシング - 並列処理で高速化
5. 詳細エラーログ - 失敗理由の詳細記録

---

## モジュール化のメリット

- 各機能を単独でテスト可能
- エラー発生時の原因特定が容易
- コードの再利用性が高い
- 機能追加・変更が容易
- チーム開発に適している

完成日: 2026-04-13