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

# ログ設定
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

import signal
import json

def signal_handler(sig, frame):
    logger.warning(f'⏹️  中断されました。キャッシュを保存中...')
    logger.info('✅ キャッシュ保存完了')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def run_collect(keywords=None, dry_run=False, max_channels=150):
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
        return

    # Step 5: スコアリング
    logger.info("\n=== Step 5: スコアリング ===")
    scored_channels = score_channels(channels)
    logger.info(f"✅ スコアリング完了: {len(scored_channels)} 件")


    # Step 6: メールアドレス自動取得
    logger.info("\n=== Step 6: メールアドレス自動取得 ===")
    email_count = 0
    email_data = {}
    
    for i, ch in enumerate(scored_channels):
        if i % 10 == 0 and i > 0:
            logger.info(f"進捗: {i}/{len(scored_channels)}")

        channel_url = ch.channel_url
        company_name = ch.channel_name

        try:
            website_url, email, contact_form_url = get_email_from_youtube_channel(channel_url)
            ch.contact_email = email if email else ''
            ch.website_url = website_url if website_url else ''
            ch.contact_form_url = contact_form_url if contact_form_url else ''

            # メールアドレスの有効性チェック
            if email:
                from email_extractor import is_valid_email
                if not is_valid_email(email):
                    logger.warning(f'無効なメール（ドメイン未確認）: {email} → スキップ')
                    email = None
            
            if email:
                logger.info(f"✅ メール取得成功: {company_name} → {email}")
                email_count += 1
            elif contact_form_url:
                # ===== Step 6b: フォーム自動送信でメール抽出 =====
                logger.info(f"Step 6b 開始: フォーム送信 → {contact_form_url}")
                try:
                    from contact_form_extractor import FormSubmitter
                    submitter = FormSubmitter()
                    form_data = {
                        "company": company_name,
                        "email": "test@example.com",
                        "phone": "09000000000",
                        "message": "YouTube 営業活動"
                    }
                    extracted_email = submitter.submit_form(contact_form_url, form_data)
                    if extracted_email:
                        email = extracted_email
                        email_count += 1
                        logger.info(f"✅ フォーム送信でメール抽出: {company_name} → {email}")
                    else:
                        logger.debug(f"フォーム送信: メール未抽出 {company_name}")
                except Exception as e:
                    logger.warning(f"Step 6b エラー [{company_name}]: {e}")
            else:
                logger.debug(f"メール取得失敗: {company_name}")
        except Exception as e:
            logger.warning(f"メール抽出エラー [{company_name}]: {e}")

    logger.info(f"✅ Step 6 完了: {email_count}/{len(scored_channels)} 件のメール取得")

    # JSON にメール情報を保存（既存キャッシュとマージ）
    os.makedirs("cache", exist_ok=True)
    existing_data = {}
    if os.path.exists("cache/email_data.json"):
        try:
            with open("cache/email_data.json", "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except:
            pass
    existing_data.update(email_data)
    with open("cache/email_data.json", "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    logger.info(f"✅ メール情報保存: 累計 {len(existing_data)} 件（新規 {len(email_data)} 件）")

    # Step 7: CRM 更新
    logger.info("\n=== Step 7: CRM 更新 ===")
    
    if dry_run:
        logger.info(f"⏭️  DRY-RUN: {len(scored_channels)} 件のチャンネルをスキップ（更新しません）")
    else:
        for i, ch in enumerate(scored_channels):
            if i % 10 == 0 and i > 0:
                logger.info(f"進捗: {i}/{len(scored_channels)}")
            
            try:
                # lead_data を作成
                lead_data = ch.to_crm_dict()
                
                # JSON から取得したデータで上書き（確実に反映させる）
                channel_url = ch.channel_url
                if channel_url in email_data:
                    lead_data["メールアドレス"] = email_data[channel_url].get("email", "")
                    lead_data["公式サイト"] = email_data[channel_url].get("website", "")
                    lead_data["問い合わせフォームURL"] = email_data[channel_url].get("form_url", "")
                    logger.debug(f"JSON データを反映: {channel_url} → website={lead_data.get('公式サイト')}")
                
                upsert_lead(lead_data)
            except Exception as e:
                logger.warning(f"CRM 更新エラー [{ch.channel_name}]: {e}")
        
        logger.info(f"✅ CRM 更新: {len(scored_channels)} 件")

        # Step 7 の検証: メール情報が正常に保存されたか確認
        try:
            from utils import validate_crm_data_saved
            with_email, total = validate_crm_data_saved(min_email_ratio=0.5)
            logger.info(f"✅ CRM データ検証: {with_email}/{total} 件がメール情報を含む")
        except Exception as e:
            logger.error(f"❌ {str(e)}")

    # 最終報告
    logger.info("\n" + "=" * 70)
    logger.info("✅ 収集フロー完了")
    logger.info(f"  合計チャンネル: {len(scored_channels)} 件")
    logger.info(f"  メールアドレス取得: {email_count} 件")
    logger.info("=" * 70)


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
        sys.exit(1)


