with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# pickle 保存の代わりに JSON で保存
old_code = '''    import pickle
    os.makedirs("cache", exist_ok=True)
    with open("cache/scored_channels.pkl", "wb") as f:
        pickle.dump(scored_channels, f)
    logger.info("✅ キャッシュ保存: scored_channels")'''

new_code = '''    # メール情報を JSON に保存
    import json
    os.makedirs("cache", exist_ok=True)
    email_data = {}
    for ch in scored_channels:
        if ch.contact_email:  # メール取得済みのみ保存
            email_data[ch.channel_url] = {
                'email': ch.contact_email,
                'website': ch.website_url,
                'form_url': ch.contact_form_url
            }
    
    with open("cache/email_data.json", "w", encoding="utf-8") as f:
        json.dump(email_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✅ メール情報保存: {len(email_data)} 件 を JSON に保存")'''

content = content.replace(old_code, new_code)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ メール情報を JSON で保存するようにしました')
