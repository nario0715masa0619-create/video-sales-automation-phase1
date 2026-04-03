import re
with open('logs/collect.log', 'r', encoding='utf-8') as f:
    log_content = f.read()

# 最新実行（2026-03-31 12:）のログを抽出
latest_logs = [line for line in log_content.split('\n') if '2026-03-31 12:' in line]

new_adds = len([l for l in latest_logs if 'リード新規追加' in l])
updates = len([l for l in latest_logs if 'リード更新' in l])

print(f'最新実行（2026-03-31）:')
print(f'  リード新規追加: {new_adds}件')
print(f'  リード更新: {updates}件')
print(f'  合計処理: {new_adds + updates}件')
print(f'\nスプレッドシート保存: 120件')
print(f'未保存: {237 - (new_adds + updates)}件')
