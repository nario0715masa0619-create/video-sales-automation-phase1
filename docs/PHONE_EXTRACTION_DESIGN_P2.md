## 5. phone_extractor_core.py 仕様

class PhoneExtractor:
    def __init__(self, timeout=10, cache_dir="cache"):
        """
        初期化
        Args:
            timeout: HTTP タイムアウト（秒）
            cache_dir: キャッシュディレクトリ
        """
    
    def extract(self, url: str) -> Dict:
        """
        URL から情報を抽出
        Args:
            url: 対象 URL
        Returns:
            {
                "url": "https://example.com",
                "company_name": "Cybozu, Inc.",
                "phone": "03-1234-5678",
                "email": "contact@example.com",
                "status": "success",
                "methods": {
                    "company_name": "og:site_name",
                    "phone": "regex",
                    "email": "mailto_link"
                },
                "error": None,
                "timestamp": "2026-04-21T09:00:00"
            }
        Status値：
        - success: 全情報取得成功
        - partial: 一部のみ取得
        - not_found: 情報見つからず
        - timeout: アクセスタイムアウト
        - forbidden: アクセス拒否
        - error: その他エラー
        """
    
    def extract_batch(self, urls: List[str]) -> List[Dict]:
        """複数 URL をバッチ処理"""

## 6. 会社名抽出の優先度
1. <meta name="og:site_name" content="..."> （最高信頼度）
2. <title> タグテキスト
3. JSON-LD {"@type": "Organization", "name": "..."}
4. <h1> タグテキスト
5. ドメイン名から推測 (example.com → Example)
6. 取得失敗時は None

## 7. 電話番号抽出の優先度
1. <a href="tel:03-1234-5678"> （最高信頼度）
2. JSON-LD telephone プロパティ
3. <meta name="telephone" content="...">
4. 正規表現マッチング

## 8. メール抽出の優先度
1. <a href="mailto:contact@example.com"> （最高信頼度）
2. JSON-LD contactPoint.email
3. 正規表現マッチング
