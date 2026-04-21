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

