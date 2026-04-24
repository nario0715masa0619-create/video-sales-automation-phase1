# 電話番号・メール・会社名抽出パイプライン設計書

## 1. 概要
CRM、Google 検索、ファイルなど複数のソースから URL を取得し、
汎用的にスクレイピングして以下の情報を抽出する：
- 会社名
- 電話番号
- メールアドレス
結果を Google Sheets に保存する。

## 2. アーキテクチャ図
【URL ソース層】
├─ CRM から URL + 既存データ取得
├─ Google 検索から URL 取得
└─ CSV/JSON ファイルから URL 読み込み
        ↓ URL リスト
【汎用スクレイピング層】
├─ HTML ダウンロード
├─ 会社名抽出
├─ 電話番号抽出
├─ メールアドレス抽出
└─ キャッシング・リトライ
        ↓ 結果
【保存層】
├─ Google Sheets 保存
└─ ローカル DB 保存

## 3. モジュール構成
ルート
├── phone_extractor_core.py
├── phone_extractor_crm.py
├── phone_extractor_google.py
├── phone_extractor_file.py
└── phone_sheet_saver.py

## 4. Google Sheets スキーマ
company_name | website_url | phone | email | source_page | status
Cybozu Inc.  | https://... | 03... | c... | crm | success
Example AI   | https://... | 050..| i... | google | partial

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

## 13. 使用例

### パターン A: CRM から取得して Sheets に保存
from phone_extractor_crm import get_urls_from_crm
from phone_extractor_core import PhoneExtractor
from phone_sheet_saver import PhoneSheetSaver

urls = get_urls_from_crm(limit=50)
extractor = PhoneExtractor()
results = extractor.extract_batch([u["url"] for u in urls])
saver = PhoneSheetSaver()
saver.save(results)

### パターン B: Google 検索から取得して Sheets に保存
from phone_extractor_google import get_urls_from_google
from phone_extractor_core import PhoneExtractor
from phone_sheet_saver import PhoneSheetSaver

urls = get_urls_from_google("AI スタートアップ", num_results=20)
extractor = PhoneExtractor()
results = extractor.extract_batch([u["url"] for u in urls])
saver = PhoneSheetSaver()
saver.save(results)

### パターン C: CSV ファイルから読み込んで Sheets に保存
from phone_extractor_file import get_urls_from_file
from phone_extractor_core import PhoneExtractor
from phone_sheet_saver import PhoneSheetSaver

urls = get_urls_from_file("companies.csv")
extractor = PhoneExtractor()
results = extractor.extract_batch([u["url"] for u in urls])
saver = PhoneSheetSaver()
saver.save(results)

## 14. エラーハンドリング

| Status | 原因 | 対応 |
|--------|------|------|
| success | 全情報抽出成功 | 保存 |
| partial | 一部のみ抽出 | 保存（空欄あり） |
| not_found | 情報なし | 保存（なしと記録） |
| timeout | タイムアウト | リトライ 3 回 |
| forbidden | アクセス拒否 | スキップ、ログ |
| error | その他エラー | スキップ、詳細ログ |

## 15. キャッシング機能
- HTML キャッシュ: 24 時間有効
- キャッシュディレクトリ: cache/
- キャッシュキー: URL の SHA256 ハッシュ

## 16. リトライ機能
- タイムアウト: 3 回まで自動リトライ
- 待機時間: 2 秒（指数バックオフ）
- Forbidden: リトライなし

## 17. 実装優先度

### Phase 1（必須）
- phone_extractor_core.py（会社名・電話・メール抽出）
- phone_extractor_crm.py（CRM 連携）
- phone_sheet_saver.py（Sheets 保存）

### Phase 2（推奨）
- phone_extractor_google.py（Google 検索）
- phone_extractor_file.py（ファイル入出力）

### Phase 3（オプション）
- キャッシング強化
- バッチ処理最適化
- ローカル DB バックアップ機能
- 非同期処理対応

## 18. ファイル構成

ルート/
├── phone_extractor_core.py
├── phone_extractor_crm.py
├── phone_extractor_google.py
├── phone_extractor_file.py
├── phone_sheet_saver.py
├── cache/（キャッシュディレクトリ）
└── logs/（ログディレクトリ）

