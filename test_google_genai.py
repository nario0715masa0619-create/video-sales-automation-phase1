import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

prompt = """
あなたは YouTube Insight データ分析の営業メール作成専門家です。
以下のYouTubeチャンネルについて、営業メール本文に組み込める1文のコメントを書いてください。

【チャンネル名】テストチャンネル
【最新動画タイトル】【実例】YouTubeの成長戦略

要件：
- 営業メール内に自然に組み込める1文（80～150文字）
- 「このテーマはYouTube Insightでどう分類されるか」という観点を含める
- 「視聴者のコメント分析」「テーマの正規化」などInsight関連の話題を織り交ぜる
- 営業メールのトーンで自然な日本語
- 句点「。」で終わる
- 余計な説明や前置きは一切不要

出力：1文のコメントのみ。何も追加しないでください。
"""

response = client.models.generate_content(
    model=f"models/{config.GEMINI_MODEL}",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
        max_output_tokens=256,
        temperature=0.7,
        top_p=0.95,
    )
)

print("【google.genai テスト】")
print(f"出力: {repr(response.text)}")
print(f"長さ: {len(response.text)}")
