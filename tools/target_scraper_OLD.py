"""
target_scraper.py
=================
YouTubeチャンネルのデータ取得とICP条件フィルタリングを行うモジュール。

【APIなし版の実装方針】
- yt-dlp を使ってチャンネルメタデータと動画リストを取得
- SerpAPI（Google検索API）を使って企業チャンネル候補を検索
- BeautifulSoup による補完スクレイピング

【将来のAPI有効化拡張】
- YouTube Data API v3 に切り替える場合は `_get_channel_stats_api()` を使用
- YOUTUBE_API_KEY を .env に追加するだけで切り替え可能
"""

import time
import re
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional
import requests
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

import config

# JST タイムゾーン
JST = timezone(timedelta(hours=9))


# ==================================================
# データクラス定義
# ==================================================

@dataclass
class VideoData:
    """個別動画のデータモデル"""
    video_id: str
    title: str
    published_at: datetime
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    duration_seconds: int = 0

    @property
    def engagement_rate(self) -> float:
        """エンゲージメント率 = (いいね + コメント) / 再生数"""
        if self.view_count == 0:
            return 0.0
        return (self.like_count + self.comment_count) / self.view_count


@dataclass
class ChannelData:
    """YouTubeチャンネルの集約データモデル"""
    # 基本情報
    channel_url: str
    channel_id: str = ""
    channel_name: str = ""
    description: str = ""
    country: str = ""

    # 統計情報
    subscriber_count: int = 0
    total_video_count: int = 0

    # 直近3ヶ月の動画データ
    recent_videos: list[VideoData] = field(default_factory=list)
    videos_3m_count: int = 0          # 直近3ヶ月の投稿本数
    avg_view_count: float = 0.0       # 直近3ヶ月の平均再生数
    avg_engagement_rate: float = 0.0  # 直近3ヶ月の平均エンゲージメント率

    # トレンド（直近1ヶ月 vs 過去平均）
    trend_ratio: float = 1.0          # 1.0 = 変化なし、1.2 = 20%増加

    # 最新動画情報（メールパーソナライズ用）
    latest_video_title: str = ""
    latest_video_url: str = ""
    latest_video_published_at: Optional[datetime] = None

    # スクレイピング状態
    scraped_at: Optional[datetime] = None
    error_message: str = ""

    @property
    def is_valid(self) -> bool:
        """データが有効かどうか"""
        return bool(self.channel_name) and self.subscriber_count > 0


# ==================================================
# SerpAPI を使ったチャンネル候補検索
# ==================================================

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def _search_via_serpapi(query: str) -> list[str]:
    """
    SerpAPI（Google検索）を使ってYouTubeチャンネルURLを検索する。

    Args:
        query: 検索クエリ文字列

    Returns:
        list[str]: 発見したYouTubeチャンネルURLのリスト
    """
    if not config.SERPAPI_KEY:
        logger.warning("SERPAPI_KEY が未設定です。SerpAPI検索をスキップします。")
        return []

    params = {
        "engine": "google",
        "q": f'site:youtube.com/c OR site:youtube.com/@  {query}',
        "api_key": config.SERPAPI_KEY,
        "num": 10,
        "hl": "ja",
        "gl": "jp",
    }

    try:
        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        channel_urls = []
        organic_results = data.get("organic_results", [])

        for result in organic_results:
            link = result.get("link", "")
            # YouTube チャンネルURLのパターンにマッチするものを抽出
            if re.search(r'youtube\.com/(@[\w\-]+|c/[\w\-]+|channel/UC[\w\-]+)', link):
                # /videos や /about などのサブパスを除去してチャンネルURLに正規化
                channel_url = re.sub(r'/(videos|about|playlists|community).*$', '', link)
                if channel_url not in channel_urls:
                    channel_urls.append(channel_url)

        logger.info(f"SerpAPI検索 '{query}': {len(channel_urls)}件のチャンネルを発見")
        return channel_urls

    except requests.RequestException as e:
        logger.error(f"SerpAPI リクエストエラー: {e}")
        raise


def search_company_channels(keywords: list[str] | None = None) -> list[str]:
    """
    キーワードリストを使って企業YouTubeチャンネル候補を検索する。

    Args:
        keywords: 検索キーワードリスト（Noneの場合はデフォルトを使用）

    Returns:
        list[str]: 重複除去済みのチャンネルURLリスト
    """
    if keywords is None:
        keywords = config.DEFAULT_SEARCH_KEYWORDS

    all_channel_urls: list[str] = []

    for keyword in keywords:
        logger.info(f"キーワード '{keyword}' でチャンネルを検索中...")
        urls = _search_via_serpapi(keyword)
        all_channel_urls.extend(urls)
        time.sleep(config.SCRAPE_DELAY_SECONDS)

        # 上限チェック
        if len(all_channel_urls) >= config.SCRAPE_MAX_CHANNELS:
            break

    # 重複除去
    unique_urls = list(dict.fromkeys(all_channel_urls))
    logger.info(f"検索完了: 計{len(unique_urls)}件のユニークなチャンネルURL")
    return unique_urls[:config.SCRAPE_MAX_CHANNELS]


