"""
config.py
=========
全モジュール共通の設定値を一元管理するファイル。
.env ファイルの値を読み込み、型付きの設定オブジェクトとして提供する。
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env ファイルを読み込む（プロジェクトルートから探索）
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


# ==================================================
# Google API 認証設定
# ==================================================
GOOGLE_SERVICE_ACCOUNT_JSON: str = os.getenv(
    "GOOGLE_SERVICE_ACCOUNT_JSON", "credentials/service_account.json"
)
GMAIL_SENDER_ADDRESS: str = os.getenv("GMAIL_SENDER_ADDRESS", "")
GMAIL_OAUTH_TOKEN_FILE: str = os.getenv(
    "GMAIL_OAUTH_TOKEN_FILE", "credentials/gmail_token.json"
)

# ==================================================
# Google Sheets（ミニ CRM）設定
# ==================================================
SPREADSHEET_ID: str = os.getenv("SPREADSHEET_ID", "")
SHEET_LEADS: str = os.getenv("SHEET_LEADS", "Leads")
SHEET_EMAIL_LOG: str = os.getenv("SHEET_EMAIL_LOG", "メール送信ログ")
SHEET_MASTER: str = os.getenv("SHEET_MASTER", "マスタ設定")

# ==================================================
# Gemini API 設定
# ==================================================
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3-pro-preview")

# ==================================================
# SerpAPI 設定
# ==================================================
# SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "")  # 廃止
SERPAPI_KEYS: list[str] = [
    os.getenv("SERPAPI_KEY_1", ""),
    os.getenv("SERPAPI_KEY_2", ""),
    os.getenv("SERPAPI_KEY", ""),
]
SERPAPI_KEY_INDEX: int = 1  # 現在使用中のキーインデックス

# ==================================================
# 自社情報（メール署名）
# ==================================================
MY_COMPANY_NAME: str = os.getenv("MYCOMPANYNAME", "株式会社ルヴィラ")
MY_NAME: str = os.getenv("MYNAME", "成相")
MY_TITLE: str = os.getenv("MYTITLE", "マーケティング担当")
MY_PHONE: str = os.getenv("MYPHONE", "070-5595-9523")
MY_WEBSITE: str = os.getenv("MYWEBSITE", "https://luvira.co.jp")

# メール署名テンプレート（全メールで共通使用）
EMAIL_SIGNATURE: str = f"""
--
{MY_NAME}（{MY_TITLE}）
{MY_COMPANY_NAME}
TEL: {MY_PHONE}
URL: {MY_WEBSITE}
"""

# ==================================================
# 営業メール設定
# ==================================================
EMAIL_MAX_SEQUENCE = int(os.getenv("EMAIL_MAX_SEQUENCE", "4"))
EMAIL_INTERVAL_DAYS = int(os.getenv("EMAIL_INTERVAL_DAYS", "4"))
EMAIL_MAX_SEND_PER_RUN = int(os.getenv("EMAIL_MAX_SEND_PER_RUN", "20"))
EMAIL_TARGET_RANKS = [
    r.strip() for r in os.getenv("EMAIL_TARGET_RANKS", "A,B").split(",")
]

# ==================================================
# メール送信の配分比率（1回目優先）
# ==================================================
EMAIL_FIRST_SEND_RATIO = 0.70    # 1回目送信：70%
EMAIL_FOLLOWUP_SEND_RATIO = 0.30  # 2回目以降：30%

# ==================================================
# ICP（理想顧客プロファイル）条件
# ==================================================
ICP_MIN_SUBSCRIBERS: int = 500         # 最小登録者数
ICP_MAX_SUBSCRIBERS: int = 50_000      # 最大登録者数
ICP_MIN_VIDEOS_3M: int = 4             # 直近3ヶ月の最低投稿本数
ICP_COUNTRY: str = "JP"                # 対象国コード

# ==================================================
# スコアリング設定
# ==================================================
# 各指標の最大点数
SCORE_WEIGHTS = {
    "posting_frequency": 30,    # 投稿頻度
    "view_count": 25,           # 再生数
    "engagement": 25,           # エンゲージメント率
    "trend": 20,                # 成長トレンド
}

# 投稿頻度スコアのしきい値（直近3ヶ月の投稿本数）
POSTING_FREQ_THRESHOLDS = [
    (12, 30),   # 12本以上 → 満点
    (8, 20),    # 8本以上  → 20点
    (4, 10),    # 4本以上  → 10点
]

# 再生数スコアのしきい値（登録者比の再生率）
VIEW_RATE_THRESHOLDS = [
    (0.10, 25),  # 10%以上 → 満点
    (0.05, 15),  # 5%以上  → 15点
    (0.02, 8),   # 2%以上  → 8点
]

# エンゲージメント率のしきい値
ENGAGEMENT_THRESHOLDS = [
    (0.05, 25),  # 5%以上 → 満点
    (0.03, 15),  # 3%以上 → 15点
    (0.01, 8),   # 1%以上 → 8点
]

# 成長トレンドのしきい値（直近1ヶ月 / 過去平均）
TREND_THRESHOLDS = [
    (1.20, 20),  # 120%以上 → 満点
    (1.00, 12),  # 100%以上 → 12点
    (0.80, 6),   # 80%以上  → 6点
]

# ランク分け基準
RANK_A_MIN: float = 70.0
RANK_B_MIN: float = 40.0
# 39点以下 → C ランク

# ==================================================
# Flask REST API 設定
# ==================================================
FLASK_PORT: int = int(os.getenv("FLASK_PORT", "8080"))
API_SECRET_TOKEN: str = os.getenv("API_SECRET_TOKEN", "change_me")

# ==================================================
# ロギング設定
# ==================================================
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")

# ==================================================
# スクレイピング設定
# ==================================================
SCRAPE_DELAY_SECONDS: float = float(os.getenv("SCRAPE_DELAY_SECONDS", "3"))
SCRAPE_MAX_CHANNELS: int = int(os.getenv("SCRAPE_MAX_CHANNELS", "50"))

# YouTube チャンネル検索キーワード（ICP候補を発掘するためのデフォルトキーワード）
DEFAULT_SEARCH_KEYWORDS: list[str] = [
    "YouTube活用",
    "動画マーケティング",
    "オンライン営業",
    "SNS活用",
    "動画集客",
    "ウェビナー",
    "YouTube広告",
    "インフルエンサー",
    "チャンネル運用",
    "コンテンツマーケティング",
    "ビジネスYouTube",
    "企業動画",
]

# ==================================================
# 設定値の検証（起動時に必須項目をチェック）
# ==================================================
def validate_config(strict: bool = False) -> list[str]:
    """
    必須設定値が未設定の場合に警告リストを返す。
    strict=True の場合は ValueError を送出する。

    Returns:
        list[str]: 未設定の環境変数名リスト
    """
    required_vars = {
        "SPREADSHEET_ID": SPREADSHEET_ID,
        "GEMINI_API_KEY": GEMINI_API_KEY,
    }
    missing = [k for k, v in required_vars.items() if not v]

    if missing and strict:
        raise ValueError(
            f"必須環境変数が未設定です: {', '.join(missing)}\n"
            ".env.example を参考に .env ファイルを設定してください。"
        )
    return missing


if __name__ == "__main__":
    # 設定確認用：python config.py で実行
    missing = validate_config()
    if missing:
        print(f"⚠️  未設定の環境変数: {missing}")
    else:
        print("✅ 全設定値が正常にロードされました")
    print(f"   SPREADSHEET_ID: {SPREADSHEET_ID[:8]}..." if SPREADSHEET_ID else "   SPREADSHEET_ID: 未設定")
    print(f"   GEMINI_MODEL: {GEMINI_MODEL}")
    print(f"   EMAIL_MAX_SEQUENCE: {EMAIL_MAX_SEQUENCE}通")
    print(f"   EMAIL_TARGET_RANKS: {EMAIL_TARGET_RANKS}")

# ==================================================
# メール送信の配分比率（1回目優先）
# ==================================================
EMAIL_FIRST_SEND_RATIO = 0.70    # 1回目送信：70%
EMAIL_FOLLOWUP_SEND_RATIO = 0.30  # 2回目以降：30%






# YouTube Data API v3
YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY が .env に設定されていません")

# ===== ウォームアップ・バウンス管理設定 =====
from datetime import datetime
import os

# ドメイン運用開始日
DOMAIN_LAUNCH_DATE = "2026-04-07"

# 週ごとのウォームアップスケジュール
WARMUP_SCHEDULE = {
    1: 10,   # 1週目：10件/日
    2: 15,   # 2週目：15件/日
    3: 20,   # 3週目：20件/日
    4: 25,   # 4週目：25件/日
}

# 4週目以降のオプション設定
ENABLE_AGGRESSIVE_MODE = False  # True なら最大 30 件/日を許可
AGGRESSIVE_BOUNCE_THRESHOLD = 1.0  # バウンス率が 1% 未満なら aggressive mode に進める条件

# SMTP送信元設定（luvira-biz.jp）
SMTP_HOST = "mail.luvira-biz.jp"
SMTP_PORT = 587
SMTP_USER = "marketing@luvira-biz.jp"
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
MAIL_FROM = "marketing@luvira-biz.jp"

# ===== IMAP 設定（バウンス監視用）=====
IMAP_HOST = os.getenv("IMAP_HOST", "mail.luvira-biz.jp")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
IMAP_USER = os.getenv("IMAP_USER", "marketing@luvira-biz.jp")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")
if not IMAP_PASSWORD:
    raise ValueError("IMAP_PASSWORD が .env に設定されていません")

# === 大規模実行用ジャンル別キーワード定義 ===

CONSTRUCTION_KEYWORDS: list[str] = [
    "建設企業", "工務店", "ハウスメーカー", "建築会社"
]

RETAIL_KEYWORDS: list[str] = [
    "小売企業", "店舗運営", "商業施設", "チェーン店"
]

FOOD_BEVERAGE_KEYWORDS: list[str] = [
    "飲食店", "飲食企業", "レストラン", "カフェ運営"
]

SERVICE_KEYWORDS: list[str] = [
    "サービス企業", "コンサルティング", "人材派遣", "清掃サービス"
]

FINANCE_KEYWORDS: list[str] = [
    "金融企業", "銀行", "保険会社", "投資会社"
]

REAL_ESTATE_KEYWORDS: list[str] = [
    "不動産企業", "不動産開発", "賃貸管理", "物件仲介"
]

APPAREL_KEYWORDS: list[str] = [
    "アパレル企業", "ファッションブランド", "衣料品メーカー", "靴メーカー"
]

LOGISTICS_KEYWORDS: list[str] = [
    "物流企業", "配送サービス", "運送会社", "倉庫管理"
]

# ===== ウォームアップ・バウンス管理設定 =====
DOMAIN_LAUNCH_DATE = "2026-04-07"
WARMUP_SCHEDULE = {1: 10, 2: 15, 3: 20, 4: 25}
ENABLE_AGGRESSIVE_MODE = False
AGGRESSIVE_BOUNCE_THRESHOLD = 1.0
IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")

SPREADSHEET_ID_PHASE5: str = os.getenv("SPREADSHEET_ID_PHASE5", "")

SHEET_NAME_CRM: str = os.getenv("SHEET_NAME_CRM", "Leads")
SHEET_NAME_PHASE5: str = os.getenv("SHEET_NAME_PHASE5", "leads")
CREDENTIALS_FILE: str = os.getenv("CREDENTIALS_FILE", "credentials/service_account.json")


# ==================================================
# 電話番号抽出用の正規表現パターン（幅広く抽出後、is_valid_phone で厳密検証）
# ==================================================
PHONE_PATTERNS = [
    r'0\d{1,4}[-\s]?\d{1,4}[-\s]?\d{4}',     # 固定電話（各種形式）
    r'(070|080|090)[-\s]?\d{4}[-\s]?\d{4}',  # 携帯（各種形式）
    r'0120[-\s]?\d{2,4}[-\s]?\d{4}',         # フリーダイヤル
    r'0570[-\s]?\d{2,4}[-\s]?\d{4}',         # ナビダイヤル
    r'\+81[-\s]?\d{1,4}[-\s]?\d{1,4}[-\s]?\d{4}',  # 国際電話
    r'0\d{2,4}\d{2,4}\d{4}',                 # ハイフンなし固定電話
    r'(070|080|090)\d{8}',                   # ハイフンなし携帯
]

# ==================================================
# HTML フェッチング設定
# ==================================================
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

REQUEST_TIMEOUT = 10  # Requests タイムアウト（秒）
CRAWL_TIMEOUT = 30    # Playwright タイムアウト（秒）
# ==================================================
# スキップ対象 URL パターン（短縮 URL、PDF、画像など）
# ==================================================
SKIP_URL_PATTERNS = [
    r'bit\.ly',
    r'goo\.gl',
    r'tinyurl',
    r'short\.link',
    r'ow\.ly',
    r'\.pdf$',
    r'\.jpg$', r'\.jpeg$', r'\.png$', r'\.gif$', r'\.webp$',
    r'\.mp4$', r'\.mov$', r'\.avi$',
    r'youtube\.com/watch',
    r'youtube\.com/playlist',
    r'twitter\.com',
    r'facebook\.com',
    r'instagram\.com',
    r'linkedin\.com',
]



# ==================================================
# ZeroBounce API 設定（Phase 6）
# ==================================================
ZEROBOUNCE_API_KEY: str = os.getenv("ZEROBOUNCE_API_KEY", "")
ZEROBOUNCE_API_URL: str = "https://api.zerobounce.net/v2/validate"
