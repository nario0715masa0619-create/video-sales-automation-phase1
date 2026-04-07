with open('crm_manager.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 647-656 行を置き換え
new_lines = lines[:646] + [
    '    def get_leads_for_email(self, limit=10):\n',
    '        """メールアドレスを持つリード（A/B ランク、営業ステータス=未接触）を取得"""\n',
    '        leads = self.get_all_leads()\n',
    '        email_leads = [\n',
    '            lead for lead in leads\n',
    '            if lead.get(\'メールアドレス\')\n',
    '            and lead.get(\'ランク\') in [\'A\', \'B\']\n',
    '            and lead.get(\'営業ステータス\') == \'未接触\'\n',
    '        ]\n',
    '        return email_leads[:limit]\n',
    '\n',
] + lines[657:]

with open('crm_manager.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('✅ get_leads_for_email を営業ステータスベースに修正しました')
