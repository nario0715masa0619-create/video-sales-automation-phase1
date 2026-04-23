# API Reference

## phone_extractor.py

### is_valid_phone(phone_str)

入力: phone_str (str) - 電話番号文字列
処理:
  - スペース・ハイフン・括弧を削除
  - 00 プレフィックス除外
  - 02 市外局番除外
  - 桁数チェック (10-11桁)
  - 連続同一数字除外
  - パターンマッチ
出力: bool (True = 有効, False = 無効)

### extract_phone_from_tel_link(soup)

入力: soup (BeautifulSoup) - HTML オブジェクト
処理:
  - <a href="tel:..."> リンク検索
  - 電話番号を抽出・検証
出力: str or None

### extract_phone_from_jsonld(soup)

入力: soup (BeautifulSoup)
処理:
  - JSON-LD スクリプトを検索
  - telephone フィールドを取得
  - 検証
出力: str or None

### extract_phone_from_meta(soup)

入力: soup (BeautifulSoup)
処理:
  - meta タグを検索（name/property に phone 含む）
  - content 属性を取得
  - 検証
出力: str or None

### extract_phone_from_regex(html_text)

入力: html_text (str) - HTML テキスト
処理:
  - config.PHONE_PATTERNS を適用
  - 最初にマッチしたものを検証
出力: str or None

### extract_phone(html_text)

入力: html_text (str) - HTML テキスト
処理:
  - 優先順位: tel → JSON-LD → meta → regex
  - 各メソッドを順に実行
  - 見つかったら即座に返す
出力: str or None

## email_extractor.py

### is_valid_email(email_str)

入力: email_str (str) - メールアドレス文字列
処理:
  - 基本フォーマット検証 (regex)
  - テスト用ドメイン除外
  - 誤字ドメイン除外
出力: bool (True = 有効, False = 無効)

### extract_email_from_mailto_link(soup)

入力: soup (BeautifulSoup)
処理:
  - <a href="mailto:..."> リンク検索
  - メールアドレスを抽出・検証
出力: str or None

### extract_email_from_jsonld(soup)

入力: soup (BeautifulSoup)
処理:
  - JSON-LD スクリプトを検索
  - email フィールド取得
  - contactPoint.email も検索
  - 検証
出力: str or None

### extract_email_from_meta(soup)

入力: soup (BeautifulSoup)
処理:
  - meta タグを検索（property/name に email 含む）
  - content 属性を取得
  - 検証
出力: str or None

### extract_email_from_regex(html_text)

入力: html_text (str) - HTML テキスト
処理:
  - regex パターンを適用
  - 最初にマッチしたものを検証
出力: str or None

### extract_email(html_text)

入力: html_text (str) - HTML テキスト
処理:
  - 優先順位: mailto → JSON-LD → meta → regex
  - 各メソッドを順に実行
  - 見つかったら即座に返す
出力: str or None

