import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
gemini_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_key)

# 利用可能なモデルを列挙
print('=== 利用可能なモデル ===')
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f'✅ {model.name}')