# ==================================================
# yt-dlp を使ったチャンネルデータ取得
# ==================================================

def _parse_ytdlp_date(date_str: str) -> Optional[datetime]:
    """yt-dlp の日付文字列 (YYYYMMDD) を datetime に変換"""
    if not date_str or len(date_str) < 8:
        return None
    try:
        return datetime.strptime(date_str[:8], "%Y%m%d").replace(tzinfo=JST)
    except ValueError:
        return None


@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=3, max=15))
def get_channel_stats(channel_url: str) -> ChannelData:
    """
    yt-dlp を使ってYouTubeチャンネルの統計情報と動画リストを取得する。
    （YouTube Data API 不要バージョン）

    Args:
        channel_url: YouTubeチャンネルのURL

    Returns:
        ChannelData: 取得したチャンネルデータ
    """
    # yt-dlp のインポート（実行時にチェック）
    try:
        import yt_dlp
    except ImportError:
        raise ImportError("yt-dlp がインストールされていません。`pip install yt-dlp` を実行してください。")

    channel = ChannelData(channel_url=channel_url)

    # 直近3ヶ月の基準日
    three_months_ago = datetime.now(JST) - timedelta(days=90)
    one_month_ago = datetime.now(JST) - timedelta(days=30)

    # yt-dlp オプション設定
    ydl_opts = {
        "quiet": True,
        "extract_flat": "in_playlist",  # 動画リストのみ取得（高速化）
        "playlistend": 50,              # 最新50本まで取得
        "ignoreerrors": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # チャンネルの動画一覧ページを取得
            videos_url = channel_url.rstrip("/") + "/videos"
            info = ydl.extract_info(videos_url, download=False)

            if not info:
                channel.error_message = "チャンネル情報を取得できませんでした"
                return channel

            # チャンネル基本情報
            channel.channel_name = info.get("channel", info.get("uploader", ""))
            channel.channel_id = info.get("channel_id", info.get("uploader_id", ""))
            channel.description = (info.get("description", "") or "")[:500]
            channel.subscriber_count = info.get("channel_follower_count", 0) or 0
            channel.total_video_count = len(info.get("entries", []))

            # 個別動画データの処理
            entries = info.get("entries", []) or []
            recent_videos = []
            all_3m_views = []
            recent_1m_views = []

            for entry in entries:
                if not entry:
                    continue

                upload_date = _parse_ytdlp_date(entry.get("upload_date", ""))
                if not upload_date:
                    continue

                # 動画の詳細取得（再生数・いいね数）
                view_count = entry.get("view_count", 0) or 0
                like_count = entry.get("like_count", 0) or 0
                comment_count = entry.get("comment_count", 0) or 0

                video = VideoData(
                    video_id=entry.get("id", ""),
                    title=entry.get("title", ""),
                    published_at=upload_date,
                    view_count=view_count,
                    like_count=like_count,
                    comment_count=comment_count,
                    duration_seconds=entry.get("duration", 0) or 0,
                )
                recent_videos.append(video)

                # 直近3ヶ月の集計
                if upload_date >= three_months_ago:
                    all_3m_views.append(view_count)

                # 直近1ヶ月の集計（トレンド計算用）
                if upload_date >= one_month_ago:
                    recent_1m_views.append(view_count)

            channel.recent_videos = recent_videos
            channel.videos_3m_count = len(all_3m_views)

            if all_3m_views:
                channel.avg_view_count = sum(all_3m_views) / len(all_3m_views)

            # 平均エンゲージメント率の計算（直近3ヶ月）
            recent_3m_videos = [
                v for v in recent_videos
                if v.published_at >= three_months_ago
            ]
            if recent_3m_videos:
                channel.avg_engagement_rate = sum(
                    v.engagement_rate for v in recent_3m_videos
                ) / len(recent_3m_videos)

            # トレンド比率の計算（直近1ヶ月の平均 / 直近3ヶ月の平均）
            if all_3m_views and recent_1m_views:
                avg_3m = sum(all_3m_views) / len(all_3m_views)
                avg_1m = sum(recent_1m_views) / len(recent_1m_views)
                channel.trend_ratio = avg_1m / avg_3m if avg_3m > 0 else 1.0

            # 最新動画情報（メール文生成用）
            if recent_videos:
                latest = recent_videos[0]
                channel.latest_video_title = latest.title
                channel.latest_video_url = f"https://www.youtube.com/watch?v={latest.video_id}"
                channel.latest_video_published_at = latest.published_at

            channel.scraped_at = datetime.now(JST)
            logger.info(
                f"チャンネル取得完了: {channel.channel_name} "
                f"| 登録者: {channel.subscriber_count:,} "
                f"| 3ヶ月投稿: {channel.videos_3m_count}本"
            )

    except Exception as e:
        channel.error_message = str(e)
        logger.error(f"チャンネルデータ取得エラー [{channel_url}]: {e}")

    return channel


# ==================================================
# ICP 条件によるフィルタリング
# ==================================================

def filter_by_icp(channels: list[ChannelData]) -> list[ChannelData]:
    """
    ICP（理想顧客プロファイル）条件に合致するチャンネルのみを返す。

    フィルタ条件（config.py で設定可能）:
    - 直近3ヶ月で config.ICP_MIN_VIDEOS_3M 本以上投稿
    - 登録者数が ICP_MIN_SUBSCRIBERS 〜 ICP_MAX_SUBSCRIBERS の範囲内
    - チャンネル名・説明文が存在する（有効なチャンネルであること）

    Args:
        channels: フィルタ対象のチャンネルリスト

    Returns:
        list[ChannelData]: ICP条件を満たすチャンネルのリスト
    """
    passed = []
    filtered_out = []

    for ch in channels:
        reject_reason = ""

        # 有効データチェック
        if not ch.is_valid:
            reject_reason = "チャンネル情報が不完全"
        # エラーチェック
        elif ch.error_message:
            reject_reason = f"取得エラー: {ch.error_message}"
        # 登録者数の下限チェック
        elif ch.subscriber_count < config.ICP_MIN_SUBSCRIBERS:
            reject_reason = f"登録者数不足 ({ch.subscriber_count:,} < {config.ICP_MIN_SUBSCRIBERS:,})"
        # 登録者数の上限チェック
        elif ch.subscriber_count > config.ICP_MAX_SUBSCRIBERS:
            reject_reason = f"登録者数超過 ({ch.subscriber_count:,} > {config.ICP_MAX_SUBSCRIBERS:,})"
        # 直近3ヶ月の投稿数チェック
        elif ch.videos_3m_count < config.ICP_MIN_VIDEOS_3M:
            reject_reason = f"3ヶ月投稿数不足 ({ch.videos_3m_count} < {config.ICP_MIN_VIDEOS_3M})"
        else:
            passed.append(ch)
            continue

        filtered_out.append((ch.channel_name or ch.channel_url, reject_reason))

    # フィルタ結果のログ出力
    logger.info(f"ICP フィルタ結果: {len(passed)}件通過 / {len(filtered_out)}件除外")
    for name, reason in filtered_out[:10]:  # 最初の10件のみ表示
        logger.debug(f"  除外: {name} → {reason}")

    return passed


# ==================================================
# 将来の拡張: YouTube Data API v3 版
# ==================================================

def _get_channel_stats_api(channel_id: str, api_key: str) -> ChannelData:
    """
    【将来拡張用】YouTube Data API v3 を使ったチャンネルデータ取得。
    YOUTUBE_API_KEY を .env に設定すれば使用可能。
    現在はプレースホルダとして定義のみ。

    利点:
    - 取得データの精度が高い（登録者数が正確）
    - レート制限内であれば高速
    - 国・言語情報が正確に取得できる

    制限:
    - 1日10,000クォータ（無料枠）
    - チャンネルあたり数クォータ消費

    Args:
        channel_id: YouTube チャンネルID（UC〜で始まる文字列）
        api_key: YouTube Data API キー

    Returns:
        ChannelData: 取得したチャンネルデータ
    """
    # TODO: YouTube Data API v3 の実装
    # 参考: https://developers.google.com/youtube/v3/docs/channels/list
    raise NotImplementedError(
        "YouTube Data API 版は未実装です。"
        "YOUTUBE_API_KEY を .env に追加後、この関数を実装してください。"
    )


# ==================================================
# メイン処理（単体テスト用）
# ==================================================

if __name__ == "__main__":
    import sys

    logger.info("=== target_scraper.py 単体テスト ===")

    if len(sys.argv) > 1:
        # コマンドライン引数でチャンネルURLを指定した場合
        test_url = sys.argv[1]
        logger.info(f"チャンネルURL: {test_url}")
        result = get_channel_stats(test_url)
        print(f"\n--- 取得結果 ---")
        print(f"チャンネル名: {result.channel_name}")
        print(f"登録者数: {result.subscriber_count:,}")
        print(f"3ヶ月投稿数: {result.videos_3m_count}")
        print(f"平均再生数: {result.avg_view_count:.0f}")
        print(f"平均エンゲージ率: {result.avg_engagement_rate:.2%}")
        print(f"トレンド比率: {result.trend_ratio:.2f}")
        print(f"最新動画: {result.latest_video_title}")
    else:
        # デフォルト: キーワード検索のテスト
        logger.info("キーワード検索テスト（SerpAPIキーが必要）")
        urls = search_company_channels(["YouTube 企業 ビジネスチャンネル 商品紹介"])
        print(f"発見したチャンネル数: {len(urls)}")
        for url in urls[:5]:
            print(f"  - {url}")
