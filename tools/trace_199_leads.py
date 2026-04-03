with open('logs/collect.log', 'r', encoding='utf-8') as f:
    log_content = f.read()

# スコアリング完了のログを探す
import re
scoring_logs = re.findall(r'スコアリング完了.*?(\d+)件', log_content)
print('スコアリング完了ログ:')
for log in scoring_logs[-5:]:
    print(f'  {log}件')

# CRM 更新のログを探す
crm_logs = re.findall(r'CRM.*?(\d+)件', log_content)
print('\nCRM 更新ログ:')
for log in crm_logs[-5:]:
    print(f'  {log}件')

# チャンネル候補のログを探す
channel_logs = re.findall(r'チャンネル候補.*?(\d+)件', log_content)
print('\nチャンネル候補ログ:')
for log in channel_logs[-5:]:
    print(f'  {log}件')
