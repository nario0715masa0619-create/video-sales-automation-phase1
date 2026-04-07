import sys
sys.path.insert(0, 'src')

import pickle
from loguru import logger

cache_file = 'cache/scored_channels.pkl'

try:
    with open(cache_file, 'rb') as f:
        scored_channels = pickle.load(f)
    
    logger.info("\n=== キャッシュから読み込んだデータ ===")
    logger.info(f"総数: {len(scored_channels)} 件")
    
    logger.info("\n=== 最初の3件のメール情報 ===")
    for i, ch in enumerate(scored_channels[:3]):
        logger.info(f"{i+1}. {ch.channel_name}")
        logger.info(f"   email: '{ch.contact_email}'")
        logger.info(f"   website: '{ch.website_url}'")
        logger.info(f"   form: '{ch.contact_form_url}'")
except Exception as e:
    logger.error(f"エラー: {e}")
