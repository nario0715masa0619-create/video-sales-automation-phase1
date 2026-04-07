# tests/test_api_fallback.py を作成
import unittest
from unittest.mock import patch, MagicMock
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from youtube_api_optimized import YouTubeAPIOptimized

class TestAPIFallback(unittest.TestCase):
    '''複数 API キーのフェイルオーバーテスト'''
    
    def test_multiple_api_keys_loaded(self):
        '''複数の API キーが .env から読み込まれるか確認'''
        with patch.dict(os.environ, {
            'YOUTUBE_API_KEY': 'key1',
            'YOUTUBE_API_KEY2': 'key2'
        }):
            api = YouTubeAPIOptimized(api_key=None)
            self.assertEqual(len(api.api_keys), 2)
            self.assertIn('key1', api.api_keys)
            self.assertIn('key2', api.api_keys)
    
    def test_api_key_fallback_on_403(self):
        '''403 エラー時に API キーが切り替わるか確認'''
        with patch.dict(os.environ, {
            'YOUTUBE_API_KEY': 'key1',
            'YOUTUBE_API_KEY2': 'key2'
        }):
            api = YouTubeAPIOptimized(api_key=None)
            self.assertEqual(api.current_api_key_index, 0)
            self.assertEqual(api.api_key, 'key1')
            
            # キーを切り替え
            result = api._switch_api_key()
            self.assertTrue(result)
            self.assertEqual(api.current_api_key_index, 1)
            self.assertEqual(api.api_key, 'key2')
    
    def test_fallback_fails_when_all_keys_exhausted(self):
        '''全てのキーが無効な場合 False を返すか確認'''
        with patch.dict(os.environ, {
            'YOUTUBE_API_KEY': 'key1',
            'YOUTUBE_API_KEY2': 'key2'
        }):
            api = YouTubeAPIOptimized(api_key=None)
            # 両方のキーを試す
            api._switch_api_key()  # key2 に切り替え
            result = api._switch_api_key()  # これは失敗すべき
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
