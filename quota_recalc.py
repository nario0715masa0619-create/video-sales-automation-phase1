# 複数 API キーを考慮した計算

api_keys = 6
daily_quota_per_key = 10000
total_daily_quota = api_keys * daily_quota_per_key

print(f'API キー数: {api_keys}')
print(f'1キー当たり: {daily_quota_per_key} pt')
print(f'総日次クォータ: {total_daily_quota} pt\n')

# 150チャンネル × 4ジャンルの場合
cost_150_4genres = 15150 * 4
print(f'150チャンネル × 4ジャンル: {cost_150_4genres} pt')
print(f'実行可能: {cost_150_4genres <= total_daily_quota} ✅\n')

# 300チャンネル × 5ジャンルの場合
cost_300_5genres = 30300 * 5
print(f'300チャンネル × 5ジャンル: {cost_300_5genres} pt')
print(f'実行可能: {cost_300_5genres <= total_daily_quota} ⚠️')
print(f'オーバー: {cost_300_5genres - total_daily_quota} pt\n')

# 200チャンネル × 5ジャンルなら？
cost_200_5genres = 20200 * 5
print(f'200チャンネル × 5ジャンル: {cost_200_5genres} pt')
print(f'実行可能: {cost_200_5genres <= total_daily_quota} ✅')

# 150チャンネル × 8ジャンルなら？
cost_150_8genres = 15150 * 8
print(f'150チャンネル × 8ジャンル: {cost_150_8genres} pt')
print(f'実行可能: {cost_150_8genres <= total_daily_quota} ✅')
