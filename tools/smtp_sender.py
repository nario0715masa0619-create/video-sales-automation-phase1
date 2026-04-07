"""
smtp_sender.py
==============
Xserver SMTPを使ってメールを送信するモジュール
"""

import smtplib
import os
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

JST = timezone(timedelta(hours=9))

def _write_email_log(company_name: str, to: str, count: int, subject: str, body: str) -> None:
    os.makedirs("logs", exist_ok=True)
    now_str = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    count_str = f"{count}通目" if count else "不明"
    company_str = company_name if company_name else "不明"
    
    log_content = f"""============================================================
[SEND] {now_str}
会社名: {company_str}
宛先: {to}
通数: {count_str}
件名: {subject}
本文:
{body}
"""
    with open("logs/email.log", "a", encoding="utf-8") as f:
        f.write(log_content)

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
MAIL_FROM = os.getenv("MAIL_FROM", SMTP_USER)


def send_email(to_address: str, subject: str, body: str, company_name: str = "", email_count: int = 0) -> bool:
    """
    SMTPでメールを送信する

    Args:
        to_address: 送信先メールアドレス
        subject: 件名
        body: 本文

    Returns:
        bool: 送信成功なら True
    """
    # 実際の送信処理の直前でログに保存
    _write_email_log(company_name, to_address, email_count, subject, body)

    try:
        msg = MIMEMultipart()
        msg["From"] = MAIL_FROM
        msg["To"] = to_address
        msg["Subject"] = Header(subject, "utf-8")

        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(MAIL_FROM, to_address, msg.as_string())

        logger.info(f"✅ 送信成功: {to_address}")
        return True

    except Exception as e:
        logger.error(f"❌ 送信失敗: {to_address} - {e}")
        return False


if __name__ == "__main__":
    # 接続テスト
    print("SMTPテスト送信を開始します...")
    result = send_email(
        to_address=SMTP_USER,
        subject="【テスト】SMTP接続確認",
        body="このメールはSMTP設定のテストです。\n正常に受信できていれば設定完了です。",
        company_name="テスト会社",
        email_count=1
    )
    if result:
        print("✅ テスト送信成功！")
    else:
        print("❌ 送信失敗。.envの設定を確認してください。")
