import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

models = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]

prompt = """
YouTube Insight データ分析サービスの営業メール用に、1文の営業コメントを書いてください。

チャンネル名：テストチャンネル
最新動画タイトル：【実例】YouTubeの成長戦略

このテーマがYouTube Insightでどう分類されるか、という観点から、
テーマ正規化の価値について30字以上60字未満の日本語で述べてください。

出力：コメント1文のみ
"""

for model_name in models:
    print(f"【{model_name}】")
    try:
        response = client.models.generate_content(
            model=f"models/{model_name}",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                max_output_tokens=256,
                temperature=0.7,
                top_p=0.95,
            )
        )
        print(f"出力: {repr(response.text)}")
        print(f"長さ: {len(response.text)}")
    except Exception as e:
        print(f"エラー: {e}")
    print()
