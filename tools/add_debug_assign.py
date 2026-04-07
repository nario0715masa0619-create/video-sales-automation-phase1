with open("collect.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Line 178 の後にデバッグログを追加
for i, line in enumerate(lines):
    if 'ch.channel.contact_form_url = email_data_loop[ch.channel.channel_url].get("form_url", "")' in line:
        insert_pos = i + 1
        debug_log = '                logger.debug(f"DEBUG割り当て後: {ch.channel.channel_name} → website={ch.channel.website_url}")\n'
        lines.insert(insert_pos, debug_log)
        break

with open("collect.py", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("OK")
