import os
import re
import time
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Tuple
from urllib.parse import urlparse
import config
from loguru import logger
from youtube_api_optimized import YouTubeAPIOptimized

# YouTube API 初期化
yt_api = YouTubeAPIOptimized(config.YOUTUBE_API_KEY, cache_dir="cache")

@dataclass
class ChannelData:
    """YouTube チャンネルデータ"""
    channel_id: str
    channel_url: str
    channel_name: str
    description: str
    subscriber_count: int
    view_count: int
    video_count: int
    recent_3m_count: int = 0
    avg_view_count: float = 0.0
    avg_engagement_rate: float = 0.0
    growth_trend: str = "安定"
    custom_url: Optional[str] = None
    contact_email: str = ""
    contact_form_url: str = ""
    latest_video_url: str = ""
    latest_video_title: str = ""
    latest_video_title: str = ""
    
    def to_crm_dict(self) -> dict:
        """CRM 用の辞書形式に変換"""
        return {
            'チャンネルURL': self.channel_url,
            'チャンネル名': self.channel_name,
            '説明文': self.description,
            'チャンネル登録者数': self.subscriber_count,
            '総視聴数': self.view_count,
            '動画数': self.video_count,
        }

def parse_channel_data(channel_id: str, youtube_data: dict) -> Optional[ChannelData]:
    """YouTube API レスポンスを ChannelData に変換"""
    try:
        snippet = youtube_data.get('snippet', {})
        stats = youtube_data.get('statistics', {})
        
        channel_name = snippet.get('title', '')
        description = snippet.get('description', '')
        subscriber_count = int(stats.get('subscriberCount', 0) or 0)
        view_count = int(stats.get('viewCount', 0) or 0)
        video_count = int(stats.get('videoCount', 0) or 0)
        
        # チャンネルURL の構築
        channel_url = f'https://www.youtube.com/channel/{channel_id}'
        
        # 平均再生数を推定（総視聴数 / 動画数）
        avg_view_count = 0.0
        if video_count > 0:
            avg_view_count = view_count / video_count
        
        # 平均エンゲージメント率は初期値（詳細動画取得時に更新可能）
        avg_engagement_rate = 0.02  # デフォルト 2%
        
        return ChannelData(
            channel_id=channel_id,
            channel_url=channel_url,
            channel_name=channel_name,
            description=description,
            subscriber_count=subscriber_count,
            view_count=view_count,
            video_count=video_count,
            recent_3m_count=0,
            avg_view_count=avg_view_count,
            avg_engagement_rate=avg_engagement_rate,
            growth_trend="安定",
        )
    except Exception as e:
        logger.error(f"チャンネルデータ解析エラー [{channel_id}]: {e}")
        return None

def search_company_channels(keywords: List[str], max_per_keyword: int = 50) -> List[str]:
    """
    YouTube Data API を使用してチャンネルURL を収集
    
    クォータ効率:
    - search.list: 100pt × キーワード数
    - キャッシュヒット時: 0pt
    
    Args:
        keywords: 検索キーワードのリスト
        max_per_keyword: キーワードあたりの検索結果数
    
    Returns:
        チャンネルURL のリスト
    """
    all_channel_ids = []
    
    for keyword in keywords:
        try:
            channel_ids = yt_api.search_channels(keyword, max_per_keyword)
            all_channel_ids.extend(channel_ids)
            time.sleep(1.0)  # Rate limiting
        except Exception as e:
            logger.error(f"キーワード検索エラー [{keyword}]: {e}")
    
    # チャンネルID からチャンネルURL を構築
    channel_urls = [f'https://www.youtube.com/channel/{cid}' for cid in all_channel_ids]
    
    quota_status = yt_api.get_quota_status()
    logger.info(f"チャンネル検索完了: {len(all_channel_ids)} チャンネル")
    logger.info(f"クォータ使用: {quota_status['quota_used']}/{quota_status['quota_limit']} "
                f"({quota_status['utilization_percent']}%)")
    
    return channel_urls

def get_channel_stats(channel_url: str) -> Optional[ChannelData]:
    """
    チャンネルURL からチャンネル情報を取得
    
    クォータ効率:
    - channels.list: 1pt
    
    Args:
        channel_url: YouTube チャンネルURL
    
    Returns:
        ChannelData または None
    """
    # チャンネルID を抽出
    if '/channel/' in channel_url:
        channel_id = channel_url.split('/channel/')[-1].rstrip('/')
    else:
        logger.warning(f"チャンネルID 抽出失敗: {channel_url}")
        return None
    
    try:
        # チャンネル詳細を取得
        youtube_data = yt_api.get_channel_details(channel_id)
        
        if youtube_data:
            return parse_channel_data(channel_id, youtube_data)
    except Exception as e:
        logger.error(f"チャンネル情報取得エラー [{channel_url}]: {e}")
    
    return None

def get_channel_recent_videos(channel_id: str, max_videos: int = 30) -> Tuple[List[dict], int]:
    """
    チャンネルから最近の動画を取得（Uploads プレイリスト経由）
    
    クォータ効率:
    - channels.list (uploads ID 取得): 1pt
    - playlistItems.list: 1pt/ページ
    - videos.list (統計情報): 1pt
    
    Args:
        channel_id: YouTube チャンネルID
        max_videos: 取得する動画の最大数
    
    Returns:
        (動画リスト, クォータ消費)
    """
    quota_start = yt_api.quota_used
    
    try:
        # Uploads プレイリスト ID を取得
        uploads_playlist_id = yt_api.get_channel_uploads_playlist(channel_id)
        if not uploads_playlist_id:
            logger.warning(f"Uploads プレイリスト ID 取得失敗: {channel_id}")
            return [], yt_api.quota_used - quota_start
        
        # プレイリストから動画を取得
        all_videos = []
        page_token = None
        
        while len(all_videos) < max_videos:
            videos, page_token, quota = yt_api.get_playlist_videos(
                uploads_playlist_id, 
                max_results=min(50, max_videos - len(all_videos)),
                page_token=page_token
            )
            
            all_videos.extend(videos)
            
            if not page_token:
                break
        
        # 動画の統計情報を取得
        video_ids = [v['contentDetails']['videoId'] for v in all_videos[:max_videos]]
        video_stats = yt_api.get_videos_stats(video_ids)
        
        logger.debug(f"動画取得完了: {channel_id} → {len(all_videos)} 動画")
        
        return all_videos[:max_videos], yt_api.quota_used - quota_start
    
    except Exception as e:
        logger.error(f"動画取得エラー [{channel_id}]: {e}")
        return [], yt_api.quota_used - quota_start

def filter_by_icp(channels: List[ChannelData]) -> Tuple[List[ChannelData], List[ChannelData]]:
    """ICP（理想的な顧客プロフィール）でフィルタリング"""
    passed = []
    rejected = []
    
    for ch in channels:
        if (config.ICP_MIN_SUBSCRIBERS <= ch.subscriber_count <= config.ICP_MAX_SUBSCRIBERS):
            passed.append(ch)
        else:
            rejected.append(ch)
    
    return passed, rejected

def deduplicate_urls(urls: list) -> list:
    """チャンネルURL の重複排除"""
    return list(set(urls))

def print_quota_status():
    """クォータ使用状況を表示"""
    status = yt_api.get_quota_status()
    logger.info("="*60)
    logger.info(f"📊 クォータ使用状況")
    logger.info(f"  使用: {status['quota_used']}/{status['quota_limit']} ユニット")
    logger.info(f"  残り: {status['remaining']} ユニット")
    logger.info(f"  使用率: {status['utilization_percent']}%")
    logger.info("="*60)
