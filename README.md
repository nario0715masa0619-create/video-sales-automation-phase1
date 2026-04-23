# Video Sales Automation - Phase 1

営業自動化プロジェクト Phase 1

## 主な機能
- CRM シートから企業 URL を読み込み
- ウェブサイトをクロール
- 電話番号とメールアドレスを自動抽出
- 結果を Phase 5 Google Sheet に保存

## 使用方法
python website_scraper.py
python website_scraper.py --limit=3

## Phase 5 Google Sheet スキーマ
列A: company_name (企業名)
列B: website_url (ウェブサイト URL)
列C: phone (電話番号または "None")
列D: email (メールアドレスまたは "None")
列E: source_page (抽出元ページ)
列F: status ("success" または "invalid")
列G: scraped_at (実行日時 YYYY-MM-DD HH:MM:SS)

## Email 抽出機能
tools/email_extractor.py で実装
優先順位: mailto リンク → JSON-LD → meta タグ → regex
ドメイン検証: テスト用ドメイン除外、誤字ドメイン除外
未検出時は "None" 文字列を保存

## パフォーマンス
1 URL あたり 10-30 秒
全 1,589 URL で約 4-8 時間（シングルスレッド）
