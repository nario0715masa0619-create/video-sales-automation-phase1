with open('crm_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# update_after_email_send を修正
old_method = '''    def update_after_email_send(self, lead, success=True):
        """メール送信後に CRM を更新"""
        from datetime import datetime
        if success:
            lead['営業ステータス'] = '接触中'
            lead['メール送信回数'] = lead.get('メール送信回数', 0) + 1
            lead['1通目送信日'] = lead.get('1通目送信日') or datetime.now().strftime('%Y-%m-%d')
            lead['最終送信日'] = datetime.now().strftime('%Y-%m-%d')
        else:
            lead['営業ステータス'] = '未接触'
        self.upsert_lead(lead)'''

new_method = '''    def update_after_email_send(self, lead, success=True):
        """メール送信後に CRM を更新"""
        from datetime import datetime
        if success:
            lead['営業ステータス'] = '接触中'
            send_count = int(lead.get('メール送信回数', 0) or 0)
            lead['メール送信回数'] = send_count + 1
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            lead['1通目送信日'] = lead.get('1通目送信日') or now_str
            lead['最終送信日'] = now_str
        else:
            lead['営業ステータス'] = '未接触'
        self.upsert_lead(lead)'''

content = content.replace(old_method, new_method)

with open('crm_manager.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ update_after_email_send をタイムスタンプ形式に修正しました')
