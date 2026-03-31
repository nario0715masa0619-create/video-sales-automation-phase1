with open('crm_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# upsert_lead 関数の定義行の直後に1行だけ追加
content = content.replace(
    'def upsert_lead(lead_data: dict) -> None:',
    'def upsert_lead(lead_data: dict) -> None:\n    logger.info(f"[upsert_lead] 開始: {lead_data.get(\'チャンネル名\', \'Unknown\')}")'
)

# logger.info(f"リード更新: が出現する直前に [upsert_lead] 完了を追加
content = content.replace(
    '        logger.info(f"リード更新:',
    '        logger.info(f"[upsert_lead] 完了")\n        logger.info(f"リード更新:'
)

content = content.replace(
    '        logger.info(f"リード新規追加:',
    '        logger.info(f"[upsert_lead] 完了")\n        logger.info(f"リード新規追加:'
)

with open('crm_manager.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ crm_manager.py を修復してログを追加しました')
