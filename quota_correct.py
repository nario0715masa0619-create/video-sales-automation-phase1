api_keys = 6
daily_quota_per_key = 10000
total_daily_quota = api_keys * daily_quota_per_key

print(f'総日次クォータ: {total_daily_quota} pt\n')

# 150チャンネル × 4ジャンルの場合
cost_150_4genres = 15150 * 4
print(f'150チャンネル × 4ジャンル: {cost_150_4genres} pt')
print(f'実行可能: {cost_150_4genres <= total_daily_quota}')
print(f'余裕: {total_daily_quota - cost_150_4genres} pt\n')

# 200チャンネル × 5ジャンル
cost_200_5genres = 20200 * 5
print(f'200チャンネル × 5ジャンル: {cost_200_5genres} pt')
print(f'実行可能: {cost_200_5genres <= total_daily_quota}')
print(f'余裕: {total_daily_quota - cost_200_5genres} pt\n')

# 150チャンネル × 8ジャンル
cost_150_8genres = 15150 * 8
print(f'150チャンネル × 8ジャンル: {cost_150_8genres} pt')
print(f'実行可能: {cost_150_8genres <= total_daily_quota}')
print(f'余裕: {total_daily_quota - cost_150_8genres} pt\n')

# 推奨: 150チャンネル × 6ジャンル
cost_150_6genres = 15150 * 6
print(f'150チャンネル × 6ジャンル: {cost_150_6genres} pt ← 推奨')
print(f'実行可能: {cost_150_6genres <= total_daily_quota}')
print(f'余裕: {total_daily_quota - cost_150_6genres} pt')
