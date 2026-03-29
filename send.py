#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
send.py
CRM からメール/フォーム送信対象のリードを取得して送信
"""
import os
import sys
from datetime import datetime
from pytz import timezone
from loguru import logger

# ローカルモジュール
from crm_manager import get_crm, get_pending_leads, update_email_status
from email_generator import generate_email
from email_sender import XserverSMTPSender
from form_submitter import submit_form_sync
import config

JST = timezone('Asia/Tokyo')

def run_send(dry_run=False):
    """
    メール/フォーム送信フロー
    
    Args:
        dry_run (bool): ドライランモード
    """
    logger.info("=" * 60)
    logger.info(f"送信フロー開始 (dry_run={dry_run})")
    logger.info("=" * 60)
    
    # Step 4: 送信対象リードを取得
    logger.info("\n=== Step 4: 送信対象リード取得 ===")
    crm = get_crm()
    pending_leads = get_pending_leads()
    logger.info(f"送信対象: {len(pending_leads)}件")
    
    if not pending_leads:
        logger.warning("送信対象なし。終了。")
        return
    
    # 初期化
    emails_sent = 0
    forms_sent = 0
    errors = []
    
    # 各リードに対して送信
    for lead in pending_leads:
        company_name = lead.get("会社名", "Unknown")
        email_address = lead.get("メールアドレス", "")
        form_url = lead.get("問い合わせフォームURL", "")
        channel_url = lead.get("YouTubeチャンネルURL", "")
        
        logger.info(f"\n処理中: {company_name}")
        
        try:
            # Step 5+6+7: メール生成・送信
            if email_address and "@" in email_address:
                logger.info(f"メール送信: {company_name} → {email_address}")
                
                email_content = generate_email(lead)
                
                if not dry_run:
                    sender = XserverSMTPSender()
                    result = sender.send(
                        to_email=email_address,
                        subject=email_content.subject,
                        body=email_content.body
                    )
                    if result:
                        logger.info(f"✅ メール送信成功: {company_name}")
                        emails_sent += 1
                        update_email_status(channel_url, 1, datetime.now(JST))
                    else:
                        logger.error(f"❌ メール送信失敗: {company_name}")
                        errors.append(f"メール送信失敗: {company_name}")
                else:
                    logger.info(f"[DRY-RUN] メール送信: {company_name}")
                    emails_sent += 1
            
            # フォームURLがあり、メールアドレスがない場合
            elif form_url:
                logger.info(f"フォーム送信: {company_name} → {form_url}")
                
                email_content = generate_email(lead)
                
                if not dry_run:
                    form_result = submit_form_sync(
                        form_url=form_url,
                        company_name=company_name,
                        sender_name=config.MY_NAME,
                        sender_email=config.SMTP_USER if hasattr(config, 'SMTP_USER') else os.getenv('SMTP_USER', ''),
                        sender_phone=config.MY_PHONE,
                        message_body=email_content.body
                    )
                    if form_result.success:
                        logger.info(f"✅ フォーム送信成功: {company_name}")
                        forms_sent += 1
                        update_email_status(channel_url, 1, datetime.now(JST))
                    else:
                        logger.error(f"❌ フォーム送信失敗: {company_name} - {form_result.error_message}")
                        errors.append(f"フォーム送信失敗: {company_name}")
                else:
                    logger.info(f"[DRY-RUN] フォーム送信: {company_name}")
                    forms_sent += 1
            
            else:
                logger.warning(f"⚠️ メール・フォーム両方なし: {company_name}")
                errors.append(f"送信方法なし: {company_name}")
        
        except Exception as e:
            logger.error(f"❌ 送信エラー [{company_name}]: {e}")
            errors.append(f"送信エラー: {company_name}")
    
    # サマリー出力
    logger.info("\n" + "=" * 60)
    logger.info("📊 送信フロー結果")
    logger.info("=" * 60)
    logger.info(f"メール送信: {emails_sent}件")
    logger.info(f"フォーム送信: {forms_sent}件")
    logger.info(f"エラー: {len(errors)}件")
    if errors:
        for err in errors:
            logger.info(f"  - {err}")
    logger.info("✅ 送信フロー完了")
    logger.info("=" * 60)

if __name__ == "__main__":
    logger.add("logs/send.log", rotation="500 MB", retention="7 days")
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="ドライランモード")
    args = parser.parse_args()
    
    run_send(dry_run=args.dry_run)


