# 1キーワード = 150チャンネルのコスト内訳

# search.list: キーワード1回で複数チャンネルを一括取得
# → 1リクエスト = 100pt（ページネーション無視）
search_cost = 1 * 100

# channels.list: 各チャンネル詳細を個別取得
# → 150チャンネル × 1pt = 150pt
channel_cost = 150 * 1

total_per_keyword = search_cost + channel_cost

print(f'1キーワード当たり:')
print(f'  search.list: {search_cost} pt')
print(f'  channels.list: {channel_cost} pt')
print(f'  合計: {total_per_keyword} pt\n')

# 4ジャンル（各4キーワード）
keywords_per_genre = 4
genres = 4
total_keywords = keywords_per_genre * genres

cost_4genres = total_per_keyword * total_keywords

print(f'4ジャンル（{total_keywords}キーワード）: {cost_4genres} pt')
print(f'クォータ: 60,000 pt')
print(f'実行可能: {cost_4genres <= 60000}')
