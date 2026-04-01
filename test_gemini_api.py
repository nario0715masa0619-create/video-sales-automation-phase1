import os
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv('GEMINI_API_KEY')

if gemini_key:
    print(f'✅ GEMINI_API_KEY は設定されています')
    print(f'   キーの最初の 10 文字: {gemini_key[:10]}...')
    
    # キーが流出していないか確認
    import google.generativeai as genai
    genai.configure(api_key=gemini_key)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content('テスト')
        print(f'✅ Gemini API は正常に動作しています')
    except Exception as e:
        print(f'❌ Gemini API エラー: {str(e)[:100]}')
else:
    print('❌ GEMINI_API_KEY が見つかりません')
