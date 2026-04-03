with open('logs/collect.log', 'r', encoding='utf-8') as f:
    log_lines = f.readlines()

# 「リード更新」で始まる行を抽出
update_logs = [line for line in log_lines if 'リード更新' in line]

print(f'リード更新ログ行数: {len(update_logs)}')
print('\n最初の 10 行:')
for line in update_logs[:10]:
    print(line.rstrip())

print('\n最後の 10 行:')
for line in update_logs[-10:]:
    print(line.rstrip())
