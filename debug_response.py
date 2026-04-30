import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

prompt = "こんにちは。『テスト』と1文で返してください。"

response = client.models.generate_content(
    model=f"models/{config.GEMINI_MODEL}",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
        max_output_tokens=256,
        temperature=0.7,
        top_p=0.95,
    )
)

print("【response オブジェクト全体】")
print(f"type: {type(response)}")
print(f"dir: {[x for x in dir(response) if not x.startswith('_')]}")
print()
print("【response.text】")
print(repr(response.text))
print()
print("【その他の属性】")
for attr in ['candidates', 'content', 'usage_metadata', 'finish_reason']:
    if hasattr(response, attr):
        print(f"{attr}: {getattr(response, attr)}")
