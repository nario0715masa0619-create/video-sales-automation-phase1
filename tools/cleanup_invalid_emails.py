from crm_manager import CRMManager
from email_extractor import is_valid_email

crm = CRMManager()
all_leads = crm.get_all_leads()

print(f'=== CRM 無効メール クリーンアップ開始 ===')

invalid_leads = []
for lead in all_leads:
    email = lead.get('メールアドレス', '')
    if email and email.strip():
        if not is_valid_email(email):
            ch_name = lead.get('チャンネル名', 'Unknown')
            invalid_leads.append((ch_name, email))

print(f'クリア対象: {len(invalid_leads)}件\n')

# 1件ずつ upsert_lead で更新
for ch_name, old_email in invalid_leads:
    try:
        # 同じリードをメールアドレスなしで再登録
        lead_dict = {
            'チャンネル名': ch_name,
            'メールアドレス': '',  # クリア
        }
        crm.upsert_lead(lead_dict)
        print(f'✅ {ch_name}: メールアドレスをクリア')
    except Exception as e:
        print(f'❌ {ch_name}: エラー - {e}')

print(f'\n🎉 クリーンアップ完了: {len(invalid_leads)}件処理')
