"""
target_scraper.py - YouTubeチャンネルスクレイピング（v3）

【修正履歴】
v1: 初期生成版（全指標が0になるバグあり）
v2: URLに /videos 付加 + RSS フィードで投稿日取得
v3: 登録者数フォールバック追加
    - yt-dlp の channel_follower_count が 0 の場合、
      ベースURLで再取得を試みる（古いyt-dlpバージョン対策）
    - それでも 0 の場合、HTML スクレイピングで取得
    - 数値パース関数を追加（万・千・K・M 対応）
"""

import re
import logging
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests
import yt_dlp

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# データクラス定義
# ─────────────────────────────────────────────

@dataclass
class ChannelData:
    """YouTubeチャンネルの取得データ"""
    channel_url: str            # 正規化後チャンネルURL（/videos なし）
    channel_name: str           # チャンネル名
    channel_id: str             # チャンネルID (UC...)
    subscriber_count: int       # 登録者数
    total_video_count: int      # 取得した動画数（最大30）
    recent_3m_count: int        # 直近3ヶ月の投稿数（RSS基準）
    avg_view_count: float       # 直近最大10本の平均再生数
    avg_engagement_rate: float  # エンゲージメント率（APIなし版: 0.0）
    growth_trend: str           # "上昇" / "横ばい" / "下降" / "不明"
    latest_video_title: str     # 最新動画タイトル（メール生成用）
    latest_video_url: str       # 最新動画URL
    fetched_at: str             # 取得日時
    contact_email: str = ""
    contact_form_url: str = ""
    icp_pass: bool = False
    icp_reject_reason: str = ""
    fetch_error: str = ""


@dataclass
class ICPConfig:
    """ICP（理想顧客プロファイル）条件設定"""
    min_subscribers: int = 500       # 最小登録者数
    max_subscribers: int = 50000     # 最大登録者数
    min_recent_3m_videos: int = 4    # 直近3ヶ月の最小投稿数
    recent_months: int = 3           # 判定対象月数


# ─────────────────────────────────────────────
# URL ユーティリティ
# ─────────────────────────────────────────────

def _normalize_channel_url(url: str) -> str:
    """
    任意の形式のYouTubeチャンネルURLを @channel/videos 形式に正規化する。
    例:
      https://m.youtube.com/@takagi1866/featured  → https://www.youtube.com/@takagi1866/videos
      https://www.youtube.com/c/msinsurance       → https://www.youtube.com/c/msinsurance/videos
    """
    url = url.replace('m.youtube.com', 'www.youtube.com')
    url = url.split('?')[0].rstrip('/')
    url = re.sub(r'/(featured|shorts|community|about|playlists|videos)$', '', url)
    return url + '/videos'


def _extract_base_channel_url(videos_url: str) -> str:
    """@channel/videos → @channel のベースURLを返す"""
    return re.sub(r'/videos$', '', videos_url)


# ─────────────────────────────────────────────
# 登録者数取得（3段階フォールバック）
# ─────────────────────────────────────────────

def _parse_subscriber_count(count_str: str) -> int:
    """
    YouTube の登録者数文字列を整数に変換する。
    対応フォーマット:
      'チャンネル登録者数 2,310人' → 2310
      '19.5万人'                   → 195000
      '51,000 subscribers'         → 51000
      '1.2M'                       → 1200000
    """
    s = re.sub(r'チャンネル登録者数\s*', '', count_str)
    s = re.sub(r'\s*(subscribers?|人)\s*', '', s, flags=re.IGNORECASE)
    s = s.replace(',', '').replace(' ', '').strip()

    units = [
        ('億', 100_000_000),
        ('万', 10_000),
        ('千', 1_000),
        ('M', 1_000_000),
        ('K', 1_000),
        ('k', 1_000),
    ]
    for suffix, mult in units:
        if suffix in s:
            try:
                return int(float(s.replace(suffix, '')) * mult)
            except ValueError:
                pass
    try:
        return int(float(s))
    except ValueError:
        return 0


