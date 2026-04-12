# 現在の API クォータ計算

# 1キーワード 150 チャンネル取得のコスト:
search_cost = 150 * 100  # search.list: 100pt/リクエスト
channel_cost = 150 * 1   # channels.list: 1pt/リクエスト
total_per_keyword = search_cost + channel_cost

# 4キーワード × 4ジャンル
keywords_count = 4 * 4
total_quota = total_per_keyword * keywords_count

print(f'1キーワード当たり: {total_per_keyword} pt')
print(f'4ジャンル（4キーワード）: {total_quota} pt')
print(f'API 日次クォータ: 10,000 pt')
print(f'実行可能: {10000 / total_quota:.1f} 回/日')

# 150 を 300 に増やした場合
search_cost_300 = 300 * 100
channel_cost_300 = 300 * 1
total_300 = search_cost_300 + channel_cost_300
total_quota_300 = total_300 * 16

print(f'\n300チャンネルに拡張した場合:')
print(f'1キーワード当たり: {total_300} pt')
print(f'4ジャンル（4キーワード）: {total_quota_300} pt')
print(f'実行可能: {10000 / total_quota_300:.1f} 回/日')
