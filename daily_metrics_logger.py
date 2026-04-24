#!/usr/bin/env python3
"""
Daily Metrics Logger for Cold Email Campaign
Records: date, raw count, valid count, sent count, reply count, deal count, memo
Appends to Google Sheet "Daily Log"
"""

import sqlite3
import json
import logging
from datetime import datetime
import os
import sys
from pathlib import Path

# ===== Configuration =====
DB_PATH = "logs/phase5_data.db"
SEND_LOG_PATH = "logs/send_email.log"
CRM_LOG_PATH = "logs/crm_manager.log"
DAILY_LOG_SHEET = "日次ログシート"

# ===== Logging =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# ===== Functions =====

def get_today_date():
    """Return today's date as YYYY-MM-DD"""
    return datetime.now().strftime('%Y-%m-%d')

def get_raw_count_today():
    """Count new addresses scraped today (all status)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        today = get_today_date()
        cur.execute("""
            SELECT COUNT(*) FROM phase5_data 
            WHERE DATE(scraped_at) = ?
        """, (today,))
        count = cur.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        logger.warning(f"Failed to get raw count: {e}")
        return 0

def get_valid_count_today():
    """Count addresses with ready_to_contact status today"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        today = get_today_date()
        cur.execute("""
            SELECT COUNT(*) FROM phase5_data 
            WHERE DATE(scraped_at) = ? AND status = 'ready_to_contact'
        """, (today,))
        count = cur.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        logger.warning(f"Failed to get valid count: {e}")
        return 0

def get_sent_count_today():
    """Count emails sent today from send_email.log"""
    try:
        if not os.path.exists(SEND_LOG_PATH):
            return 0
        
        sent_count = 0
        today = get_today_date()
        with open(SEND_LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if today in line and "sent to" in line.lower():
                    sent_count += 1
        return sent_count
    except Exception as e:
        logger.warning(f"Failed to get sent count: {e}")
        return 0

def get_reply_count_today():
    """Count replies received today from send_email.log"""
    try:
        if not os.path.exists(SEND_LOG_PATH):
            return 0
        
        reply_count = 0
        today = get_today_date()
        with open(SEND_LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if today in line and ("reply" in line.lower() or "responded" in line.lower()):
                    reply_count += 1
        return reply_count
    except Exception as e:
        logger.warning(f"Failed to get reply count: {e}")
        return 0

def get_deal_count_today():
    """Count deals created today from crm_manager.log"""
    try:
        if not os.path.exists(CRM_LOG_PATH):
            return 0
        
        deal_count = 0
        today = get_today_date()
        with open(CRM_LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if today in line and ("deal" in line.lower() or "商談" in line):
                    deal_count += 1
        return deal_count
    except Exception as e:
        logger.warning(f"Failed to get deal count: {e}")
        return 0

def log_daily_metrics(raw_count, valid_count, sent_count, reply_count, deal_count, memo=""):
    """Log daily metrics"""
    today = get_today_date()
    
    log_entry = {
        "date": today,
        "raw_count": raw_count,
        "valid_count": valid_count,
        "sent_count": sent_count,
        "reply_count": reply_count,
        "deal_count": deal_count,
        "memo": memo,
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"📊 Daily Metrics for {today}")
    logger.info(f"  Raw: {raw_count} | Valid: {valid_count} | Sent: {sent_count} | Replies: {reply_count} | Deals: {deal_count}")
    if memo:
        logger.info(f"  Memo: {memo}")
    
    return log_entry

def save_daily_log_local(log_entry):
    """Save to logs/daily_metrics.jsonl"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    json_path = log_dir / "daily_metrics.jsonl"
    
    try:
        with open(json_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        logger.info(f"✅ Saved to {json_path}")
    except Exception as e:
        logger.error(f"Failed to save: {e}")

def append_to_google_sheet(log_entry):
    """Print entry ready for Google Sheet append"""
    logger.info(f"📋 Ready for Google Sheet '{DAILY_LOG_SHEET}':")
    logger.info(f"  {log_entry['date']} | {log_entry['raw_count']} | {log_entry['valid_count']} | {log_entry['sent_count']} | {log_entry['reply_count']} | {log_entry['deal_count']} | {log_entry['memo']}")

def main():
    """Main entry point"""
    logger.info("🚀 Daily Metrics Logger started")
    
    memo = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    
    raw_count = get_raw_count_today()
    valid_count = get_valid_count_today()
    sent_count = get_sent_count_today()
    reply_count = get_reply_count_today()
    deal_count = get_deal_count_today()
    
    log_entry = log_daily_metrics(raw_count, valid_count, sent_count, reply_count, deal_count, memo)
    save_daily_log_local(log_entry)
    append_to_google_sheet(log_entry)
    
    logger.info("✅ Done")

if __name__ == "__main__":
    main()