def _get_subscriber_count_direct(base_url: str) -> int:
    """
    フォールバック①: ベースURL（/videos なし）で yt-dlp を再実行して
    channel_follower_count を取得する。
    古いyt-dlpバージョンでも /videos なしなら取れる場合がある。
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'playlistend': 1,
        'ignoreerrors': True,
        'socket_timeout': 15,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(base_url, download=False)
        if info:
            return int(info.get('channel_follower_count') or 0)
    except Exception as e:
        logger.debug(f"フォールバック① 失敗 ({base_url}): {e}")
    return 0


def _get_subscriber_count_from_html(base_url: str) -> int:
    """
    フォールバック②: チャンネルページのHTMLから登録者数をスクレイピング。
    subscriberCountText パターンを複数試みる。
    """
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept-Language': 'ja-JP,ja;q=0.9,en;q=0.8',
    }
    try:
        resp = requests.get(base_url, headers=headers, timeout=15)
        html = resp.text

        patterns = [
            r'"subscriberCountText":\{"simpleText":"([^"]+)"',
            r'"subscriberCountText":\{"accessibility":\{"accessibilityData":\{"label":"([^"]+)"',
            r'"subscriberCountText":\{"runs":\[.*?"text":"([^"]+)"',
        ]
        for pattern in patterns:
            m = re.search(pattern, html)
            if m:
                raw = m.group(1)
                # accessibility label は "チャンネル登録者数 2,310人" 形式
                # 数字部分だけ抽出してパース
                num_m = re.search(r'[\d,.]+\s*[万千億KkMm]?\s*人?', raw)
                target = num_m.group() if num_m else raw
                count = _parse_subscriber_count(target)
                if count > 0:
                    logger.debug(f"HTML スクレイピング成功: {raw} → {count:,}")
                    return count
    except Exception as e:
        logger.debug(f"フォールバック② 失敗 ({base_url}): {e}")
    return 0


def _resolve_subscriber_count(
    yt_dlp_count: int,
    base_url: str,
    channel_name: str,
) -> int:
    """
    登録者数を3段階で取得する。
    ① yt-dlp の channel_follower_count（/videos URL 取得時）
    ② yt-dlp の channel_follower_count（ベースURL で再取得）
    ③ HTML スクレイピング
    """
    # ① yt-dlp /videos URL からすでに取れていればそのまま使う
    if yt_dlp_count > 0:
        return yt_dlp_count

    logger.info(f"登録者数フォールバック開始: {channel_name}")

    # ② ベースURLで再取得
    count = _get_subscriber_count_direct(base_url)
    if count > 0:
        logger.info(f"  フォールバック①成功: {count:,}人")
        return count

    # ③ HTML スクレイピング
    count = _get_subscriber_count_from_html(base_url)
    if count > 0:
        logger.info(f"  フォールバック②成功: {count:,}人")
        return count

    logger.warning(f"  登録者数の取得に全て失敗: {channel_name}")
    return 0






def _extract_contact_info(description: str, channel_url: str) -> tuple[str, str]:
    """
    チャンネル説明文からメールアドレスとお問い合わせフォームURLを抽出する。
    
    Args:
        description: チャンネル説明文
        channel_url: チャンネルURL（ログ用）
        
    Returns:
        tuple[str, str]: (メールアドレス, お問い合わせフォームURL)
    """
    email = ""
    contact_form_url = ""
    
    if not description:
        return email, contact_form_url
    
    # メールアドレス抽出
    email_pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    email_matches = re.findall(email_pattern, description)
    exclude_domains = ['youtube.com', 'google.com', 'gmail.com', 'example.com']
    
    for m in email_matches:
        if not any(d in m.lower() for d in exclude_domains):
            email = m
            break
    
    # お問い合わせフォームURL抽出
    contact_patterns = [
        r'https?://[^\s\u3000-\u9fff]+(?:contact|inquiry|inquire|form|toiawase)[^\s\u3000-\u9fff]*',
    ]
    
    for pattern in contact_patterns:
        m = re.search(pattern, description, re.IGNORECASE)
        if m:
            contact_form_url = m.group(0).rstrip('.,)')
            break
    
    # フォールバック：contact_patterns でヒットしなかった場合、
    # 概要欄に含まれる最初の https:// で始まるURLを公式サイトURLとして取得
    if not contact_form_url:
        url_pattern = r'https?://(?!(?:www\.youtube\.com|youtu\.be|instagram\.com|twitter\.com|x\.com|facebook\.com|tiktok\.com|lit\.link|linktr\.ee|line\.me|bit\.ly|t\.co))[^\s\u3000-\u9fff]+'
        m = re.search(url_pattern, description)
        if m:
            contact_form_url = m.group(0).rstrip('.,)')
    
    return email, contact_form_url


# ─────────────────────────────────────────────
# RSS フィードによる投稿日取得
# ─────────────────────────────────────────────

def _get_recent_count_from_rss(channel_id: str, months: int = 3) -> int:
    """
    YouTube RSS フィードから直近N月の動画数を取得する。
    APIキー不要・高速（HTTPリクエスト1回）。RSSは最新15件を返す。

    Returns:
        直近 months ヶ月以内の動画数。エラー時は -1。
    """
    if not channel_id:
        return -1

    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        resp = requests.get(
            rss_url,
            timeout=10,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
        )
        resp.raise_for_status()

        root = ET.fromstring(resp.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        cutoff = datetime.now(timezone.utc) - timedelta(days=months * 30)
        count = 0

        for entry in root.findall('atom:entry', ns):
            pub = entry.find('atom:published', ns)
            if pub is not None and pub.text:
                try:
                    if datetime.fromisoformat(pub.text) >= cutoff:
                        count += 1
                except ValueError:
                    pass
        return count

    except requests.HTTPError as e:
        logger.warning(f"RSS HTTPエラー (channel_id={channel_id}): {e}")
    except ET.ParseError as e:
        logger.warning(f"RSS パースエラー (channel_id={channel_id}): {e}")
    except Exception as e:
        logger.warning(f"RSS 取得エラー (channel_id={channel_id}): {e}")
    return -1


# ─────────────────────────────────────────────
# yt-dlp チャンネルデータ取得
# ─────────────────────────────────────────────

def _ytdlp_extract(videos_url: str, max_videos: int = 30) -> Optional[dict]:
    """
    yt-dlp で @channel/videos プレイリストを extract_flat で取得する。
    取得できる主なフィールド:
      info['channel_follower_count'] : 登録者数（新しいyt-dlpのみ）
      info['channel_id']             : チャンネルID
      info['channel']                : チャンネル名
      entries[n]['view_count']       : 各動画の再生数
      entries[n]['title']            : 各動画タイトル
      entries[n]['id']               : 動画ID
    ※ upload_date / timestamp は extract_flat では None → RSS で補完
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist',
        'playlistend': max_videos,
        'ignoreerrors': True,
        'socket_timeout': 20,
        'retries': 2,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(videos_url, download=False)
    except Exception as e:
        logger.error(f"yt-dlp エラー ({videos_url}): {e}")
        return None


