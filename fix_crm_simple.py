with open('crm_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# upsert_lead メソッドの定義行直後に logger を追加
content = content.replace(
    '    def upsert_lead(self, lead_data: dict) -> None:\n        """\n        リードを新規追加または更新する（重複チェック込み）。',
    '    def upsert_lead(self, lead_data: dict) -> None:\n        logger.info(f"[upsert_lead] 開始: {lead_data.get(\'チャンネル名\', \'Unknown\')}")\n        """\n        リードを新規追加または更新する（重複チェック込み）。'
)

# 「既存レコードの更新」の logger の後に [upsert_lead] 完了を追加
content = content.replace(
    'logger.info(f"リード更新: {lead_data.get(\'チャンネル名\', channel_url)} (行{row_num}, {len(cell_list)}セル)")',
    'logger.info(f"リード更新: {lead_data.get(\'チャンネル名\', channel_url)} (行{row_num}, {len(cell_list)}セル)")\n                logger.info(f"[upsert_lead] 完了")'
)

content = content.replace(
    'logger.info(f"リード更新: {lead_data.get(\'チャンネル名\', channel_url)} (変更なし)")',
    'logger.info(f"リード更新: {lead_data.get(\'チャンネル名\', channel_url)} (変更なし)")\n                logger.info(f"[upsert_lead] 完了")'
)

with open('crm_manager.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ crm_manager.py にログを追加しました')
