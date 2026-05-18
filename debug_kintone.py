from crm_manager import get_crm
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=9))
crm = get_crm()
all_leads = crm.get_all_leads()

kintone = [r for r in all_leads if 'kintone活用ちゃんねる' in r.get('チャンネル名', '')][0]

print(f"チャンネル名: {kintone.get('チャンネル名')}")
print(f"送信回数: {kintone.get('送信回数')}")
print(f"最終送信日: {kintone.get('最終送信日')}")
print(f"営業ステータス: {kintone.get('営業ステータス')}")

# _row_to_dict で何が読み込まれているか確認
print(f"\n辞書全体のキー: {list(kintone.keys())}")
