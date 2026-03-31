import sys
from loguru import logger
from crm_manager import CRMManager
from email_generator import generate_email, EmailContent
from email_sender import XserverSMTPSender
import argparse

logger.add('logs/send_email.log', rotation='500 MB')

def main():
    parser = argparse.ArgumentParser(description='メール送信スクリプト')
    parser.add_argument('--limit', type=int, default=10, help='送信上限件数')
    parser.add_argument('--dry-run', action='store_true', help='ドライラン（実際には送信しない）')
    args = parser.parse_args()
    
    logger.info(f'=== メール送信開始 (limit={args.limit}, dry_run={args.dry_run}) ===')
    
    # CRM からメール対象リードを取得
    crm = CRMManager()
    leads = crm.get_leads_for_email(args.limit)
    logger.info(f'対象リード: {len(leads)} 件')
    
    if not leads:
        logger.warning('メール対象リードなし')
        return
    
    # メール送信
    sender = XserverSMTPSender()
    sent_count = 0
    
    for lead in leads:
        try:
            ch_name = lead.get('チャンネル名', 'Unknown')
            email = lead.get('メールアドレス')
            
            logger.info(f'処理中: {ch_name} ({email})')
            
            # メール本文生成（email_num=1 で固定）
            email_content = generate_email(lead, email_num=1)
            
            if args.dry_run:
                logger.info(f'[DRY-RUN] {ch_name} へメール送信スキップ')
                logger.debug(f'件名: {email_content.subject}')
            else:
                # メール送信
                result = sender.send_email(
                    to=email,
                    subject=email_content.subject,
                    body=email_content.body,
                    from_name='営業自動化',
                    company_name='会社名',
                    email_count=sent_count + 1
                )
                
                if result.success:
                    logger.info(f'✅ {ch_name} へメール送信成功')
                    crm.update_after_email_send(lead, success=True)
                    sent_count += 1
                else:
                    logger.error(f'❌ {ch_name} へメール送信失敗: {result.error}')
                    crm.update_after_email_send(lead, success=False)
        
        except Exception as e:
            logger.error(f'例外発生 ({ch_name}): {e}')
            crm.update_after_email_send(lead, success=False)
    
    logger.info(f'=== メール送信完了: {sent_count} 件 ===')

if __name__ == '__main__':
    main()
