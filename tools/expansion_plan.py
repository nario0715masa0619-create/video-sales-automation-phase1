quota_per_keyword = 250
daily_quota = 60000

print(f'1キーワード当たり: {quota_per_keyword} pt')
print(f'総日次クォータ: {daily_quota} pt\n')

# 何キーワード実行可能か？
max_keywords = daily_quota // quota_per_keyword
print(f'実行可能な最大キーワード: {max_keywords} 個\n')

# パターン別
print('実行パターン:')
print(f'  1. 150チャンネル × 16ジャンル（各4キーワード）: {250*64} pt ← 可能')
print(f'  2. 150チャンネル × 20ジャンル（各4キーワード）: {250*80} pt ← 不可')
print(f'  3. 200チャンネル × ?ジャンルは？')

# 200チャンネルの場合のコスト再計算
search_cost = 100
channel_cost_200 = 200
per_keyword_200 = search_cost + channel_cost_200
print(f'\n200チャンネル 1キーワード当たり: {per_keyword_200} pt')
max_keywords_200 = daily_quota // per_keyword_200
print(f'実行可能な最大キーワード: {max_keywords_200} 個')
print(f'例: 200チャンネル × 12ジャンル（各3キーワード）: {per_keyword_200 * 36} pt ← 可能')
