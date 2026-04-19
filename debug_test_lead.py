from crm_manager import CRMManager
import config

crm = CRMManager()
all_leads = crm.get_all_leads()

# テスト企業を直接検索
test_lead = [l for l in all_leads if 'テスト用2通目' in str(l.get('チャンネル名', ''))]

if test_lead:
    lead = test_lead[0]
    print('✅ テスト企業が見つかりました:')
    rank = lead.get('ランク')
    target_ranks = config.EMAIL_TARGET_RANKS
    print(f'  ランク: {rank} (対象: {target_ranks})')
    print(f'  NGフラグ: {lead.get("NGフラグ")}')
    print(f'  バウンスフラグ: {lead.get("バウンスフラグ")}')
    print(f'  営業ステータス: {lead.get("営業ステータス")}')
    print(f'  メール送信回数: {lead.get("メール送信回数")}')
    print(f'  最終送信日: {lead.get("最終送信日")}')
else:
    print('❌ テスト企業が見つかりません')
