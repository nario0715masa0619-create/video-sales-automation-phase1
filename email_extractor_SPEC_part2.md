## 2. scrape_email_from_site(website_url: str) -> tuple

**目的**
企業の公式サイトからメールアドレスとお問い合わせフォームURLを自動抽出する

**入力パラメータ**
- website_url (str): 企業の公式サイトのURL
  例: https://example.com

**出力**
タプル形式で3つの値を返す
- website_url (str): 入力されたサイトURL（そのまま返す）
- email (str): 抽出されたメールアドレス。見つからなければ空文字列
- contact_form_url (str): 抽出されたお問い合わせフォームのURL。見つからなければ空文字列

**内部処理**
この関数内部では html 変数を使用してHTMLをパースしますが、html は外部には返しません。

**メール抽出の優先度（順序重要）**
1. JSON-LDスキーマ（<script type="application/ld+json">）から email フィールドを検索
2. HTMLの mailto: リンク（<a href="mailto:...">）から抽出
3. ページのテキストから正規表現でメールアドレスパターンを検索
4. いずれも見つからなければ空文字列を返す

**お問い合わせフォームURL抽出の優先度**
1. HTMLの <form> タグの action 属性から取得
2. contact/inquiry/support などのキーワードを含むリンクを検索
3. 相対URLの場合は urljoin で絶対URLに変換
4. 見つからなければ空文字列を返す

**キャッシング機能**
- 初回アクセス時はキャッシュから確認
- キャッシュヒット時は load_from_cache() から (website_url, email, contact_form_url) を返す
- キャッシュミス時は HTTPリクエストでスクレイピング実施
- スクレイピング後は save_to_cache() で結果をキャッシュに保存

**リトライ機能**
- ネットワークタイムアウト時は MAX_RETRIES 回まで自動リトライ
- リトライ間隔は RETRY_DELAY 秒

**戻り値例**
成功時:
- website_url: "https://example.com"
- email: "info@example.com"
- contact_form_url: "https://example.com/inquiry"

見つからない場合:
- website_url: "https://example.com"
- email: ""
- contact_form_url: ""

