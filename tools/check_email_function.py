with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'get_email_from_youtube_channel' in content:
    print('✅ get_email_from_youtube_channel が定義されている')
else:
    print('❌ get_email_from_youtube_channel が見つかりません')
