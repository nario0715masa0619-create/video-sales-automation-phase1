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

