with open('collect.py', 'r', encoding='utf-8') as f:
    content = f.read()

# デバッグログの ch.contact_email → ch.channel.contact_email に修正
content = content.replace(
    "f\"DEBUG Step 6ループ {i}: {ch.channel_name} - email before to_crm_dict: '{ch.contact_email}'\"",
    "f\"DEBUG Step 6ループ {i}: {ch.channel_name} - email before to_crm_dict: '{ch.channel.contact_email}'\""
)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ デバッグログの参照を修正しました')
