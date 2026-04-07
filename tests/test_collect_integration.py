import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')

from target_scraper import ChannelData

class TestCollectIntegration(unittest.TestCase):
    '''Step 6 と Step 7 の依存関係をテストする'''
    
    def test_step7_sets_contact_email_before_step6(self):
        '''Step 7 でメール設定 → Step 6 で保存される流れを検証'''
        ch = ChannelData(
            channel_id='test_id',
            channel_url='https://youtube.com/channel/test',
            channel_name='Test Channel',
            description='Test',
            subscriber_count=10000,
            view_count=100000,
            video_count=50
        )
        
        # Step 7 シミュレーション: メール情報を ch に設定
        ch.contact_email = 'test@example.com'
        ch.contact_form_url = 'https://example.com/contact'
        
        # Step 6 シミュレーション: to_crm_dict() でメール情報が含まれるか確認
        crm_dict = ch.to_crm_dict()
        
        # 検証: メールが to_crm_dict() に含まれているか
        self.assertIn('メールアドレス', crm_dict)
        self.assertEqual(crm_dict['メールアドレス'], 'test@example.com')
        self.assertIn('お問い合わせフォームURL', crm_dict)
        self.assertEqual(crm_dict['お問い合わせフォームURL'], 'https://example.com/contact')

    def test_channel_data_has_email_fields(self):
        '''ChannelData に contact_email フィールドがあるか確認'''
        ch = ChannelData(
            channel_id='test_id',
            channel_url='https://youtube.com/channel/test',
            channel_name='Test Channel',
            description='Test',
            subscriber_count=10000,
            view_count=100000,
            video_count=50
        )
        
        # フィールドが存在するか確認
        self.assertTrue(hasattr(ch, 'contact_email'))
        self.assertTrue(hasattr(ch, 'contact_form_url'))
        
        # デフォルト値が空文字列か確認
        self.assertEqual(ch.contact_email, '')
        self.assertEqual(ch.contact_form_url, '')

if __name__ == '__main__':
    unittest.main()
