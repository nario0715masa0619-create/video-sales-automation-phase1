import google.genai as genai
import config
import json

client = genai.Client(api_key=config.GEMINI_API_KEY)

prompt = "YouTube Insight について、60字以上の営業メール用コメントを書いてください。"

print("【リクエスト内容】")
print(f"Model: models/{config.GEMINI_MODEL}")
print(f"Prompt length: {len(prompt)}")
print(f"Prompt: {repr(prompt)}")
print()

response = client.models.generate_content(
    model=f"models/{config.GEMINI_MODEL}",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
        max_output_tokens=512,
        temperature=0.5,
        top_p=0.95,
    )
)

print("【レスポンス詳細】")
print(f"response.text: {repr(response.text)}")
print(f"text length: {len(response.text)}")
print()
print(f"candidates count: {len(response.candidates)}")
print(f"finish_reason: {response.candidates[0].finish_reason}")
print(f"usage_metadata: {response.usage_metadata}")
