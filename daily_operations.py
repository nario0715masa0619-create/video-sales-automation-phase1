import subprocess
import sys
from datetime import datetime
from loguru import logger

logger.add('logs/daily_operations.log', rotation='500 MB')

def run_daily_operations(limit=15):
    """日次運用: バウンスチェック → メール送信"""
    logger.info("=" * 60)
    logger.info("🚀 日次運用開始")
    logger.info(f"実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # ステップ1: バウンスチェック（前日のバウンスを集計）
        logger.info("\n[Step 1] バウンスチェック開始...")
        result = subprocess.run(['python', 'bounce_checker.py'], check=True)
        logger.info("✅ バウンスチェック完了\n")
        
        # ステップ2: メール送信
        logger.info("[Step 2] メール送信開始...")
        result = subprocess.run(['python', 'send_email.py', '--limit', str(limit)], check=True)
        logger.info("✅ メール送信完了\n")
        
        logger.info("=" * 60)
        logger.info("🎉 日次運用完了")
        logger.info(f"終了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ エラー発生: {e}")
        return False
    
    return True

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=15)
    args = parser.parse_args()
    run_daily_operations(args.limit)


