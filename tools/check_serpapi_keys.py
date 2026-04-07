import config
print('=== SerpAPI キー設定 ===')
print(f'SERPAPI_KEY_1: {config.SERPAPI_KEYS[0][:10]}...')
print(f'SERPAPI_KEY_2: {config.SERPAPI_KEYS[1][:10]}...')
print(f'現在のキーインデックス: {config.SERPAPI_KEY_INDEX}')
