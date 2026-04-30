import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

prompt = """
あなたはYouTube Insight データ分析サービスの営業メール作成者です。

以下の要件に従い、営業メール本文に組み込む「ビジネス価値提案」を書いてください。

【要件】
1. 形式：日本語の1段落（複数文でもよい）
2. 長さ：最低100文字以上
3. 内容：YouTube Insightのテーマ正規化がなぜビジネス価値があるのかを具体的に説明
4. トーン：営業メール向けの自然な日本語、敬語を使用
5. 終わり方：「です。」で終わること

【出力内容】
YouTube Insightのテーマが分散している課題について、テーマ正規化サービスがいかに経営判断を改善するかを、具体例を交えて説明してください。必ず100文字以上の長さで。

出力：コンテンツのみ。余計な説明はなし。
"""

print("【長い出力強制プロンプト】")
full_text = ""
for chunk in client.models.generate_content_stream(
    model="models/gemini-2.5-flash",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
        max_output_tokens=1024,
        temperature=0.7,
        top_p=0.95,
    )
):
    if chunk.text:
        full_text += chunk.text

print(repr(full_text))
print(f"長さ: {len(full_text)}")
