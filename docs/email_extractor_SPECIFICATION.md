# email_extractor.py 関数仕様書

## 1. get_email_from_youtube_channel(base_url: str) -> tuple

**目的**
YouTubeチャンネルから企業のメールアドレスとお問い合わせフォームを自動取得する

**入力パラメータ**
- base_url (str): YouTubeチャンネルのURL
  例: https://www.youtube.com/@example_channel

**出力**
タプル形式で3つの値を返す
- website_url (str): YouTubeチャンネルから抽出した公式サイトのURL
- email (str): 公式サイトから抽出したメールアドレス。見つからなければ空文字列
- contact_form_url (str): 公式サイトから抽出したお問い合わせフォームのURL。見つからなければ空文字列

**処理フロー**
1. get_website_from_youtube(base_url) を呼び出し YouTubeチャンネルの「About」ページから公式サイトURLを取得
2. 公式サイトが見つからなければ ("", "", "") を返す
3. scrape_email_from_site(website_url) を呼び出し公式サイトからメールアドレスとお問い合わせフォームURLを抽出
4. メールアドレスの有効性チェック (is_valid_email関数) を実施
5. EXCLUDE_EMAIL_KEYWORDS で除外キーワードを含むメールをフィルタリング
6. 最終的な (website_url, email, contact_form_url) タプルを返す

**戻り値例**
成功時:
- website_url: "https://example.com"
- email: "contact@example.com"
- contact_form_url: "https://example.com/contact"

失敗時:
- website_url: ""
- email: ""
- contact_form_url: ""



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



## 3. _extract_contact_form_url(html: str, base_url: str) -> str

**目的**
HTMLから contact form のURLを抽出する内部ヘルパー関数

**入力パラメータ**
- html (str): HTTPレスポンスで取得したHTMLの本体テキスト
- base_url (str): 相対URLを絶対URLに変換するための基準URL
  例: https://example.com

**出力**
- contact_form_url (str): 見つかったお問い合わせフォームのURL。見つからなければ空文字列

**処理フロー**
1. BeautifulSoup(html, 'html.parser') でHTMLをパース
2. すべての <form> タグを探す
3. form タグに action 属性がある場合、そのURLを返す
4. form タグが見つからない場合、<a> リンクを探す
5. リンクテキストまたは href に contact/inquiry/support などのキーワードがあるものを検索
6. 相対URLの場合 urljoin(base_url, href) で絶対URLに変換
7. 見つかったURLを返す。見つからなければ空文字列を返す

**キーワード検索対象**
- URLに含まれるキーワード: 'contact', 'inquiry', 'support', 'help', 'toiawase', 'form', 'request'
- リンクテキストに含まれるキーワード: 'お問い合わせ', 'お問合せ', '資料請求', 'contact', 'inquiry', 'form'

**戻り値例**
見つかった場合:
- "https://example.com/contact"
- "https://example.com/inquiry-form"
- "https://example.com/support"

見つからない場合:
- ""

**呼び出し元**
get_email_from_youtube_channel() 内で contact_form_url が見つからない場合に呼び出される

**注意事項**
- この関数は scrape_email_from_site() 内部で既に contact form 検出が行われているため、その補助的な役割を果たす
- HTMLは呼び出し元から受け取り、この関数内では新たにHTTPリクエストを発行しない


