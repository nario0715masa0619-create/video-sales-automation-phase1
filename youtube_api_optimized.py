import requests
import time
from typing import Optional, Dict, List, Any
from loguru import logger
import config
from cache_manager import CacheManager

class YouTubeAPIOptimized:
    """YouTube Data API v3 クォータ最適化版"""
    
    def __init__(self, api_key: str, cache_dir: str = "cache"):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.cache = CacheManager(cache_dir)
        self.quota_used = 0
        
        # リトライ設定
        self.max_retries = 3
        self.retry_wait = 2  # 秒
        
        logger.info("YouTubeAPIOptimized を初期化しました")
    
    def _request_with_etag(self, method: str, endpoint: str, params: Dict, 
                          resource_key: str) -> tuple[Optional[Dict], int]:
        """ETag ベースのリクエスト（304 対応）"""
        
        # 保存済み ETag を取得
        saved_etag = self.cache.get_etag(resource_key)
        headers = {}
        if saved_etag:
            headers['If-None-Match'] = saved_etag
        
        for attempt in range(self.max_retries):
            try:
                params['key'] = self.api_key
                resp = requests.request(method, endpoint, params=params, 
                                       headers=headers, timeout=15)
                
                # 304 Not Modified
                if resp.status_code == 304:
                    logger.debug(f"キャッシュヒット（304）: {resource_key}")
                    return None, 0  # クォータ消費なし（帯域は節約）
                
                resp.raise_for_status()
                
                # ETag を保存
                if 'ETag' in resp.headers:
                    self.cache.set_etag(resource_key, resp.headers['ETag'])
                
                # クォータ消費を推定
                quota_cost = self._estimate_quota(endpoint, params)
                self.quota_used += quota_cost
                
                return resp.json(), quota_cost
            
            except requests.exceptions.Timeout:
                logger.warning(f"タイムアウト [{resource_key}] 再試行 {attempt+1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_wait * (attempt + 1))
            
            except requests.exceptions.HTTPError as e:
                if resp.status_code == 403:
                    logger.error(f"403 Forbidden: API キーまたはクォータの問題 [{resource_key}]")
                    return None, 0
                elif resp.status_code == 404:
                    logger.warning(f"404 Not Found: {resource_key}")
                    return None, 0
                else:
                    logger.error(f"HTTP エラー {resp.status_code} [{resource_key}]: {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_wait * (attempt + 1))
            
            except Exception as e:
                logger.error(f"リクエストエラー [{resource_key}]: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_wait)
        
        logger.error(f"リトライ失敗: {resource_key}")
        return None, 0
    
    def _estimate_quota(self, endpoint: str, params: Dict) -> int:
        """API エンドポイントのクォータ消費を推定"""
        if 'search' in endpoint:
            return 100  # search.list
        elif 'channels' in endpoint:
            return 1   # channels.list
        elif 'playlistItems' in endpoint:
            return 1   # playlistItems.list
        elif 'videos' in endpoint:
            return 1   # videos.list
        else:
            return 1
    
    # ===== チャンネル検索（search.list） =====
    def search_channels(self, keyword: str, max_results: int = 50) -> List[str]:
        """
        キーワードからチャンネルを検索（初期発見用のみ）
        クォータ: 100pt/リクエスト
        """
        # キャッシュから取得
        cached = self.cache.get_search_results(keyword)
        if cached:
            logger.info(f"検索キャッシュヒット: {keyword} ({len(cached)} チャンネル)")
            return cached
        
        logger.info(f"YouTube 検索開始: {keyword}")
        
        params = {
            'part': 'snippet',
            'q': keyword,
            'type': 'channel',
            'maxResults': min(max_results, 50),
            'relevanceLanguage': 'ja',
            'regionCode': 'JP',
            'order': 'relevance',
        }
        
        endpoint = f"{self.base_url}/search"
        data, quota = self._request_with_etag('GET', endpoint, params, 
                                              f"search:{keyword}")
        
        if not data:
            return []
        
        channel_ids = []
        for item in data.get('items', []):
            if item.get('id', {}).get('kind') == 'youtube#channel':
                channel_id = item['id']['channelId']
                channel_ids.append(channel_id)
        
        # 検索結果をキャッシュに保存
        self.cache.set_search_results(keyword, channel_ids)
        
        logger.info(f"検索完了: {keyword} → {len(channel_ids)} チャンネル（クォータ消費: {quota}）")
        return channel_ids
    
    # ===== チャンネル詳細取得 =====
    def get_channel_uploads_playlist(self, channel_id: str) -> Optional[str]:
        """
        チャンネルの uploads プレイリスト ID を取得
        クォータ: 1pt
        """
        params = {
            'part': 'contentDetails',
            'id': channel_id,
            'fields': 'items(contentDetails/relatedPlaylists/uploads),etag',
        }
        
        endpoint = f"{self.base_url}/channels"
        data, quota = self._request_with_etag('GET', endpoint, params, 
                                              f"channel_uploads:{channel_id}")
        
        if not data or not data.get('items'):
            logger.warning(f"チャンネル uploads プレイリスト取得失敗: {channel_id}")
            return None
        
        uploads_id = data['items'][0].get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads')
        logger.debug(f"Uploads プレイリスト: {channel_id} → {uploads_id}")
        
        return uploads_id
    
    def get_channel_details(self, channel_id: str) -> Optional[Dict]:
        """
        チャンネルの基本情報を取得
        クォータ: 1pt
        """
        params = {
            'part': 'snippet,statistics',
            'id': channel_id,
            'fields': (
                'items('
                'id,'
                'snippet/title,'
                'snippet/description,'
                'statistics/subscriberCount,'
                'statistics/viewCount,'
                'statistics/videoCount'
                '),etag'
            ),
        }
        
        endpoint = f"{self.base_url}/channels"
        data, quota = self._request_with_etag('GET', endpoint, params, 
                                              f"channel_details:{channel_id}")
        
        if not data or not data.get('items'):
            return None
        
        return data['items'][0]
    
    # ===== 動画取得（Uploads プレイリスト経由） =====
    def get_playlist_videos(self, playlist_id: str, max_results: int = 50,
                           page_token: Optional[str] = None) -> tuple[List[Dict], Optional[str], int]:
        """
        プレイリスト（uploads）から動画一覧を取得
        クォータ: 1pt/ページ
        """
        params = {
            'part': 'snippet,contentDetails',
            'playlistId': playlist_id,
            'maxResults': min(max_results, 50),
            'fields': (
                'items('
                'snippet/title,'
                'snippet/publishedAt,'
                'contentDetails/videoId'
                '),'
                'nextPageToken,'
                'etag'
            ),
        }
        
        if page_token:
            params['pageToken'] = page_token
        
        endpoint = f"{self.base_url}/playlistItems"
        data, quota = self._request_with_etag('GET', endpoint, params, 
                                              f"playlist_items:{playlist_id}:{page_token or 'page1'}")
        
        if not data:
            return [], None, quota
        
        videos = data.get('items', [])
        next_token = data.get('nextPageToken')
        
        logger.debug(f"プレイリスト動画取得: {playlist_id} → {len(videos)} 動画")
        
        return videos, next_token, quota
    
    def get_videos_stats(self, video_ids: List[str]) -> Dict[str, Dict]:
        """
        複数動画の統計情報を取得（最大50件/リクエスト）
        クォータ: 1pt
        """
        if not video_ids:
            return {}
        
        all_videos = {}
        
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            
            params = {
                'part': 'statistics',
                'id': ','.join(batch),
                'fields': (
                    'items('
                    'id,'
                    'statistics/viewCount,'
                    'statistics/likeCount,'
                    'statistics/commentCount'
                    '),etag'
                ),
            }
            
            endpoint = f"{self.base_url}/videos"
            data, quota = self._request_with_etag('GET', endpoint, params, 
                                                  f"videos_stats:{','.join(batch[:3])}...")
            
            if data:
                for item in data.get('items', []):
                    all_videos[item['id']] = item.get('statistics', {})
        
        return all_videos
    
    def get_quota_status(self) -> Dict:
        """クォータ使用状況を返す"""
        return {
            'quota_used': self.quota_used,
            'quota_limit': 10000,
            'remaining': 10000 - self.quota_used,
            'utilization_percent': round((self.quota_used / 10000) * 100, 2)
        }
