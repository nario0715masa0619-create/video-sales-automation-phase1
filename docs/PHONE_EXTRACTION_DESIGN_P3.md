## 9. phone_extractor_crm.py 仕様

def get_urls_from_crm(limit=None, filters=None) -> List[Dict]:
    """
    CRM から URL を取得
    Args:
        limit: 取得件数（デフォルト: すべて）
        filters: フィルタ条件 (e.g., {"業界": "IT"})
    Returns:
        [
            {
                "source_id": "ch_001",
                "channel_name": "kintone活用ちゃんねる",
                "url": "https://kintone.cybozu.com",
                "source": "crm",
                "existing_email": "contact@kintone.com",
                "existing_phone": None
            },
            ...
        ]
    注: existing_email, existing_phone は CRM 既存データ。
    スクレイピング結果で上書きされる。
    """

## 10. phone_extractor_google.py 仕様

def get_urls_from_google(query, num_results=10) -> List[Dict]:
    """
    Google 検索結果から URL を取得
    Args:
        query: 検索キーワード (e.g., "AI スタートアップ")
        num_results: 取得件数
    Returns:
        [
            {
                "source_id": "google_001",
                "query": "AI スタートアップ",
                "url": "https://example-ai.com",
                "source": "google",
                "rank": 1,
                "title": "Example AI - AI ソリューション"
            },
            ...
        ]
    注: company_name は未設定。スクレイピングで取得。
    """

## 11. phone_extractor_file.py 仕様

def get_urls_from_file(file_path) -> List[Dict]:
    """
    CSV/JSON ファイルから URL を読み込み
    Args:
        file_path: ファイルパス
    Returns:
        [
            {
                "source_id": "file_001",
                "url": "https://example.com",
                "source": "file",
                "company_name": None,
                "metadata": {...}
            },
            ...
        ]
    対応フォーマット:
    CSV:
    url,company_name,industry
    https://example.com,Example Inc,IT
    
    JSON:
    [{"url": "https://example.com", "company_name": "Example Inc"}]
    """

## 12. phone_sheet_saver.py 仕様

class PhoneSheetSaver:
    def __init__(self, sheet_name="電話番号DB"):
        """Google Sheets に接続"""
    
    def save(self, results: List[Dict]) -> Dict:
        """
        結果を Google Sheets に保存
        Args:
            results: extract() の結果リスト
        Returns:
            {
                "saved_count": 5,
                "updated_count": 2,
                "failed_count": 0,
                "sheet_url": "https://docs.google.com/..."
            }
        """
    
    def update_existing(self, url: str, data: Dict) -> bool:
        """既存レコード（同じ URL）を更新"""
