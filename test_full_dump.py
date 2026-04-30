import google.genai as genai
import config
import json

client = genai.Client(api_key=config.GEMINI_API_KEY)

prompt = "YouTube Insight について、営業メール用に150字以上の詳しいコメントを書いてください。"

response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
        max_output_tokens=2048,
        temperature=0.7,
        top_p=0.95,
    )
)

print("【response オブジェクト全体】")
print(response.model_dump_json(indent=2))
