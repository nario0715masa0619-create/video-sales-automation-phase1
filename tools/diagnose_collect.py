import re
from collections import Counter

print('=== 収集フロー診断レポート ===\n')

with open('logs/collect.log', 'r', encoding='utf-8') as f:
    log_content = f.read()
    lines = log_content.split('\n')

# Step 1: 候補数
if 'チャンネル候補:' in log_content:
    match = re.search(r'チャンネル候補: (\d+)件', log_content)
    if match:
        print(f'✅ Step 1 候補: {match.group(1)} 件')

# Step 1 → ICP フィルタ
icp_before = re.search(r'ICP フィルタリング前: (\d+)件', log_content)
icp_after = re.search(r'ICP フィルタリング後: (\d+)件', log_content)
if icp_before and icp_after:
    before = icp_before.group(1)
    after = icp_after.group(1)
    print(f'✅ ICP フィルタ: {before} → {after} 件')

# Step 2: スコアリング
scoring = re.search(r'スコアリング完了: Aランク (\d+)件 / Bランク (\d+)件 / Cランク (\d+)件', log_content)
if scoring:
    print(f'✅ Step 2 スコアリング: A={scoring.group(1)}, B={scoring.group(2)}, C={scoring.group(3)}')

# Step 3: CRM 更新
crm_update = re.search(r'CRM 更新: (\d+)件', log_content)
if crm_update:
    print(f'✅ Step 3 CRM 更新: {crm_update.group(1)} 件')

# リード新規追加数
new_leads = len(re.findall(r'リード新規追加:', log_content))
print(f'✅ 新規追加: {new_leads} 件')

# スコアリング時の重複チェック
scored_channels = []
for line in lines:
    if 'calculate_score' in line and 'DEBUG' in line:
        match = re.search(r'(\w+.*?): ', line.split(' - ')[-1] if ' - ' in line else '')
        if match:
            ch_name = line.split(' - ')[-1].split(':')[0].strip()
            scored_channels.append(ch_name)

if scored_channels:
    unique = len(set(scored_channels))
    duplicates = len(scored_channels) - unique
    print(f'\n⚠️  スコアリング時の重複:')
    print(f'   処理: {len(scored_channels)} 件, ユニーク: {unique} 件')
    if duplicates > 0:
        counts = Counter(scored_channels)
        dup_list = [(ch, counts[ch]) for ch in counts if counts[ch] > 1]
        dup_list.sort(key=lambda x: x[1], reverse=True)
        print(f'   重複: {duplicates} 件')
        print(f'   最多重複: {dup_list[0][0]} ({dup_list[0][1]} 回)')

print('\n=== 推奨アクション ===')
if duplicates > 0:
    print('❌ URL 重複排除ロジックが機能していません')
else:
    print('✅ 重複排除が正常に機能しています')
