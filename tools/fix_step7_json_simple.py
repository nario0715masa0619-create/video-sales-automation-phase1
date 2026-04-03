with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if "if ch.contact_email:" in line:
        new_lines.append(line.replace('ch.contact_email', 'ch.channel.contact_email'))
    elif "'email': ch.contact_email" in line:
        new_lines.append(line.replace('ch.contact_email', 'ch.channel.contact_email'))
    elif "'website': ch.website_url" in line:
        new_lines.append(line.replace('ch.website_url', 'ch.channel.website_url'))
    elif "'form_url': ch.contact_form_url" in line:
        new_lines.append(line.replace('ch.contact_form_url', 'ch.channel.contact_form_url'))
    elif 'email_data[ch.channel_url]' in line:
        new_lines.append(line.replace('ch.channel_url', 'ch.channel.channel_url'))
    else:
        new_lines.append(line)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ JSON 保存コードを修正しました')
