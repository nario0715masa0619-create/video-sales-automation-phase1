import json
import os
import logging
from contact_form_extractor import FormSubmitter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s'
)
logger = logging.getLogger(__name__)

# cache/email_data.json からフォーム URL を取得
cache_file = "cache/email_data.json"

if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        email_data = json.load(f)
    
    logger.info(f"キャッシュ読み込み: {len(email_data)} チャンネル")
    
    # フォーム URL を持つがメール未抽出のチャンネルを抽出
    form_only_channels = [
        (url, data) for url, data in email_data.items()
        if data.get('form_url') and not data.get('email')
    ]
    
    logger.info(f"フォーム URL あり・メールなし: {len(form_only_channels)} チャンネル")
    
    # テスト対象（最初の 3 件）
    test_channels = form_only_channels[:3]
    
    submitter = FormSubmitter()
    test_form_data = {
        'company': 'テスト企業',
        'email': 'test@example.com',
        'phone': '09000000000',
        'message': 'YouTube 営業活動テスト'
    }
    
    logger.info(f"\n=== Step 6b 本番テスト開始（{len(test_channels)} 件） ===\n")
    
    for idx, (channel_url, data) in enumerate(test_channels, 1):
        form_url = data.get('form_url')
        logger.info(f"[{idx}/{len(test_channels)}] テスト: {form_url}")
        
        try:
            extracted_email = submitter.submit_form(form_url, test_form_data)
            if extracted_email:
                logger.info(f"  ✅ メール抽出成功: {extracted_email}")
            else:
                logger.info(f"  ⚠️ メール未抽出")
        except Exception as e:
            logger.error(f"  ❌ エラー: {e}")
    
    logger.info(f"\n=== Step 6b 本番テスト完了 ===\n")
else:
    logger.error(f"キャッシュファイルが見つかりません: {cache_file}")
