with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# クラス外の不正なメソッド定義を削除
new_lines = []
skip_until_next_def = False
for i, line in enumerate(lines):
    # 行 721 以降のテスト関数内のメソッド定義をスキップ
    if i >= 720 and line.strip().startswith('def get_leads_for_email'):
        skip_until_next_def = True
        continue
    if i >= 720 and line.strip().startswith('def get_leads_for_form'):
        skip_until_next_def = True
        continue
    if i >= 720 and line.strip().startswith('def update_after_email_send'):
        skip_until_next_def = True
        continue
    if i >= 720 and line.strip().startswith('def update_after_form_send'):
        skip_until_next_def = True
        continue
    
    # スキップ中で新しいデフが出たら終了
    if skip_until_next_def and line.startswith('def ') and not line.startswith('    '):
        skip_until_next_def = False
    
    if not skip_until_next_def:
        new_lines.append(line)

# CRMManager クラスの末尾（行 753 付近）を探して、メソッドを追加
final_lines = []
inserted = False

for i, line in enumerate(new_lines):
    final_lines.append(line)
    
    # 最後のメソッドの終了を探す
    if not inserted and i < len(new_lines) - 50:
        # update_ng_list メソッドの終了を探す
        if i > 740 and 'def update_ng_list' in new_lines[i] if i < len(new_lines) else False:
            # メソッドの終了まで続ける
            j = i + 1
            while j < len(new_lines) and (new_lines[j].startswith('        ') or new_lines[j].strip() == ''):
                final_lines.append(new_lines[j])
                j += 1
            
            # ここにメソッドを追加
            methods = '''
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
            final_lines.append(methods)
            inserted = True
            
            # 残りの行をスキップして追加
            for k in range(j, len(new_lines)):
                final_lines.append(new_lines[k])
            break

# ファイルに書き込み
with open('crm_manager.py', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print('✅ メソッドを CRMManager クラス内に正しく追加しました')
