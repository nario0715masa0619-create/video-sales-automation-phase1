import sys
sys.path.insert(0, '.')

from crm_manager import get_crm

# 2026-05-17 送信済みメールアドレス
sent_emails = [
    'sample@xx.co.jp',
    'info@webst8.com',
    'membership@guga.or.jp',
    'lend_house-consulting@yahoo.co.jp',
    'info@umino-ai.com',
    'info@densanbanto.com',
    'l.labo.clubhouse@gmail.com',
    'tarou@sample.com',
    'info@enegaeru.com',
    'pmark@b-style.net',
    'xxx@xx.com',
    'consulting@s-bokan.com',
    'xxx123@mail.com',
    'info@acacia-web.com',
    'info@event-marketing.co.jp'
]

crm = get_crm()
all_leads = crm.get_all_leads()

updated_count = 0
for lead in all_leads:
    if lead.get('メールアドレス', '').strip() in sent_emails:
        lead['メール送信回数'] = 1
        lead['送信ステータス'] = 'sent'
        crm.upsert_lead(lead)
        updated_count += 1
        print(f"✅ {lead.get('チャンネル名')}: メール送信回数=1に更新")

print(f"\n合計 {updated_count} 件を更新しました")
