import sys
sys.path.insert(0, '.')

from crm_manager import get_crm

# kintone のレコードを取得
crm = get_crm()
all_leads = crm.get_all_leads()

kintone = [r for r in all_leads if 'kintone活用ちゃんねる' in r.get('チャンネル名', '')][0]

# メール送信回数をセットしてテスト更新
kintone['メール送信回数'] = 1
kintone['最終送信日'] = '2026-05-18T14:43:00'
crm.upsert_lead(kintone)

# 更新後を確認
all_leads = crm.get_all_leads()
kintone_after = [r for r in all_leads if 'kintone活用ちゃんねる' in r.get('チャンネル名', '')][0]

print(f"メール送信回数（更新後）: {kintone_after.get('メール送信回数')}")
print(f"最終送信日（更新後）: {kintone_after.get('最終送信日')}")
