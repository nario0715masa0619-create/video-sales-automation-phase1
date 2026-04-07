with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ループ内で for i, ch in enumerate の直後にメール割り当てを追加
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if 'for i, ch in enumerate(scored_channels):' in line:
        new_lines.append('            # メール情報を割り当て\n')
        new_lines.append('            if ch.channel_url in email_data_loop:\n')
        new_lines.append('                ch.contact_email = email_data_loop[ch.channel_url].get(\'email\', \'\')\n')
        new_lines.append('                ch.website_url = email_data_loop[ch.channel_url].get(\'website\', \'\')\n')
        new_lines.append('                ch.contact_form_url = email_data_loop[ch.channel_url].get(\'form_url\', \'\')\n')
        new_lines.append('\n')

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ ループ内でメール割り当てを追加しました')
