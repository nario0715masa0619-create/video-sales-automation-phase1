with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Step 7 のメール割り当て部分を探して修正
new_lines = []
for i, line in enumerate(lines):
    if 'ch.contact_email = email if email else' in line:
        new_lines.append(line.replace('ch.contact_email', 'ch.channel.contact_email'))
    elif 'ch.website_url = website_url if website_url else' in line:
        new_lines.append(line.replace('ch.website_url', 'ch.channel.website_url'))
    elif 'ch.contact_form_url = contact_form_url if contact_form_url else' in line:
        new_lines.append(line.replace('ch.contact_form_url', 'ch.channel.contact_form_url'))
    else:
        new_lines.append(line)

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ Step 7 のメール割り当てを修正しました')
