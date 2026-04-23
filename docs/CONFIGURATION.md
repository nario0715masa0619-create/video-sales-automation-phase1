# Configuration Guide

## config.py

### Google Sheets Settings

SPREADSHEET_ID_PHASE5
  説明: Phase 5 Google Sheet の ID
  形式: str
  取得方法: Sheet URL から抽出
    https://docs.google.com/spreadsheets/d/{ID}/edit
  例: "1a2b3c4d5e6f7g8h9i0j"

SHEET_NAME_PHASE5
  説明: Phase 5 Google Sheet のシート名
  形式: str
  デフォルト: "Phase5"
  注意: シート名に空白が含まれる場合は引用符で囲む

CRM_SHEET_ID
  説明: CRM Google Sheet の ID
  形式: str

CRM_SHEET_NAME
  説明: CRM Google Sheet のシート名
  形式: str
  デフォルト: "leads" or "CRM"

### Website Crawling Settings

MAX_CRAWL_PAGES
  説明: ドメインごとのクロール最大ページ数
  形式: int
  デフォルト: 20
  調整: 多いほど時間がかかる / 少ないと見落とし増加

TIMEOUT
  説明: HTTP リクエストのタイムアウト（秒）
  形式: int
  デフォルト: 10
  調整: ネットワークが遅い場合は増やす

CRAWL_DELAY
  説明: クロール間隔（秒）
  形式: float
  デフォルト: 0.5
  注意: 小さすぎると アクセス拒否のリスク

USER_AGENT
  説明: HTTP User-Agent ヘッダー
  形式: str
  デフォルト: "Mozilla/5.0 (...)"

### Extraction Settings

PHONE_PATTERNS
  説明: 電話番号を検出する正規表現リスト
  形式: list of str
  例:
    [
      r'0\d{1,4}-?\d{1,4}-?\d{4}',
      r'0\d{10,11}',
      r'\+81-?\d{1,4}-?\d{1,4}-?\d{4}'
    ]

EMAIL_PATTERN
  説明: メールアドレス検出用 regex
  形式: str
  例: r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

### Database Settings

DB_PATH
  説明: SQLite DB ファイルパス
  形式: str
  デフォルト: "logs/phase5_data.db"

CACHE_DB_PATH
  説明: HTML キャッシュ DB パス
  形式: str
  デフォルト: "logs/html_cache.db"

CACHE_EXPIRE_DAYS
  説明: キャッシュ有効期限（日数）
  形式: int
  デフォルト: None (永続)

### Logging Settings

LOG_FILE
  説明: ログファイルパス
  形式: str
  デフォルト: "logs/website_scraper.log"

LOG_LEVEL
  説明: ログレベル
  形式: str
  オプション: "DEBUG", "INFO", "WARNING", "ERROR"
  デフォルト: "INFO"

### Performance Settings

BATCH_SIZE
  説明: 1バッチでのシート追記数
  形式: int
  デフォルト: 1

PARALLEL_WORKERS
  説明: 並列ワーカー数（予約済み）
  形式: int
  デフォルト: 1 (シングルスレッド)

