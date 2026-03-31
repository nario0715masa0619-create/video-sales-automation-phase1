import re

with open('logs/collect.log', 'r', encoding='utf-8') as f:
    log_content = f.read()

# 最新の実行（2026-03-30 22:）のログだけを抽出
latest_logs = [line for line in log_content.split('\n') if '2026-03-30 22:' in line or '2026-03-30 23:' in line]

# リード新規追加と更新を数える
new_adds = len([l for l in latest_logs if 'リード新規追加' in l])
updates = len([l for l in latest_logs if 'リード更新' in l])

print(f'最新実行のログ行数: {len(latest_logs)}')
print(f'リード新規追加: {new_adds}件')
print(f'リード更新: {updates}件')
print(f'合計: {new_adds + updates}件')
