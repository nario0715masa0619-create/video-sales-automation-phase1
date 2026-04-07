with open('collect.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 修正 1: extractor → get_email_from_youtube_channel
text = text.replace('extractor.extract_email(channel_url)', 'get_email_from_youtube_channel(channel_url)')

# 修正 2: website_url 割り当てを追加
old = "            ch.channel.contact_email = email if email else ''"
new = "            ch.channel.contact_email = email if email else ''
            ch.channel.website_url = website_url if website_url else ''"
text = text.replace(old, new)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('OK')
