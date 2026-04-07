with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# YOUTUBE_API_KEY が既に存在するか確認
if 'YOUTUBE_API_KEY' not in content:
    # 最後に追加
    addition = '''
# YouTube Data API v3
YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY が .env に設定されていません")
'''
    with open('config.py', 'a', encoding='utf-8') as f:
        f.write(addition)
    print('✅ YOUTUBE_API_KEY を config.py に追加しました')
else:
    print('ℹ️ YOUTUBE_API_KEY は既に config.py に存在します')
