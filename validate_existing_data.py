"""
validate_existing_data.py
既存 DB 内のメールアドレスを検証
1. メール形式チェック → 2. ZeroBounce API 検証 → 3. 無効なものは削除
"""
import sqlite3
import requests
import time
import logging
from datetime import datetime
import config
import re

logging.basicConfig(
    filename='logs/validate_existing_data.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger()

ZEROBOUNCE_API_URL = 'https://api.zerobounce.net/v2/validate'
API_KEY = config.ZEROBOUNCE_API_KEY

def is_valid_email_format(email_str):
    """メールアドレスの事前チェック（形式・除外ルール）"""
    if not email_str or email_str == 'None':
        return False, 'empty'

    # 基本的なメールアドレス正規表現
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email_str):
        return False, 'invalid_format'

    domain = email_str.split('@')[1].lower()
    local_part = email_str.split('@')[0].lower()

    # 連続する同じ文字を除外
    if re.search(r'(.)\1{1,}', local_part):
        return False, 'continuous_chars_local'

    domain_name = domain.split('.')[0]
    if re.search(r'(.)\1{1,}', domain_name):
        return False, 'continuous_chars_domain'

    # localhost を除外
    if 'localhost' in domain:
        return False, 'localhost'

    # テスト用ドメインを除外
    invalid_domains = ['example.com', 'test.com', 'sample.com', 'invalid.com', 'example.org', 'example.net']
    if domain in invalid_domains:
        return False, 'test_domain'

    # よくある誤字ドメインを除外
    common_typos = {'gmial.com': 'gmail.com', 'gmai.com': 'gmail.com', 'yahooo.com': 'yahoo.com', 'hotmial.com': 'hotmail.com'}
    if domain in common_typos:
        return False, 'typo_domain'

    # サンプルメールを除外
    sample_keywords = ['sample', 'example', 'test', 'demo', 'dummy']
    if any(keyword in local_part for keyword in sample_keywords):
        return False, 'sample_keyword'

    return True, 'format_ok'

logger.info('=' * 80)
logger.info('🚀 既存メールアドレス検証開始')
logger.info('=' * 80)

# DB から全メールを取得
conn = sqlite3.connect('logs/phase5_data.db')
c = conn.cursor()
c.execute('SELECT id, email, company_name FROM phase5_data WHERE email IS NOT NULL AND email != "None"')
rows = c.fetchall()
logger.info(f'検証対象: {len(rows)} 件')
print(f'検証対象: {len(rows)} 件\n')

if not rows:
    print('✅ 検証対象メールがありません')
    conn.close()
    exit(0)

valid_count = 0
deleted_count = 0
rejected_by_format = {}  # 形式で弾かれた理由別カウント
rejected_by_api = {}     # API で弾かれた理由別カウント
start_time = time.time()

for idx, (row_id, email, company_name) in enumerate(rows, 1):
    try:
        # 1. メール形式チェック
        is_valid, reason = is_valid_email_format(email)
        
        if not is_valid:
            # 形式で弾かれた
            logger.warning(f'❌【形式チェック弾き/{reason}】({idx}/{len(rows)}): {email}')
            rejected_by_format[reason] = rejected_by_format.get(reason, 0) + 1
            
            # DB から削除
            c.execute('DELETE FROM phase5_data WHERE id = ?', (row_id,))
            conn.commit()
            deleted_count += 1
            logger.info(f'   → DB から削除: {company_name}')
            continue

        # 2. ZeroBounce API チェック
        params = {'api_key': API_KEY, 'email': email, 'ip_address': ''}
        resp = requests.get(ZEROBOUNCE_API_URL, params=params, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            status = data.get('status', 'unknown')
            sub_status = data.get('sub_status', '')
            
            if status == 'valid':
                valid_count += 1
                logger.info(f'✅【API 合格/valid】({idx}/{len(rows)}): {email}')
            else:
                # API で弾かれた
                api_reason = f'{status}/{sub_status}' if sub_status else status
                logger.warning(f'❌【API チェック弾き/{api_reason}】({idx}/{len(rows)}): {email}')
                rejected_by_api[api_reason] = rejected_by_api.get(api_reason, 0) + 1
                
                # DB から削除
                c.execute('DELETE FROM phase5_data WHERE id = ?', (row_id,))
                conn.commit()
                deleted_count += 1
                logger.info(f'   → DB から削除: {company_name}')
        else:
            logger.error(f'❌【API エラー/{resp.status_code}】({idx}/{len(rows)}): {email}')
            rejected_by_api[f'api_error_{resp.status_code}'] = rejected_by_api.get(f'api_error_{resp.status_code}', 0) + 1

        # 進捗表示（100 件ごと）
        if idx % 100 == 0:
            elapsed = time.time() - start_time
            remaining = len(rows) - idx
            msg = f'進捗: {idx}/{len(rows)} ({int(100*idx/len(rows))}%) - 有効: {valid_count} / 削除: {deleted_count}'
            logger.info(msg)
            print(msg)

        time.sleep(0.5)

    except Exception as e:
        logger.error(f'❌【例外】(ID {row_id}, {email[:30]}): {str(e)[:100]}')
        rejected_by_api['exception'] = rejected_by_api.get('exception', 0) + 1

elapsed = time.time() - start_time

# 最終結果
logger.info('=' * 80)
logger.info(f'✅ 検証完了')
logger.info(f'   有効メール: {valid_count} 件')
logger.info(f'   削除対象: {deleted_count} 件')
logger.info(f'   経過時間: {int(elapsed//60)} 分 {int(elapsed%60)} 秒')
logger.info('')
logger.info('【形式チェックで除外】')
for reason, count in sorted(rejected_by_format.items(), key=lambda x: x[1], reverse=True):
    logger.info(f'   {reason}: {count} 件')
logger.info('')
logger.info('【API チェックで除外】')
for reason, count in sorted(rejected_by_api.items(), key=lambda x: x[1], reverse=True):
    logger.info(f'   {reason}: {count} 件')
logger.info('=' * 80)

print(f'\n✅ 検証完了')
print(f'   有効メール: {valid_count} 件')
print(f'   削除対象: {deleted_count} 件')
print(f'   経過時間: {int(elapsed//60)} 分 {int(elapsed%60)} 秒')
print(f'\n【形式チェックで除外】')
for reason, count in sorted(rejected_by_format.items(), key=lambda x: x[1], reverse=True):
    print(f'   {reason}: {count} 件')
print(f'\n【API チェックで除外】')
for reason, count in sorted(rejected_by_api.items(), key=lambda x: x[1], reverse=True):
    print(f'   {reason}: {count} 件')

conn.close()