def _calc_growth_trend(view_counts: list) -> str:
    """
    再生数リスト（新しい順）からトレンドを判定する。
    最新5件 vs 古い5件を比較。
    """
    if len(view_counts) < 6:
        return "不明"
    recent_avg = sum(view_counts[:5]) / 5
    older_avg  = sum(view_counts[-5:]) / 5
    if older_avg == 0:
        return "不明"
    ratio = recent_avg / older_avg
    if ratio >= 1.15:
        return "上昇"
    elif ratio <= 0.85:
        return "下降"
    return "横ばい"


# ─────────────────────────────────────────────
# メイン関数: get_channel_stats
# ─────────────────────────────────────────────

def get_channel_stats(channel_url: str) -> Optional[ChannelData]:
    """
    YouTubeチャンネルの統計情報を取得する（APIキー不要版）。

    取得手順:
      1. URL正規化 → @channel/videos 形式に変換
      2. yt-dlp で動画リスト・再生数・登録者数を取得
      3. 登録者数が 0 なら 3段階フォールバックで再取得
      4. YouTube RSS で直近3ヶ月の投稿数を取得

    Args:
        channel_url: YouTube チャンネルURL（任意の形式）

    Returns:
        ChannelData（取得失敗時は None）
    """
    fetched_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # ── Step 1: URL 正規化 ──
    try:
        videos_url = _normalize_channel_url(channel_url)
        base_url   = _extract_base_channel_url(videos_url)
    except Exception as e:
        logger.error(f"URL正規化エラー ({channel_url}): {e}")
        return None

    # ── Step 2: yt-dlp でデータ取得 ──
    info = _ytdlp_extract(videos_url, max_videos=30)
    if not info:
        logger.warning(f"yt-dlp 取得失敗: {videos_url}")
        return None

    channel_name = (
        info.get('channel') or info.get('title') or info.get('uploader') or '不明'
    )
    channel_id = info.get('channel_id') or ''

    # ── Step 3: 登録者数（3段階フォールバック付き）──
    raw_sub_count = int(info.get('channel_follower_count') or 0)
    subscriber_count = _resolve_subscriber_count(raw_sub_count, base_url, channel_name)

    # ── 動画リスト処理 ──
    entries = [e for e in (info.get('entries') or []) if e is not None]
    view_counts = [
        float(e['view_count'])
        for e in entries
        if e.get('view_count') and e['view_count'] > 0
    ]
    avg_view_count = (
        sum(view_counts[:10]) / len(view_counts[:10]) if view_counts else 0.0
    )
    growth_trend = _calc_growth_trend(view_counts)

    latest_video_title = ''
    latest_video_url   = ''
    if entries:
        first = entries[0]
        latest_video_title = first.get('title') or ''
        vid_id = first.get('id') or ''
        if vid_id:
            latest_video_url = f"https://www.youtube.com/watch?v={vid_id}"

    # ── Step 4: RSS で直近3ヶ月投稿数 ──
    recent_3m_count = 0
    if channel_id:
        rss_count = _get_recent_count_from_rss(channel_id, months=3)
        if rss_count >= 0:
            recent_3m_count = rss_count
        else:
            recent_3m_count = min(len(entries), 3)
            logger.warning(f"RSS失敗のため推定値使用: {channel_name} → {recent_3m_count}件")
    # 連絡先情報の抽出
    description = info.get('description') or ''
    contact_email, contact_form_url = _extract_contact_info(description, base_url)


    return ChannelData(
        channel_url=base_url,
        channel_name=channel_name,
        channel_id=channel_id,
        subscriber_count=subscriber_count,
        total_video_count=len(entries),
        recent_3m_count=recent_3m_count,
        avg_view_count=avg_view_count,
        avg_engagement_rate=0.0,
        growth_trend=growth_trend,
        latest_video_title=latest_video_title,
        latest_video_url=latest_video_url,
        fetched_at=fetched_at,
        contact_email=contact_email,
        contact_form_url=contact_form_url,
    )


