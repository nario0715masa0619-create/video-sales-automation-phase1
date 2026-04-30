import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

prompt = "YouTube Insight について、営業メール用に80字以上の詳しいコメントを書いてください。"

models_to_test = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

for model_name in models_to_test:
    print(f"【{model_name}】")
    try:
        full_text = ""
        for chunk in client.models.generate_content_stream(
            model=f"models/{model_name}",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                max_output_tokens=512,
                temperature=0.5,
                top_p=0.95,
            )
        ):
            if chunk.text:
                full_text += chunk.text
        
        print(f"出力: {repr(full_text)}")
        print(f"長さ: {len(full_text)}")
    except Exception as e:
        print(f"エラー: {str(e)[:100]}")
    print()
