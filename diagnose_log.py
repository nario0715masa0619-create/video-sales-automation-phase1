with open('logs/collect.log', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
print(f'総ログ行数: {len(lines)}')

# 最後の実行セッションの時刻を抽出
if lines:
    last_time = lines[-1].split('|')[0] if '|' in lines[-1] else 'Unknown'
    print(f'最後のログ時刻: {last_time}')

# キーワード検索
step3_count = len([l for l in lines if 'Step 3' in l or 'CRM 更新' in l])
email_count = len([l for l in lines if 'メール抽出' in l])
icp_count = len([l for l in lines if 'ICP' in l])

print(f'\nStep 3（CRM更新）関連: {step3_count}行')
print(f'メール抽出関連: {email_count}行')
print(f'ICP フィルタ関連: {icp_count}行')

# 最後の 30 行を表示
print('\n=== ログの最後 30 行 ===')
for line in lines[-30:]:
    if line.strip():
        print(line)
