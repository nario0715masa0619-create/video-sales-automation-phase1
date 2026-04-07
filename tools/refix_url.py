from crm_manager import CRMManager
import time

crm = CRMManager()
leads = crm.get_all_leads()

# 問題のURLを持つリードを直接修正
for lead in leads:
    channel_name = lead.get('チャンネル名', '')
    if '中小企業活力向上アドバンス オンラインセミナー' in channel_name:
        print(f'ターゲット発見: {channel_name}')
        original_url = lead.get('問い合わせフォームURL', '')
        print(f'  修正前: {repr(original_url)}')
        
        # 括弧を除去
        fixed_url = original_url.replace('）', '').replace(')', '')
        print(f'  修正後: {repr(fixed_url)}')
        
        lead['問い合わせフォームURL'] = fixed_url
        crm.upsert_lead(lead)
        time.sleep(3)
        print(f'  ✅ 更新完了')

print('\n再確認中...')
time.sleep(3)
leads = crm.get_all_leads()
for lead in leads:
    if '中小企業活力向上アドバンス オンラインセミナー' in lead.get('チャンネル名', ''):
        url = lead.get('問い合わせフォームURL', '')
        print(f'確認: {url}')
        if '）' in url or ')' in url:
            print('❌ まだゴミ文字が残っている')
        else:
            print('✅ クリア！')
