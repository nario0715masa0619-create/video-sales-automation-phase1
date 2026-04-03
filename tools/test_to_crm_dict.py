from target_scraper import ChannelData

# テスト用 ChannelData を作成
ch = ChannelData(
    channel_id="test",
    channel_url="https://www.youtube.com/channel/test",
    channel_name="Test Channel",
    description="Test",
    subscriber_count=0,
    view_count=0,
    video_count=0
)

# website_url を動的に割り当て
ch.website_url = "https://example.com"
ch.contact_email = "test@example.com"
ch.contact_form_url = "https://example.com/contact"

# to_crm_dict() を呼び出す
result = ch.to_crm_dict()

print("=== to_crm_dict() の結果 ===")
for key, value in result.items():
    print(f"{key}: {value}")
