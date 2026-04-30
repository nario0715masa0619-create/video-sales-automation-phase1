import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

prompt = "YouTube Insight のテーマ正規化について、営業メール用に60字以上の詳しいコメントを書いてください。"

print("【ストリーミング出力】")
full_text = ""

for chunk in client.models.generate_content_stream(
    model=f"models/{config.GEMINI_MODEL}",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
        max_output_tokens=512,
        temperature=0.5,
        top_p=0.95,
    )
):
    if chunk.text:
        print(repr(chunk.text), end=" ")
        full_text += chunk.text

print()
print()
print(f"【結合テキスト】")
print(repr(full_text))
print(f"長さ: {len(full_text)}")
