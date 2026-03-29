#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
collect.py
YouTube チャンネル候補のスクレイピング、スコアリング、CRM 登録、メール抽出
"""
import os
import sys
from datetime import datetime
from pytz import timezone
from loguru import logger

# ローカルモジュール
from target_scraper import run_scraping_pipeline, filter_by_icp
from scorer import score_channels
from crm_manager import upsert_lead
from email_extractor import get_email_from_youtube_channel

JST = timezone('Asia/Tokyo')

def run_collect(keywords=None, dry_run=False):
    """
    YouTube チャンネル収集フロー
    
    Args:
        keywords (list): 検索キーワード（None の場合はデフォルト使用）
        dry_run (bool): ドライランモード
    """
    logger.info("=" * 60)
    logger.info("収集フロー開始")
    logger.info("=" * 60)
    
    # デフォルトキーワード
    if not keywords:
        keywords = [
            'YouTube 集客', 'セミナー YouTube', 'オンライン講座 YouTube',
            'ウェビナー YouTube', 'スクール YouTube', '教室 YouTube',
            'クリニック YouTube', 'ジム YouTube', '整体院 YouTube',
            '学習塾 YouTube', '士業 YouTube', 'コーチング YouTube'
        ]
    
    logger.info(f"キーワード: {keywords}")
    
    # Step 1: スクレイピング
    logger.info("\n=== Step 1: ターゲット候補の検索・スクレイピング ===")
    channels = run_scraping_pipeline(keywords)
    logger.info(f"チャンネル候補: {len(channels)}件")
    
    if not channels:
        logger.warning("チャンネル候補なし。終了。")
        return
    
    # Step 2+3: スコアリングと CRM 更新
    logger.info("\n=== Step 2+3: スコアリングと CRM 更新 ===")
    scored_channels = score_channels(channels)
    logger.info(f"スコアリング完了: {len(scored_channels)}件")
    
    # CRM に登録
    for ch in scored_channels:
        lead_data = ch.to_crm_dict()
        upsert_lead(lead_data)
    logger.info(f"CRM 更新: {len(scored_channels)}件")
    
    # Step 3.5: メールアドレス抽出
    logger.info("\n=== Step 3.5: メールアドレス自動取得 ===")
    email_count = 0
    for ch in scored_channels:
        channel_url = ch.get("url")
        company_name = ch.get("company_name")
        try:
            email = get_email_from_youtube_channel(channel_url)
            if email:
                logger.info(f"メール取得成功: {company_name} → {email}")
                # CRM に反映（別処理で実装）
                email_count += 1
            else:
                logger.debug(f"メール取得失敗: {company_name}")
        except Exception as e:
            logger.warning(f"メール抽出エラー [{company_name}]: {e}")
    
    logger.info(f"Step 3.5 完了: {email_count}件のメール取得")
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ 収集フロー完了")
    logger.info("=" * 60)

if __name__ == "__main__":
    logger.add("logs/collect.log", rotation="500 MB", retention="7 days")
    run_collect()



