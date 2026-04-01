import os
import re
import time
import logging
import requests
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, List
from urllib.parse import urlparse
import config
from loguru import logger

# YouTube Data API v3 クライアント
class YouTubeCollector:
    """YouTube Data API v3 を使用したチャンネル収集"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://www.googleapis.com/youtube/v3'
        self.quota_used = 0
        
    def search_channels(self, keyword: str, max_results: int = 50) -> List[str]:
        """キーワードからチャンネルID を取得（100ユニット消費）"""
        try:
            params = {
                'part': 'snippet',
                'q': keyword,
                'type': 'channel',
                'maxResults': min(max_results, 50),
                'key': self.api_key,
                'relevanceLanguage': 'ja',
                'regionCode': 'JP',
                'order': 'relevance',
            }
            
            resp = requests.get(f'{self.base_url}/search', params=params, timeout=15)
            resp.raise_for_status()
            
            channel_ids = []
            for item in resp.json().get('items', []):
                if item.get('id', {}).get('kind') == 'youtube#channel':
                    channel_ids.append(item['id']['channelId'])
            
            self.quota_used += 100
            logger.info(f"YouTube 検索 '{keyword}': {len(channel_ids)} チャンネル見つかった（クォータ: {self.quota_used}）")
            
            return channel_ids
        except Exception as e:
            logger.error(f"YouTube 検索エラー (keyword={keyword}): {e}")
            return []
    
    def get_channels_batch(self, channel_ids: List[str]) -> List[dict]:
        """チャンネル詳細を一括取得"""
        if not channel_ids:
            return []
        
        try:
            channels = []
            for i in range(0, len(channel_ids), 50):
                batch = channel_ids[i:i+50]
                params = {
                    'part': 'snippet,statistics,brandingSettings',
                    'id': ','.join(batch),
                    'key': self.api_key,
                }
                
                resp = requests.get(f'{self.base_url}/channels', params=params, timeout=15)
                resp.raise_for_status()
                
                channels.extend(resp.json().get('items', []))
                self.quota_used += len(batch)
                time.sleep(1.0)
            
            logger.info(f"チャンネル詳細取得: {len(channels)} チャンネル（クォータ: {self.quota_used}）")
            return channels
        except Exception as e:
            logger.error(f"チャンネル詳細取得エラー: {e}")
            return []

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
    custom_url: Optional[str] = None
    
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

def parse_channel_data(youtube_channel: dict) -> Optional[ChannelData]:
    """YouTube API レスポンスを ChannelData に変換"""
    try:
        channel_id = youtube_channel.get('id', '')
        snippet = youtube_channel.get('snippet', {})
        stats = youtube_channel.get('statistics', {})
        branding = youtube_channel.get('brandingSettings', {})
        
        channel_name = snippet.get('title', '')
        description = snippet.get('description', '')
        subscriber_count = int(stats.get('subscriberCount', 0) or 0)
        view_count = int(stats.get('viewCount', 0) or 0)
        video_count = int(stats.get('videoCount', 0) or 0)
        custom_url = branding.get('channel', {}).get('customUrl', '')
        
        if custom_url:
            channel_url = f'https://www.youtube.com/@{custom_url}'
        else:
            channel_url = f'https://www.youtube.com/channel/{channel_id}'
        
        return ChannelData(
            channel_id=channel_id,
            channel_url=channel_url,
            channel_name=channel_name,
            description=description,
            subscriber_count=subscriber_count,
            view_count=view_count,
            video_count=video_count,
            custom_url=custom_url,
        )
    except Exception as e:
        logger.error(f"チャンネルデータ解析エラー: {e}")
        return None

def search_company_channels(keywords: List[str], max_per_keyword: int = 50) -> List[str]:
    """YouTube Data API を使用してチャンネルURL を収集"""
    collector = YouTubeCollector(config.YOUTUBE_API_KEY)
    all_channel_ids = []
    
    for keyword in keywords:
        channel_ids = collector.search_channels(keyword, max_per_keyword)
        all_channel_ids.extend(channel_ids)
        time.sleep(1.0)
    
    channel_urls = [f'https://www.youtube.com/channel/{cid}' for cid in all_channel_ids]
    
    logger.info(f"合計 {len(all_channel_ids)} チャンネルを取得（クォータ使用: {collector.quota_used}）")
    
    return channel_urls

def get_channel_stats(channel_url: str) -> Optional[ChannelData]:
    """チャンネルURL からチャンネル情報を取得"""
    if '/channel/' in channel_url:
        channel_id = channel_url.split('/channel/')[-1].rstrip('/')
    elif '/@' in channel_url:
        custom_url = channel_url.split('/@')[-1].rstrip('/')
        logger.warning(f"カスタムURL {custom_url} はスキップ")
        return None
    else:
        return None
    
    try:
        collector = YouTubeCollector(config.YOUTUBE_API_KEY)
        channels = collector.get_channels_batch([channel_id])
        
        if channels:
            return parse_channel_data(channels[0])
    except Exception as e:
        logger.error(f"チャンネル情報取得エラー [{channel_url}]: {e}")
    
    return None

def filter_by_icp(channels: List[ChannelData]) -> tuple[List[ChannelData], List[ChannelData]]:
    """ICP でフィルタリング"""
    passed = []
    rejected = []
    
    for ch in channels:
        if (config.ICP_MIN_SUBSCRIBERS <= ch.subscriber_count <= config.ICP_MAX_SUBSCRIBERS and
            ch.video_count >= config.ICP_MIN_VIDEOS_3M):
            passed.append(ch)
        else:
            rejected.append(ch)
    
    return passed, rejected

def deduplicate_urls(urls: list) -> list:
    """チャンネルURL の重複排除"""
    return list(set(urls))
