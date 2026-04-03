import config

# YouTube Data API キーの確認
if hasattr(config, 'YOUTUBE_API_KEY'):
    print('✅ YOUTUBE_API_KEY が設定されています')
    print(f'   キー先頭10文字: {config.YOUTUBE_API_KEY[:10]}...')
else:
    print('❌ YOUTUBE_API_KEY が config.py に存在しません')
    print('   設定が必要です')
