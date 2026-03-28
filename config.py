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
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ==================================================
# SerpAPI 設定
# ==================================================
SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "")

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
EMAIL_MAX_SEQUENCE: int = int(os.getenv("EMAIL_MAX_SEQUENCE", "4"))
EMAIL_INTERVAL_DAYS: int = int(os.getenv("EMAIL_INTERVAL_DAYS", "4"))
EMAIL_MAX_SEND_PER_RUN: int = int(os.getenv("EMAIL_MAX_SEND_PER_RUN", "20"))
EMAIL_TARGET_RANKS: list[str] = [
    r.strip() for r in os.getenv("EMAIL_TARGET_RANKS", "A,B").split(",")
]

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
    "YouTube 企業チャンネル 商品紹介",
    "YouTube 会社 ビジネス チャンネル",
    "YouTube D2C ブランド 動画",
    "YouTube オンライン講座 スクール",
    "YouTube BtoB サービス 紹介",
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
        "GMAIL_SENDER_ADDRESS": GMAIL_SENDER_ADDRESS,
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

