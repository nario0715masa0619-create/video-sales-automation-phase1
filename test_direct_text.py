import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

prompt = "YouTube Insight のテーマ正規化の価値について、50字程度の営業メール用コメントを1文で書いてください。"

response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
        max_output_tokens=256,
        temperature=0.7,
        top_p=0.95,
    )
)

print("【response.text】")
print(repr(response.text))
print()
print("【candidates[0].content.parts[0].text】")
print(repr(response.candidates[0].content.parts[0].text))
