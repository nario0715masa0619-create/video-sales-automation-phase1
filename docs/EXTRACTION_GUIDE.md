# Email & Phone Extraction Guide

## Phone Extraction (tools/phone_extractor.py)

### 対応フォーマット
- 国際形式: +81-90-1234-5678
- 携帯: 070/080/090 + 8桁
- 固定電話: 03/06/011 + 6-7桁
- フリーダイアル: 0120 + 6-7桁
- ナビダイアル: 0570 + 4-6桁

### 検証ロジック
- スペース・ハイフン・括弧を正規化
- 00 プレフィックス除外
- 02 市外局番除外
- 桁数チェック
- 連続同一数字除外

### 抽出優先順位
1. <a href="tel:"> リンク
2. JSON-LD telephone フィールド
3. meta タグ (name/property に phone 含む)
4. 正規表現パターンマッチ

## Email Extraction (tools/email_extractor.py)

### 対応フォーマット
- 標準: user@example.com
- ドット: user.name@example.co.jp
- プラス記号: user+tag@example.com
- 数字: user123@example.com

### ドメイン検証
除外ドメイン:
- example.com, test.com, sample.com
- localhost, invalid.com
- example.org, example.net

除外誤字:
- gmial.com → gmail.com
- gmai.com → gmail.com
- yahooo.com → yahoo.com
- hotmial.com → hotmail.com

### 抽出優先順位
1. <a href="mailto:"> リンク
2. JSON-LD email フィールド
3. meta タグ (og:email など)
4. 正規表現パターンマッチ

### 未検出時の処理
email = "None" (空文字列ではなく文字列として保存)

## 並行抽出ロジック

website_scraper.py の scrape_website() 内:
- 1つのループで電話とメールを同時抽出
- 電話見つかったら次ページへ
- メール見つかったら次ページへ
- 両方見つかったらループを抜ける
- 不要な重複ループを回避

## 正規表現パターン

Phone patterns (config.py):
- r'0\d{1,4}-?\d{1,4}-?\d{4}'
- r'0\d{10,11}'
- r'\+81-?\d{1,4}-?\d{1,4}-?\d{4}'

Email pattern:
- r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

