with open('collect.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# for i, ch in enumerate(scored_channels): の直後にメール割り当てコードを挿入
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    # ループ開始行の直後（157 行目あたり）にメール割り当てを挿入
    if 'for i, ch in enumerate(scored_channels):' in line:
        new_lines.append('            # JSON からメール情報を割り当て\n')
        new_lines.append('            if ch.channel.channel_url in email_data_loop:\n')
        new_lines.append('                ch.channel.contact_email = email_data_loop[ch.channel.channel_url].get("email", "")\n')
        new_lines.append('                ch.channel.website_url = email_data_loop[ch.channel.channel_url].get("website", "")\n')
        new_lines.append('                ch.channel.contact_form_url = email_data_loop[ch.channel.channel_url].get("form_url", "")\n')
        new_lines.append('\n')

with open('collect.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ ループ内にメール割り当てコードを挿入しました')
