import re

with open('logs/collect.log', 'r', encoding='utf-8') as f:
    log_content = f.read()

# リード新規追加と更新のログを数える
new_adds = len(re.findall(r'リード新規追加', log_content))
updates = len(re.findall(r'リード更新', log_content))
skips = len(re.findall(r'チャンネルURLが未設定', log_content))

print(f'リード新規追加: {new_adds}件')
print(f'リード更新: {updates}件')
print(f'スキップ: {skips}件')
print(f'合計: {new_adds + updates}件')

# 最後の 20 行を表示（どこで終わったか確認）
print('\n--- collect.log の最後 30 行 ---')
lines = log_content.split('\n')
for line in lines[-30:]:
    if line.strip():
        print(line)
