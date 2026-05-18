from crm_manager import CRMManager
import config

def check_pending():
    crm = CRMManager()
    leads = crm.get_pending_leads()
    print(f"Total pending leads: {len(leads)}")
    if leads:
        lead = leads[0]
        print("First pending lead:")
        print(f"  Channel Name: {lead.get('チャンネル名')}")
        print(f"  Channel URL: {lead.get('チャンネルURL')}")
        print(f"  Email: {lead.get('メールアドレス')}")
        print(f"  Sent Count: {lead.get('メール送信回数')}")
        print(f"  Rank: {lead.get('ランク')}")

if __name__ == "__main__":
    check_pending()
