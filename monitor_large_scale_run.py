import subprocess
import os
import time
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("=== large_scale_run.py 完了監視開始 ===")
logger.info("ファイル: logs/large_scale_run_result.json")

# ポーリング間隔（秒）
POLL_INTERVAL = 30
MAX_WAIT_TIME = 3600  # 1時間

start_time = time.time()

while True:
    elapsed = time.time() - start_time
    
    # large_scale_run_result.json の確認
    if os.path.exists("logs/large_scale_run_result.json"):
        logger.info("✅ large_scale_run.py 完了を検知しました")
        
        # 結果を読み込み
        with open("logs/large_scale_run_result.json", 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        summary = results.get('summary', {})
        logger.info(f"📊 8ジャンル集計結果:")
        logger.info(f"   - 総チャンネル数: {summary.get('total_channels', 0)}")
        logger.info(f"   - 総メール数: {summary.get('total_emails', 0)}")
        logger.info(f"   - 平均成功率: {summary.get('average_rate', 0):.1f}%")
        
        # cache/email_data.json の確認
        if os.path.exists("cache/email_data.json"):
            with open("cache/email_data.json", 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            form_only = sum(1 for v in cache_data.values() if v.get('form_url') and not v.get('email'))
            logger.info(f"\n📋 Step 6b テスト対象:")
            logger.info(f"   - フォーム URL あり＆メールなし: {form_only} 件")
            logger.info(f"\n✅ test_step6b_production.py を実行準備完了")
            logger.info(f"コマンド: python test_step6b_production.py\n")
        
        break
    
    # タイムアウト確認
    if elapsed > MAX_WAIT_TIME:
        logger.error(f"❌ タイムアウト: {MAX_WAIT_TIME/60}分以上待機")
        break
    
    remaining = MAX_WAIT_TIME - elapsed
    minutes_remaining = remaining / 60
    logger.info(f"待機中... ({minutes_remaining:.0f}分以内に完了予定)")
    
    time.sleep(POLL_INTERVAL)

logger.info("=== 監視スクリプト終了 ===")
