with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 137: extractor.extract_email → get_email_from_youtube_channel
for i in range(len(lines)):
    if 'extractor.extract_email' in lines[i]:
        lines[i] = lines[i].replace('extractor.extract_email', 'get_email_from_youtube_channel')

# website_url の割り当てを追加
for i in range(len(lines)):
    if 'ch.channel.contact_email = email if email else' in lines[i]:
        if i+1 < len(lines) and 'contact_form_url' in lines[i+1]:
            indent = '            '
            lines.insert(i+1, indent + 'ch.channel.website_url = website_url if website_url else \x27\x27\n')
        break

# JSON 保存コードを追加
for i in range(len(lines)):
    if 'Step 7 完了:' in lines[i]:
        insert_pos = i + 2
        json_code = '''
    # JSON にメール情報を保存
    os.makedirs("cache", exist_ok=True)
    email_data = {}
    for ch in scored_channels:
        if ch.channel.contact_email:
            email_data[ch.channel.channel_url] = {
                "email": ch.channel.contact_email,
                "website": ch.channel.website_url,
                "form_url": ch.channel.contact_form_url
            }
    with open("cache/email_data.json", "w", encoding="utf-8") as f:
        json.dump(email_data, f, ensure_ascii=False, indent=2)
    logger.info(f"✅ メール情報保存: {len(email_data)} 件 を JSON に保存")
'''
        lines.insert(insert_pos, json_code + '\n')
        break

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ 全て修正しました')
