with open('crm_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 新しいメソッドを追加する
new_methods = '''
    def get_leads_for_email(self, limit=10):
        """メールアドレスを持つリード（A/B ランク、未送信）を取得"""
        leads = self.get_all_leads()
        email_leads = [
            lead for lead in leads
            if lead.get('メールアドレス') 
            and lead.get('ランク') in ['A', 'B']
            and lead.get('送信ステータス') != 'sent'
        ]
        return email_leads[:limit]

    def get_leads_for_form(self, limit=5):
        """問い合わせフォーム URL を持つリード（A/B ランク、未送信）を取得"""
        leads = self.get_all_leads()
        form_leads = [
            lead for lead in leads
            if lead.get('問い合わせフォームURL')
            and lead.get('ランク') in ['A', 'B']
            and lead.get('送信ステータス') != 'sent'
        ]
        return form_leads[:limit]

    def update_after_email_send(self, lead, success=True):
        """メール送信後に CRM を更新"""
        from datetime import datetime
        if success:
            lead['送信ステータス'] = 'sent'
            lead['最終送信日'] = datetime.now().isoformat()
        else:
            lead['送信ステータス'] = 'failed'
        self.upsert_lead(lead)

    def update_after_form_send(self, lead, success=True):
        """フォーム送信後に CRM を更新"""
        from datetime import datetime
        if success:
            lead['送信ステータス'] = 'sent'
            lead['最終送信日'] = datetime.now().isoformat()
        else:
            lead['送信ステータス'] = 'failed'
        self.upsert_lead(lead)
'''

# クラスの最後に追加（最後の def の後）
if 'def get_leads_for_email' not in content:
    # クラスの末尾を探して追加
    content = content.rstrip() + '\n' + new_methods + '\n'
    
    with open('crm_manager.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print('✅ CRMManager にヘルパーメソッドを追加しました')
else:
    print('ℹ️  既にヘルパーメソッドが存在します')