# ─────────────────────────────────────────────
# ICP フィルタリング
# ─────────────────────────────────────────────

def filter_by_icp(
    channels: list,
    config: Optional[ICPConfig] = None,
) -> tuple:
    """ICP条件でチャンネルリストをフィルタリングする。"""
    if config is None:
        config = ICPConfig()

    passed, rejected = [], []
    for ch in channels:
        reasons = []
        if ch.subscriber_count < config.min_subscribers:
            reasons.append(f"登録者数不足: {ch.subscriber_count:,} < {config.min_subscribers:,}")
        if ch.subscriber_count > config.max_subscribers:
            reasons.append(f"登録者数超過: {ch.subscriber_count:,} > {config.max_subscribers:,}")
        if ch.recent_3m_count < config.min_recent_3m_videos:
            reasons.append(
                f"投稿数不足: 直近3ヶ月{ch.recent_3m_count}本 < {config.min_recent_3m_videos}本"
            )
        if reasons:
            ch.icp_pass = False
            ch.icp_reject_reason = " / ".join(reasons)
            rejected.append(ch)
        else:
            ch.icp_pass = True
            passed.append(ch)

    logger.info(
        f"ICP フィルタ結果: {len(passed)}件通過 / {len(rejected)}件除外 / 計{len(channels)}件"
    )
    return passed, rejected


# ─────────────────────────────────────────────
# SerpAPI チャンネル候補検索
# ─────────────────────────────────────────────

def search_company_channels(
    keywords: list,
    serp_api_key: str,
    max_per_keyword: int = 10,
) -> list:
    """SerpAPI（Google検索）でYouTubeチャンネルURLを収集する。"""
    found_urls: set = set()

    for keyword in keywords:
        query = f"site:youtube.com/@ OR site:youtube.com/c {keyword}"
        params = {
            'engine': 'google',
            'q': query,
            'num': max_per_keyword,
            'api_key': serp_api_key,
            'hl': 'ja',
            'gl': 'jp',
        }
        try:
            resp = requests.get('https://serpapi.com/search', params=params, timeout=15)
            resp.raise_for_status()
            for result in resp.json().get('organic_results', []):
                link = result.get('link', '')
                if _is_youtube_channel_url(link):
                    found_urls.add(link)
            logger.info(f"SerpAPI検索 '{keyword}': {len(found_urls)}件（累計）")
            time.sleep(1.0)
        except Exception as e:
            logger.error(f"SerpAPI検索エラー (keyword={keyword}): {e}")

    return list(found_urls)


