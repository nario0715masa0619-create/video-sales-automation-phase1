import imaplib
import email
import sqlite3
from datetime import datetime, timedelta
from loguru import logger
import os
from pathlib import Path
from dotenv import load_dotenv

# .env ファイルを読み込み
load_dotenv()

logger.add('logs/bounce_checker.log', rotation='500 MB')

DB_PATH = Path("logs/send_log.db")

def check_bounces():
    """IMAP でバウンスメールを集計"""
    logger.info("=== バウンスチェック開始 ===")
    
    # 環境変数から直接読み込み
    IMAP_HOST = os.getenv("IMAP_HOST", "sv16675.xserver.jp")
    IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
    IMAP_USER = os.getenv("IMAP_USER", "marketing@luvira-biz.jp")
    IMAP_PASSWORD = os.getenv("IMAP_PASSWORD")
    
    logger.info(f"接続情報: {IMAP_HOST}:{IMAP_PORT} / {IMAP_USER}")
    
    try:
        if not IMAP_PASSWORD:
            raise ValueError("IMAP_PASSWORD が設定されていません")
        
        imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
        imap.login(IMAP_USER, IMAP_PASSWORD)
        logger.info("✅ IMAP ログイン成功")
        
        # 本日受信したメール（未処理のみ）を検索
        imap.select("INBOX")
        today = datetime.now().strftime("%d-%b-%Y")
        status, messages = imap.search(None, f'SINCE "{today}" UNFLAGGED')
        
        bounce_count = 0
        processed_from = []
        
        if messages[0]:
            msg_ids = messages[0].split()
            logger.info(f"本日受信メール数: {len(msg_ids)} 件")
            
            for msg_id in msg_ids:
                try:
                    status, msg_data = imap.fetch(msg_id, "(RFC822)")
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    from_addr = msg.get("From", "")
                    subject = msg.get("Subject", "")
                    status_header = msg.get("Status", "")
                    
                    # バウンス判定条件
                    is_bounce = (
                        "Mail Delivery Subsystem" in from_addr or
                        "Mailer-Daemon" in from_addr or
                        any(x in subject for x in ["Mail delivery failed", "Undelivered Mail", "Returned mail", "Delivery Status Notification"]) or
                        "5." in status_header
                    )
                    
                    if is_bounce:
                        bounce_count += 1
                        processed_from.append(from_addr)
                        logger.info(f"🔴 バウンス検出: {subject}")
                        
                        # フラグを付ける（\\Flagged）
                        imap.store(msg_id, "+FLAGS", "\\Flagged")
                        logger.info(f"✅ フラグ付け完了: {msg_id}")
                
                except Exception as e:
                    logger.error(f"メール処理エラー ({msg_id}): {e}")
        
        imap.close()
        imap.logout()
        logger.info("✅ IMAP ログアウト")
        
        # 本日の送信件数を DB から集計
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        c.execute("""
        SELECT COUNT(*) FROM send_log
        WHERE date(datetime) = ? AND status = 'sent'
        """, (today_str,))
        
        send_count = c.fetchone()[0]
        
        # バウンスログを記録
        bounce_rate = (bounce_count / send_count * 100) if send_count > 0 else 0.0
        
        c.execute("""
        INSERT OR REPLACE INTO bounce_log (date, sent_count, bounce_count, bounce_rate)
        VALUES (?, ?, ?, ?)
        """, (today_str, send_count, bounce_count, bounce_rate))
        
        conn.commit()
        conn.close()
        
        logger.info(f"=== バウンス集計完了 ===")
        logger.info(f"本日送信数: {send_count} 件")
        logger.info(f"本日バウンス数: {bounce_count} 件")
        logger.info(f"バウンス率: {bounce_rate:.2f}%")
        
    except Exception as e:
        logger.error(f"IMAP接続エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_bounces()
