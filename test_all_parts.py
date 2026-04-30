import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

prompt = "YouTube Insight のテーマ正規化について、50字以上の営業メール用コメントを1文で書いてください。"

response = client.models.generate_content(
    model=f"models/{config.GEMINI_MODEL}",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
        max_output_tokens=512,
        temperature=0.8,
        top_p=0.95,
    )
)

print("【response.text】")
print(repr(response.text))
print()

print("【手動抽出：candidates[0].content.parts すべて】")
for i, part in enumerate(response.candidates[0].content.parts):
    print(f"Part {i}: {repr(part.text)}")
print()

print("【全パーツ結合】")
full_text = "".join([part.text for part in response.candidates[0].content.parts if part.text])
print(repr(full_text))
print(f"長さ: {len(full_text)}")
