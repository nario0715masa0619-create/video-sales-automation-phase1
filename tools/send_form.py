import sys
from loguru import logger
from crm_manager import CRMManager
from form_submitter import submit_form_sync
import argparse

logger.add('logs/send_form.log', rotation='500 MB')

def main():
    parser = argparse.ArgumentParser(description='フォーム送信スクリプト')
    parser.add_argument('--limit', type=int, default=5, help='送信上限件数')
    parser.add_argument('--dry-run', action='store_true', help='ドライラン（実際には送信しない）')
    parser.add_argument('--test', action='store_true', help='テストモード（最初の 1 件のみ）')
    args = parser.parse_args()
    
    if args.test:
        args.limit = 1
    
    logger.info(f'=== フォーム送信開始 (limit={args.limit}, dry_run={args.dry_run}, test={args.test}) ===')
    
    # CRM からフォーム対象リードを取得
    crm = CRMManager()
    leads = crm.get_leads_for_form(args.limit)
    logger.info(f'対象リード: {len(leads)} 件')
    
    if not leads:
        logger.warning('フォーム対象リードなし')
        return
    
    # フォーム送信
    sent_count = 0
    
    for lead in leads:
        try:
            ch_name = lead.get('チャンネル名', 'Unknown')
            form_url = lead.get('問い合わせフォームURL')
            
            logger.info(f'処理中: {ch_name} ({form_url})')
            
            if args.dry_run:
                logger.info(f'[DRY-RUN] {ch_name} へフォーム送信スキップ')
            else:
                # フォーム送信
                result = submit_form_sync(
                    url=form_url,
                    channel_name=ch_name,
                    contact_email='contact@example.com'
                )
                
                if result.success:
                    logger.info(f'✅ {ch_name} へフォーム送信成功')
                    crm.update_after_form_send(lead, success=True)
                    sent_count += 1
                else:
                    logger.error(f'❌ {ch_name} へフォーム送信失敗: {result.error}')
                    crm.update_after_form_send(lead, success=False)
        
        except Exception as e:
            logger.error(f'例外発生 ({ch_name}): {e}')
            crm.update_after_form_send(lead, success=False)
    
    logger.info(f'=== フォーム送信完了: {sent_count} 件 ===')

if __name__ == '__main__':
    main()
