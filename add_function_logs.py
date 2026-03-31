import re

# scorer.py を修正
with open('scorer.py', 'r', encoding='utf-8') as f:
    scorer_content = f.read()

# score_channels 関数の先頭にログを追加
scorer_content = re.sub(
    r'(def score_channels\(channels: list\) -> list:)',
    r'\1\n    logger.info(f"[score_channels] 開始: {len(channels)}件のチャンネルをスコアリング")',
    scorer_content
)

# score_channels 関数の return 前にログを追加
scorer_content = re.sub(
    r'(    return sorted_channels)',
    r'    logger.info(f"[score_channels] 完了: {len(sorted_channels)}件をスコアリング")\n\1',
    scorer_content
)

with open('scorer.py', 'w', encoding='utf-8') as f:
    f.write(scorer_content)

print('✅ scorer.py にログを追加しました')

# crm_manager.py を修正
with open('crm_manager.py', 'r', encoding='utf-8') as f:
    crm_content = f.read()

# upsert_lead 関数の先頭にログを追加
crm_content = re.sub(
    r'(def upsert_lead\(lead_data: dict\) -> None:)',
    r'\1\n    logger.info(f"[upsert_lead] 開始: {lead_data.get(\"チャンネル名\", \"Unknown\")}")',
    crm_content
)

# upsert_lead 関数の終わりにログを追加（最後の logger.info の後）
crm_content = re.sub(
    r'(logger\.info\(f"リード更新: .*?"\))',
    r'\1\n    logger.info(f"[upsert_lead] 完了")',
    crm_content
)

crm_content = re.sub(
    r'(logger\.info\(f"リード新規追加: .*?"\))',
    r'\1\n    logger.info(f"[upsert_lead] 完了")',
    crm_content
)

with open('crm_manager.py', 'w', encoding='utf-8') as f:
    f.write(crm_content)

print('✅ crm_manager.py にログを追加しました')
