import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
from loguru import logger

class CacheManager:
    """YouTube API のキャッシュ管理（ETag、検索結果、チャンネルインデックス）"""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        self.etag_file = self.cache_dir / "etag_cache.json"
        self.channel_index_file = self.cache_dir / "channel_index.json"
        self.search_cache_file = self.cache_dir / "search_cache.json"
        
        # キャッシュの有効期限（日数）
        self.CHANNEL_CACHE_DAYS = 30
        self.SEARCH_CACHE_DAYS = 7
        
        self._load_caches()
    
    def _load_caches(self):
        """ファイルからキャッシュを読み込む"""
        self.etag_cache = self._load_json(self.etag_file, {})
        self.channel_index = self._load_json(self.channel_index_file, {})
        self.search_cache = self._load_json(self.search_cache_file, {})
    
    def _load_json(self, filepath: Path, default: Any) -> Any:
        """JSON ファイルを安全に読み込む"""
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"キャッシュ読み込みエラー [{filepath.name}]: {e}")
        return default
    
    def _save_json(self, filepath: Path, data: Dict):
        """JSON ファイルに保存（UTF-8 BOMなし）"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"キャッシュ保存エラー [{filepath.name}]: {e}")
    
    # ===== ETag キャッシュ =====
    def get_etag(self, resource_key: str) -> Optional[str]:
        """保存済みの ETag を取得"""
        return self.etag_cache.get(resource_key)
    
    def set_etag(self, resource_key: str, etag: str):
        """ETag を保存"""
        self.etag_cache[resource_key] = etag
        self._save_json(self.etag_file, self.etag_cache)
    
    # ===== チャンネルインデックス =====
    def get_channel_id(self, keyword: str) -> Optional[str]:
        """キーワードから保存済みチャンネルID を取得"""
        entry = self.channel_index.get(keyword)
        if entry:
            # キャッシュ有効期限チェック
            cached_at = datetime.fromisoformat(entry.get('cached_at', ''))
            if (datetime.now() - cached_at).days < self.CHANNEL_CACHE_DAYS:
                return entry.get('channel_id')
        return None
    
    def set_channel_id(self, keyword: str, channel_id: str):
        """キーワードとチャンネルID を保存"""
        self.channel_index[keyword] = {
            'channel_id': channel_id,
            'cached_at': datetime.now().isoformat()
        }
        self._save_json(self.channel_index_file, self.channel_index)
    
    # ===== 検索キャッシュ =====
    def get_search_results(self, keyword: str) -> Optional[list]:
        """キーワード検索結果をキャッシュから取得"""
        entry = self.search_cache.get(keyword)
        if entry:
            cached_at = datetime.fromisoformat(entry.get('cached_at', ''))
            if (datetime.now() - cached_at).days < self.SEARCH_CACHE_DAYS:
                return entry.get('channel_ids', [])
        return None
    
    def set_search_results(self, keyword: str, channel_ids: list):
        """キーワード検索結果をキャッシュに保存"""
        self.search_cache[keyword] = {
            'channel_ids': channel_ids,
            'cached_at': datetime.now().isoformat()
        }
        self._save_json(self.search_cache_file, self.search_cache)
    
    def clear_expired_caches(self):
        """有効期限切れのキャッシュを削除"""
        # チャンネルインデックス
        expired_keywords = []
        for keyword, entry in self.channel_index.items():
            cached_at = datetime.fromisoformat(entry.get('cached_at', ''))
            if (datetime.now() - cached_at).days >= self.CHANNEL_CACHE_DAYS:
                expired_keywords.append(keyword)
        
        for keyword in expired_keywords:
            del self.channel_index[keyword]
            logger.info(f"期限切れチャンネルキャッシュを削除: {keyword}")
        
        if expired_keywords:
            self._save_json(self.channel_index_file, self.channel_index)
        
        # 検索キャッシュ
        expired_searches = []
        for keyword, entry in self.search_cache.items():
            cached_at = datetime.fromisoformat(entry.get('cached_at', ''))
            if (datetime.now() - cached_at).days >= self.SEARCH_CACHE_DAYS:
                expired_searches.append(keyword)
        
        for keyword in expired_searches:
            del self.search_cache[keyword]
            logger.info(f"期限切れ検索キャッシュを削除: {keyword}")
        
        if expired_searches:
            self._save_json(self.search_cache_file, self.search_cache)
