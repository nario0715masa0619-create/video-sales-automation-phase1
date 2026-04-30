import google.generativeai as genai
import config

genai.configure(api_key=config.GEMINI_API_KEY)

# シンプルなテスト
prompt = "『テスト』と1文で返してください。"
model = genai.GenerativeModel(config.GEMINI_MODEL)
response = model.generate_content(prompt)

print('【テスト1】')
print(f'入力: {prompt}')
print(f'出力: {repr(response.text)}')
print(f'長さ: {len(response.text)}')
print()

# 詳細なテスト
prompt2 = """日本語で50文字以上の1文を書いてください。
内容：YouTubeのテーマ分類について
出力：1文のみ。句点で終わる。余計な説明なし。"""

response2 = model.generate_content(prompt2)
print('【テスト2】')
print(f'出力: {repr(response2.text)}')
print(f'長さ: {len(response2.text)}')
