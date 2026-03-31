with open('logs/collect.log', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 最新の実行（2026-03-30）のログだけを抽出
latest_logs = [line for line in lines if '2026-03-30 19:' in line]

print(f'最新実行のログ行数: {len(latest_logs)}')
print('\n=== Step 別のログを追跡 ===')

# 各ステップのログを数える
step1 = len([l for l in latest_logs if 'Step 1' in l or 'チャンネル候補' in l])
step2 = len([l for l in latest_logs if 'Step 2' in l or 'スコアリング' in l])
step3 = len([l for l in latest_logs if 'Step 3' in l or 'CRM 更新' in l])

print(f'Step 1 (スクレイピング) ログ: {step1}行')
print(f'Step 2+3 (スコアリング・CRM) ログ: {step2}行')

# フィルタリング・除外されたログを探す
filtered = len([l for l in latest_logs if 'フィルタ' in l or '除外' in l or 'rejected' in l.lower()])
print(f'フィルタリング・除外ログ: {filtered}行')

# ICP フィルタリングの結果を探す
icp_logs = [l for l in latest_logs if 'filter_by_icp' in l or 'ICP' in l]
print(f'\nICP フィルタリング関連ログ: {len(icp_logs)}行')
for log in icp_logs[:10]:
    print(f'  {log.rstrip()}')
