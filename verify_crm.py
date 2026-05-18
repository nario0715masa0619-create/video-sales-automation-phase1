from crm_manager import CRMManager
import config

def verify_increment(channel_url):
    crm = CRMManager()
    existing = crm.find_lead_by_channel_url(channel_url)
    if existing:
        row_num, lead = existing
        print(f"Lead status for {channel_url}:")
        print(f"  Channel Name: {lead.get('チャンネル名')}")
        print(f"  Email Sent Count (メール送信回数): {lead.get('メール送信回数')}")
        print(f"  Sales Status (営業ステータス): {lead.get('営業ステータス')}")
        print(f"  Last Sent Date (最終送信日): {lead.get('最終送信日')}")
    else:
        print(f"Lead not found: {channel_url}")

if __name__ == "__main__":
    target_url = "https://www.youtube.com/channel/UCdwCRA5nabkUAddDCn9rADQ"
    verify_increment(target_url)
