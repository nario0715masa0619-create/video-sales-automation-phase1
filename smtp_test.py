import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASSWORD')
TO = 'nari.o.0715.masa.0619@gmail.com'

print(f"送信先: {TO}")
print(f"SMTPサーバー: {SMTP_HOST}:{SMTP_PORT}")
print(f"送信元: {SMTP_USER}")

msg = MIMEText('テスト送信です', 'plain', 'utf-8')
msg['Subject'] = 'SMTPテスト from luvira.co.jp'
msg['From'] = SMTP_USER
msg['To'] = TO

with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
    s.starttls()
    s.login(SMTP_USER, SMTP_PASS)
    s.sendmail(SMTP_USER, [TO], msg.as_string())
    print('✅ 送信完了！Gmailを確認してください')






