def _is_youtube_channel_url(url: str) -> bool:
    if not url:
        return False
    return any(re.search(p, url) for p in [
        r'youtube\.com/@[\w\-]+',
        r'youtube\.com/c/[\w\-]+',
        r'youtube\.com/channel/UC[\w\-]+',
        r'youtube\.com/user/[\w\-]+',
    ])


def deduplicate_urls(urls: list) -> list:
    """チャンネルURLリストから重複・バリアントを除去する。"""
    seen: set = set()
    unique = []
    for url in urls:
        try:
            base = _extract_base_channel_url(_normalize_channel_url(url))
        except Exception:
            base = url
        if base not in seen:
            seen.add(base)
            unique.append(url)
    return unique


# ─────────────────────────────────────────────
# メインパイプライン
# ─────────────────────────────────────────────

def run_scraping_pipeline(
    keywords: list,
    serp_api_key: str,
    icp_config: Optional[ICPConfig] = None,
    sleep_between_channels: float = 1.5,
) -> tuple:
    """
    スクレイピングのメインパイプライン。
    1. SerpAPI でチャンネルURL収集
    2. 重複排除
    3. 各チャンネルの統計データ取得
    4. ICP フィルタリング
    """
    logger.info(f"チャンネルURL収集開始: {len(keywords)}キーワード")
    raw_urls    = search_company_channels(keywords, serp_api_key)
    unique_urls = deduplicate_urls(raw_urls)
    logger.info(f"チャンネル候補: {len(unique_urls)}件（重複排除後）")

    all_channels = []
    for i, url in enumerate(unique_urls, 1):
        logger.info(f"チャンネル取得 [{i}/{len(unique_urls)}]: {url}")
        ch = get_channel_stats(url)
        if ch:
            logger.info(
                f"取得完了: {ch.channel_name} | "
                f"登録者: {ch.subscriber_count:,} | "
                f"3ヶ月投稿: {ch.recent_3m_count}本 | "
                f"平均再生: {ch.avg_view_count:.0f}"
            )
            all_channels.append(ch)
        else:
            logger.warning(f"取得失敗: {url}")
        if i < len(unique_urls):
            time.sleep(sleep_between_channels)

    return filter_by_icp(all_channels, icp_config)


# ─────────────────────────────────────────────
# 単体テスト
# ─────────────────────────────────────────────

if __name__ == '__main__':
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
    )

    test_urls = sys.argv[1:] if len(sys.argv) > 1 else [
        'https://www.youtube.com/@takagi1866',
        'https://www.youtube.com/c/msinsurance',
        'https://www.youtube.com/@SoftBankBiz',
        'https://www.youtube.com/@netschoolcorp',
        'https://www.youtube.com/@d2cstation331',
    ]

    print(f"\n{'='*60}")
    print(f"  target_scraper.py v3 動作確認テスト")
    print(f"{'='*60}\n")

    results = []
    for url in test_urls:
        print(f"■ {url}")
        ch = get_channel_stats(url)
        if ch:
            print(f"  チャンネル名:  {ch.channel_name}")
            print(f"  登録者数:      {ch.subscriber_count:,}")
            print(f"  3ヶ月投稿数:  {ch.recent_3m_count}本")
            print(f"  平均再生数:    {ch.avg_view_count:.0f}")
            print(f"  成長トレンド:  {ch.growth_trend}")
            print(f"  最新動画:      {ch.latest_video_title[:45]}")
            results.append(ch)
        else:
            print(f"  ❌ 取得失敗")
        print()
        time.sleep(1.5)

    print(f"{'='*60}")
    print("  ICP フィルタリング結果")
    print(f"{'='*60}")
    passed, rejected = filter_by_icp(results)

    print(f"\n✅ 通過: {len(passed)}件")
    for ch in passed:
        print(f"  - {ch.channel_name}（登録者:{ch.subscriber_count:,} / 3M:{ch.recent_3m_count}本）")

    print(f"\n❌ 除外: {len(rejected)}件")
    for ch in rejected:
        print(f"  - {ch.channel_name}: {ch.icp_reject_reason}")







