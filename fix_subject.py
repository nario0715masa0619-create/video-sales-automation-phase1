with open('email_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# subject の生成を修正
old_subject = '''    subject = (
    f"{lead.get('会社名', '御社')}様の"
    f"「{subject_title[:20]}」を拝見しました"
    )'''

new_subject = '''    company_name = (lead.get('会社名') or lead.get('チャンネル名') or '御社').strip()
    subject = (
        f"{company_name}様の"
        f"「{subject_title[:20]}」を拝見しました"
    )'''

content = content.replace(old_subject, new_subject)

with open('email_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ subject を修正しました（会社名またはチャンネル名を使用）')
