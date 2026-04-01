import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
gemini_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_key)

# 利用可能なモデルをリスト
print('=== 利用可能なモデル ===')
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f'✅ {model.name}')
except Exception as e:
    print(f'❌ エラー: {str(e)[:100]}')
    print()
    print('Google Gemini API ドキュメント参照：')
    print('https://ai.google.dev/tutorials/rest_quickstart')
