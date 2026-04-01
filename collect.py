import argparse
import os
import sys
from datetime import datetime
from pytz import timezone
import config
from loguru import logger
from target_scraper import (
    search_company_channels, get_channel_stats, filter_by_icp, 
    get_channel_recent_videos, print_quota_status, yt_api
)
from scorer import score_channels
from crm_manager import upsert_lead
from email_extractor import get_email_from_youtube_channel
from utils import normalize_url

# ログ設定（修正版：TIME のフォーマット指定）
logger.remove()
logger.add(
    sys.stderr,
    format="<level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/collect.log",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {message}",
    level="DEBUG",
    rotation="500 MB"
)

def run_collect(keywords=None, dry_run=False):
    """
    YouTube Data API 最適化版 チャンネル収集フロー
    
    クォータ効率設計:
    - 初期検索: search.list (100pt/キーワード) ×12 = 1,200pt
    - チャンネル詳細: channels.list (1pt) ×50 = 50pt
    - 動画取得: uploads プレイリスト経由のみ (1pt/チャンネル) = 50pt
    - 合計: 約 1,300pt（キャッシュヒット時はさらに削減）
    
    Args:
        keywords (list): 検索キーワード（None の場合はデフォルト使用）
        dry_run (bool): ドライランモード
    """
    logger.info("=" * 70)
    logger.info("📊 収集フロー開始（YouTube Data API 最適化版）")
    logger.info("=" * 70)
    
    # デフォルトキーワード
    if not keywords:
        keywords = config.DEFAULT_SEARCH_KEYWORDS
    
    logger.info(f"キーワード数: {len(keywords)}")
    logger.info(f"キーワード: {keywords}")
    
    # Step 1: YouTube Data API でチャンネル検索
    logger.info("\n=== Step 1: チャンネル検索（search.list） ===")
    all_urls = search_company_channels(keywords, max_per_keyword=50)
    logger.info(f"✅ 検索結果: {len(all_urls)} チャンネル取得")
    
    if not all_urls:
        logger.warning("❌ チャンネル候補なし。終了。")
        print_quota_status()
        return
    
    # Step 2: チャンネル情報の詳細取得
    logger.info("\n=== Step 2: チャンネル詳細取得（channels.list） ===")
    channels = []
    for i, url in enumerate(all_urls):
        if i % 20 == 0 and i > 0:
            logger.info(f"進捗: {i}/{len(all_urls)}")
        
        try:
            stats = get_channel_stats(url)
            if stats:
                channels.append(stats)
        except Exception as e:
            logger.warning(f"チャンネル詳細取得エラー [{url}]: {e}")
    
    logger.info(f"✅ 詳細取得完了: {len(channels)} チャンネル")
    
    # Step 3: ICP フィルタリング
    logger.info("\n=== Step 3: ICP フィルタリング ===")
    passed_channels, rejected_channels = filter_by_icp(channels)
    logger.info(f"フィルタリング前: {len(channels)} 件")
    logger.info(f"✅ 合格: {len(passed_channels)} 件")
    logger.info(f"❌ 除外: {len(rejected_channels)} 件")
    
    channels = passed_channels
    
    # Step 4: 重複排除
    logger.info("\n=== Step 4: 重複排除 ===")
    unique_channels = {ch.channel_url: ch for ch in channels}
    channels = list(unique_channels.values())
    logger.info(f"✅ 重複排除後: {len(channels)} 件")
    
    if not channels:
        logger.warning("❌ フィルタリング後にチャンネルなし。終了。")
        print_quota_status()
        return
    
    # Step 5: スコアリング
    logger.info("\n=== Step 5: スコアリング ===")
    scored_channels = score_channels(channels)
    logger.info(f"✅ スコアリング完了: {len(scored_channels)} 件")
    
    # Step 6: CRM 更新
    logger.info("\n=== Step 6: CRM 更新 ===")
    if not dry_run:
        for i, ch in enumerate(scored_channels):
            if i % 10 == 0 and i > 0:
                logger.info(f"進捗: {i}/{len(scored_channels)}")
            try:
                lead_data = ch.to_crm_dict()
                upsert_lead(lead_data)
            except Exception as e:
                logger.warning(f"CRM 更新エラー [{ch.channel_name}]: {e}")
        logger.info(f"✅ CRM 更新: {len(scored_channels)} 件")
    else:
        logger.info(f"⏭️  DRY-RUN: {len(scored_channels)} 件のチャンネルをスキップ（更新しません）")
    
    # Step 7: メールアドレス抽出
    logger.info("\n=== Step 7: メールアドレス自動取得 ===")
    email_count = 0
    for i, ch in enumerate(scored_channels):
        if i % 10 == 0 and i > 0:
            logger.info(f"進捗: {i}/{len(scored_channels)}")
        
        channel_url = ch.channel_url
        company_name = ch.channel_name
        
        try:
            email = get_email_from_youtube_channel(channel_url)
            if email:
                logger.info(f"✅ メール取得成功: {company_name} → {email}")
                email_count += 1
            else:
                logger.debug(f"メール取得失敗: {company_name}")
        except Exception as e:
            logger.warning(f"メール抽出エラー [{company_name}]: {e}")
    
    logger.info(f"✅ Step 7 完了: {email_count} 件のメール取得")
    
    # 最終報告
    logger.info("\n" + "=" * 70)
    logger.info("✅ 収集フロー完了")
    logger.info(f"  合計チャンネル: {len(scored_channels)} 件")
    logger.info(f"  メールアドレス取得: {email_count} 件")
    logger.info("=" * 70)
    
    # クォータ使用状況を表示
    print_quota_status()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="YouTube Data API 最適化版 - チャンネル収集スクリプト"
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        help="検索キーワード（指定しない場合はデフォルト）"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="ドライランモード（CRM に更新しない）"
    )
    
    args = parser.parse_args()
    
    try:
        run_collect(keywords=args.keywords, dry_run=args.dry_run)
    except KeyboardInterrupt:
        logger.warning("⏹️  ユーザーによる中断")
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        print_quota_status()
        sys.exit(1)
