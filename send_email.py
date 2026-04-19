import sys, time, random
from datetime import datetime
from loguru import logger
from email_generator import generate_email, EmailContent
from email_sender import XserverSMTPSender
from db_manager import init_send_log_db, log_send_event, get_todays_send_count, get_next_email_num
from config import DOMAIN_LAUNCH_DATE, WARMUP_SCHEDULE, ENABLE_AGGRESSIVE_MODE, AGGRESSIVE_BOUNCE_THRESHOLD, EMAIL_FIRST_SEND_RATIO, EMAIL_FOLLOWUP_SEND_RATIO
from crm_manager import get_pending_leads
import argparse
import uuid

logger.add('logs/send_email.log', rotation='500 MB')

def get_daily_limit():
    launch = datetime.fromisoformat(DOMAIN_LAUNCH_DATE)
    days_elapsed = (datetime.now() - launch).days
    week = min((days_elapsed // 7) + 1, 4)
    base_limit = WARMUP_SCHEDULE.get(week, 25)
    if week >= 4 and ENABLE_AGGRESSIVE_MODE:
        logger.info("🚀 Aggressive mode 有効：最大 30 件/日を許可")
        return 30
    return base_limit

def is_sending_allowed():
    current_hour = datetime.now().hour
    if current_hour >= 23:
        logger.warning(f'23:00以降のため送信をスキップします (現在時刻: {datetime.now().strftime("%H:%M:%S")})')
        return False
    return True

def wait_between_sends(email_count, total_count, base_wait=1200):
    if email_count < total_count:
        variance = random.uniform(0.5, 1.5)
        wait_time = int(base_wait * variance)
        logger.info(f'次のメール送信まで {wait_time} 秒（約 {wait_time // 60} 分）待機します...')
        logger.info(f'  (基本: {base_wait}秒、ランダムばらつき: ±50%)')
        for remaining in range(wait_time, 0, -1):
            if remaining % 300 == 0 or remaining <= 60:
                logger.info(f'  残り時間: {remaining} 秒（約 {remaining // 60} 分）')
            time.sleep(1)

def calculate_send_limits(daily_limit):
    """
    1回目と2回目以降の送信上限を計算
    - 1回目: 70%
    - 2回目以降: 30%
    """
    from config import EMAIL_FIRST_SEND_RATIO, EMAIL_FOLLOWUP_SEND_RATIO
    first_send_limit = int(daily_limit * EMAIL_FIRST_SEND_RATIO)
    followup_send_limit = daily_limit - first_send_limit
    logger.info(f'送信配分: 1回目 {first_send_limit}件 (70%), 2回目以降 {followup_send_limit}件 (30%)')
    return first_send_limit, followup_send_limit



def main():
    parser = argparse.ArgumentParser(description='メール送信スクリプト')
    parser.add_argument('--limit', type=int, default=None, help='送信上限件数（指定なしなら自動計算）')
    parser.add_argument('--dry-run', action='store_true', help='ドライラン（実際には送信しない）')
    parser.add_argument('--wait', type=int, default=1200, help='メール間隔（秒、デフォルト: 1200秒=20分）')
    args = parser.parse_args()

    init_send_log_db()

    if args.limit:
        daily_limit = args.limit
    else:
        daily_limit = get_daily_limit()

    # 配分比率に基づいて1回目と2回目以降の送信上限を計算
    first_send_limit, followup_send_limit = calculate_send_limits(daily_limit)
    
    logger.info(f'=== メール送信開始 (limit={daily_limit}, wait={args.wait}秒, dry_run={args.dry_run}) ===')
    logger.info(f'現在時刻: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    logger.info(f'本日の送信上限: {daily_limit} 件')
    logger.info(f'メール間隔: {args.wait} 秒（ランダムばらつき: ±50%）')

    if not args.dry_run and not is_sending_allowed():
        logger.warning('23:00以降のため送信を中止します')
        return

    leads = get_pending_leads()[:daily_limit]
    logger.info(f'対象リード: {len(leads)} 件')
    if not leads:
        logger.warning('メール対象リードなし')
        return

    sender = XserverSMTPSender()
    sent_count = 0
    total_leads = len(leads)

    processed_count = 0  # 実際に処理対象に選ばれた企業数
    for idx, lead in enumerate(leads, 1):
        try:
            if not args.dry_run and not is_sending_allowed():
                logger.warning(f'23:00に到達したため、残り {total_leads - idx + 1} 件の送信を中止します')
                break

            ch_name = lead[3] if isinstance(lead, tuple) else lead.get('チャンネル名', 'Unknown')
            email = lead[2] if isinstance(lead, tuple) else lead.get('メールアドレス')

            # メールアドレスがなければスキップ
            if not email or not email.strip():
                logger.warning(f"[SKIP] スキップ: メールアドレスなし ({ch_name})")
                continue
            logger.info(f"[CANDIDATE] 処理中: {ch_name} ({email})")

            # タプルを辞書に変換 (idx, website_url, email, company_name)
            if isinstance(lead, tuple):
                lead_dict = {
                    'チャンネル名': lead[3],
                    'メールアドレス': lead[2],
                    'サイトURL': lead[1],
                }
            else:
                lead_dict = lead
            
            # 次に送るべき通数を判定
            email_num = get_next_email_num(email)
            if email_num is None:
                logger.info(f'スキップ: 送信タイミングではない ({ch_name})')
                continue
            

            # スキップされなかった企業だけカウント
            processed_count += 1
            logger.info(f'[{processed_count}/{daily_limit}] {email_num} 通目を送信します: {ch_name}')
            email_content = generate_email(lead_dict, email_num=email_num)

            if args.dry_run:
                logger.info(f'[DRY-RUN] {ch_name} へメール送信スキップ')
                logger.debug(f'件名: {email_content.subject}')
            else:
                result = sender.send_email(
                    to=email,
                    subject=email_content.subject,
                    body=email_content.body,
                    from_name='営業自動化',
                    company_name='会社名',
                    email_count=sent_count + 1
                )
                if result.success:
                    message_id = f"msg_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"
                    logger.info(f'✅ {ch_name} へメール送信成功 (MessageID: {message_id})')
                    log_send_event(to_address=email, message_id=message_id, status='sent')
                    sent_count += 1
                else:
                    logger.error(f'❌ {ch_name} へメール送信失敗')

            if not args.dry_run:
                wait_between_sends(idx, total_leads, base_wait=args.wait)
            else:
                logger.info(f'[DRY-RUN] 待機をスキップ')

        except Exception as e:
            logger.error(f'例外発生: {e}')
            import traceback
            traceback.print_exc()

    logger.info(f'=== メール送信完了: {sent_count} 件 ===')
    logger.info(f'実行終了時刻: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

if __name__ == '__main__':
    main()






