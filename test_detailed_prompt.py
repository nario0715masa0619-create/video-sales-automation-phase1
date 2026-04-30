import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

prompt = """あなたの役割：YouTube Insight データ分析の営業メール作成専門家

タスク：以下のYouTubeチャンネルについて、営業メール本文に組み込める販売コメントを書く

【入力情報】
チャンネル名：テストチャンネル
最新動画タイトル：【実例】YouTubeの成長戦略
説明：マーケティング情報を発信

【出力要件】
- 形式：50文字～100文字の日本語1文
- 内容：このテーマがYouTube Insightでどう分類されるか、という観点から述べる
- トーン：営業メール向けの自然な日本語
- 終わり方：句点「。」で終わること
- 禁止事項：説明や前置きは一切含めない。コメント1文のみを出力する

【重要】
長さを確保してください。50文字以上100文字未満で、内容がある1文を生成してください。
"""

response = client.models.generate_content(
    model=f"models/{config.GEMINI_MODEL}",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
        max_output_tokens=512,
        temperature=0.8,
        top_p=0.95,
    )
)

print("【詳細プロンプト結果】")
print(f"出力: {repr(response.text)}")
print(f"長さ: {len(response.text)}")
