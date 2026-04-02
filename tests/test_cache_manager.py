import unittest
import json
from pathlib import Path
from cache_manager import CacheManager

class TestCacheManager(unittest.TestCase):
    '''キャッシュ機能の完全テスト'''

    def setUp(self):
        self.cache = CacheManager()
        self.test_keyword = 'テストキーワード'
        self.test_data = ['UC1234567890abcdef', 'UC0987654321fedcba']

    def test_save_and_load_search_cache(self):
        '''キャッシュ保存と読み込みテスト'''
        # 保存
        self.cache.set_search_results(self.test_keyword, self.test_data)
        
        # 読み込み
        loaded = self.cache.get_search_results(self.test_keyword)
        
        # 検証
        self.assertIsNotNone(loaded, 'キャッシュが保存されていません')
        self.assertEqual(len(loaded), len(self.test_data), 'データ件数が一致しません')
        self.assertEqual(loaded[0], self.test_data[0], 'データ内容が一致しません')

    def test_cache_file_exists(self):
        '''キャッシュファイルが存在するかテスト'''
        # キャッシュ保存
        self.cache.set_search_results(self.test_keyword, self.test_data)
        
        # ファイルの存在確認
        cache_file = Path('cache/search_cache.json')
        self.assertTrue(cache_file.exists(), 'キャッシュファイルが存在しません')

    def test_all_12_keywords_can_be_cached(self):
        '''全12キーワードがキャッシュ可能かテスト'''
        keywords = [
            'YouTube活用', '動画マーケティング', 'オンライン営業', 'SNS活用',
            '動画集客', 'ウェビナー', 'YouTube広告', 'インフルエンサー',
            'チャンネル運用', 'コンテンツマーケティング', 'ビジネスYouTube', '企業動画'
        ]
        
        for kw in keywords:
            # キャッシュ保存
            self.cache.set_search_results(kw, [f'UC{kw}'])
        
        # すべてのキーワードが保存されているか確認
        with open('cache/search_cache.json', 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        self.assertEqual(len(cache_data), 12, f'キャッシュに{len(cache_data)}キーワードしかありません（期待値: 12）')
        
        # 各キーワードが読み込めるか確認
        for kw in keywords:
            loaded = self.cache.get_search_results(kw)
            self.assertIsNotNone(loaded, f'{kw} が読み込めません')
            self.assertEqual(loaded[0], f'UC{kw}', f'{kw} のデータが一致しません')

if __name__ == '__main__':
    unittest.main()
