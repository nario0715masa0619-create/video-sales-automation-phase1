"""
email_generator.py
==================
Gemini API を使ってリードごとにパーソナライズされた営業メールを生成するモジュール。

【1通目〜4通目のメール役割】
  1通目: 自己紹介 + 動画への一言コメント + 無料診断オファー
  2通目: 事例・ベネフィットの具体例
  3通目: よくある質問（料金・工数・不安点）への回答
  4通目: 締めのリマインド（このメールで最後）

【パーソナライズ変数】
  - 会社名、担当者名
  - チャンネル名、最新動画タイトル
  - 動画への一言コメント（Geminiが生成）
  - 改善ポイントの一言（Geminiが生成）
  - 業種、ランク
"""

import re
from dataclasses import dataclass
from typing import Optional
from loguru import logger

import google.generativeai as genai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

import config

# Gemini API の初期化
genai.configure(api_key=config.GEMINI_API_KEY)


# ==================================================
# データクラス定義
# ==================================================

@dataclass
class EmailContent:
    """生成されたメールコンテンツ"""
    email_num: int          # 通数（1〜4）
    subject: str            # 件名
    body: str               # 本文
    personalized_comment: str = ""   # 動画への一言コメント（Gemini生成）
    improvement_hint: str = ""       # 改善ポイント（Gemini生成）

    def is_valid(self) -> bool:
        """件名と本文が両方存在するか確認"""
        return bool(self.subject) and bool(self.body)

    def __str__(self) -> str:
        return f"[{self.email_num}通目] 件名: {self.subject[:50]}..."


# ==================================================
# Gemini によるパーソナライズコンテンツ生成
# ==================================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
)
def _call_gemini(prompt: str, max_tokens: int = 1024) -> str:
    """
    Gemini API を呼び出してテキストを生成する。

    Args:
        prompt: 送信するプロンプト
        max_tokens: 生成トークン数の上限

    Returns:
        str: 生成されたテキスト
    """
    model = genai.GenerativeModel(
        model_name=config.GEMINI_MODEL,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=0.7,      # 適度な創造性
            top_p=0.95,
        )
    )
    response = model.generate_content(prompt)
    return response.text.strip()



def _generate_video_comment(
    channel_name: str,
    latest_video_title: str,
    channel_description: str = "",
) -> str:
    """
    最新動画への一言コメントを生成する（1通目メール用）。
    """
    prompt = f"""
あなたはBtoB営業のプロフェッショナルです。
以下のYouTubeチャンネルの最新動画を見た感想を、
「自然で誠実な一言コメント」として1〜2文で書いてください。

【チャンネル名】{channel_name}
【最新動画タイトル】{latest_video_title}
【チャンネル説明】{channel_description[:200] if channel_description else "（説明なし）"}

要件：
- 営業メールの冒頭に使う文章として自然なトーンにすること
- 上記の動画タイトルと内容についてのみ具体的に言及すること
- 他のチャンネル名や別の動画タイトルの例を出さないこと
- 箇条書きや「---」「##」などの記号は使わないこと
- 「ためになりました」「勉強になりました」などの過度な褒め言葉は避けること
- 30〜60文字程度の日本語で書くこと
- 文末は「〜という点に興味を持ちました」「〜が印象的でした」のような形にすること

出力フォーマット：
- 一言コメントのみを1段落で出力してください。
- 前後に説明文や見出し（例：「回答例」「##」）は一切書かないでください。
""".strip()

    try:
        comment = _call_gemini(prompt, max_tokens=128)
        comment = re.sub(r'[\\n\\r]+', ' ', comment).strip()
        return comment
    except Exception as e:
        logger.warning(f"動画コメント生成失敗: {e}")
        if latest_video_title:
            return f"「{latest_video_title}」で触れられていた内容が、顧客との共通言語づくりという点で印象的でした"
        else:
            return "動画で取り上げられていた視点が、顧客との共通言語づくりという点で印象的でした"



def _generate_improvement_hint(
    channel_name: str,
    videos_3m_count: int,
    avg_view_count: float,
    avg_engagement_rate: float,
    trend: str,
    rank: str,
) -> str:
    """
    チャンネルの改善ポイントの一言を生成する（1通目・3通目メール用）。

    Args:
        channel_name: チャンネル名
        videos_3m_count: 直近3ヶ月の投稿本数
        avg_view_count: 平均再生数
        avg_engagement_rate: 平均エンゲージメント率（%表記）
        trend: 成長トレンド（上昇/横ばい/下降）
        rank: ランク（A/B/C）

    Returns:
        str: 改善ポイントの一言（1〜2文）
    """
    # エンゲージメント率の評価
    if avg_engagement_rate >= 5.0:
        engagement_eval = "高い（良好）"
    elif avg_engagement_rate >= 3.0:
        engagement_eval = "平均的"
    elif avg_engagement_rate >= 1.0:
        engagement_eval = "やや低め"
    else:
        engagement_eval = "低め（改善余地あり）"

    prompt = f"""
あなたは動画マーケティングのコンサルタントです。
以下のYouTubeチャンネルデータを見て、
「具体的な改善余地」を1〜2文で指摘してください。

【チャンネル名】{channel_name}
【直近3ヶ月の投稿本数】{videos_3m_count}本
【平均再生数】{avg_view_count:.0f}回
【平均エンゲージメント率】{avg_engagement_rate:.1f}%（{engagement_eval}）
【成長トレンド】{trend}
【総合評価】{rank}ランク

要件：
- 「〜という観点で、さらに改善余地があると考えています」のような形で締めること
- 数字を具体的に使って説得力を持たせること
- 過度なネガティブ表現は避け、ポジティブに改善余地を示すこと
- 50〜80文字程度の日本語で書くこと

改善ポイントのみ出力し、余計な前置きは不要です。
""".strip()

    try:
        hint = _call_gemini(prompt, max_tokens=150)
        hint = re.sub(r'[\n\r]+', ' ', hint).strip()
        return hint
    except Exception as e:
        logger.warning(f"改善ポイント生成失敗: {e}")
        return "動画のエンゲージメント率とリーチの拡大という観点で、改善余地があると考えています"


def _generate_case_study_detail(
    channel_name: str,
    industry: str = "",
    rank: str = "B",
) -> str:
    """
    事例の具体的な指摘を生成する（2通目メール用）。

    Args:
        channel_name: チャンネル名
        industry: 業種
        rank: ランク

    Returns:
        str: 事例の具体的な指摘（1〜2文）
    """
    industry_str = f"（{industry}業界）" if industry else ""

    prompt = f"""
あなたは動画マーケティングのコンサルタントです。
{channel_name}{industry_str}のYouTubeチャンネルについて、
「問い合わせ増加の可能性」に関する具体的な指摘を1〜2文で書いてください。

要件：
- 「御社のチャンネルも〜という点で、同様の改善余地があると考えています」で締めること
- 具体的・前向きなトーンで書くこと
- 50〜80文字程度の日本語で書くこと

指摘文のみ出力し、余計な前置きは不要です。
""".strip()

    try:
        detail = _call_gemini(prompt, max_tokens=150)
        detail = re.sub(r'[\n\r]+', ' ', detail).strip()
        return detail
    except Exception as e:
        logger.warning(f"事例詳細生成失敗: {e}")
        return "御社のチャンネルも動画の構成と配信タイミングを最適化することで、同様の改善余地があると考えています"


def _generate_effect_prediction(
    channel_name: str,
    avg_view_count: float,
    avg_engagement_rate: float,
) -> str:
    """
    効果予測コメントを生成する（3通目メール用）。

    Args:
        channel_name: チャンネル名
        avg_view_count: 平均再生数
        avg_engagement_rate: 平均エンゲージメント率（%）

    Returns:
        str: 効果予測コメント（1〜2文）
    """
    prompt = f"""
あなたは動画マーケティングのコンサルタントです。
以下のデータを持つYouTubeチャンネルに対して、
「改善した場合に期待できる効果の予測」を1〜2文で書いてください。

【チャンネル名】{channel_name}
【平均再生数】{avg_view_count:.0f}回
【平均エンゲージメント率】{avg_engagement_rate:.1f}%

要件：
- 「〜という観点で改善余地があると判断しています」で締めること
- 現実的かつ前向きな予測を書くこと
- 50〜80文字程度の日本語で書くこと

予測コメントのみ出力し、余計な前置きは不要です。
""".strip()

    try:
        prediction = _call_gemini(prompt, max_tokens=150)
        prediction = re.sub(r'[\n\r]+', ' ', prediction).strip()
        return prediction
    except Exception as e:
        logger.warning(f"効果予測生成失敗: {e}")
        return "動画の視聴維持率と検索流入を改善することで、問い合わせ増加が見込めるという観点で改善余地があると判断しています"


# ==================================================
# メールテンプレートの構築
# ==================================================

def _build_email_1(lead: dict, personalized: dict) -> EmailContent:
    """
    1通目: 初回接触メール
    自己紹介 + 動画への一言コメント + スクレイピング分析の強み紹介 + 資料オファー
    """
    latest_title = (lead.get('最新動画タイトル') or "").strip()
    subject_title = latest_title if latest_title else "YouTube動画"

    subject = (
        f"{lead.get('会社名', '御社')}様の"
        f"「{subject_title[:20]}」を拝見しました"
    )

    company = (lead.get('会社名') or "").strip()
    recipient_line = f"{company} 御中" if company else "ご担当者様"

    body = f"""
{recipient_line}

はじめまして。{config.MY_COMPANY_NAME}の{config.MY_NAME}と申します。

御社のYouTubeチャンネル「{lead.get('チャンネル名', '')}」、
特に「{latest_title or '直近の動画'}」を拝見し、ご連絡しました。

{personalized.get('video_comment', '')}

弊社では、直近の動画をスクレイピングしてJSON化し、
タイトルや概要欄の重要ワードと再生数の関係をスコアリングしています。

{personalized.get('improvement_hint', '')}
といった点が、伸ばしやすいポイントだと感じました。

この仕組みで御社に対して「何ができるか」をまとめた
サービス概要（カタログ）をご用意していますので、
「資料希望」とだけご返信ください。

どうぞよろしくお願いいたします。
{config.EMAIL_SIGNATURE}
""".strip()

    return EmailContent(
        subject=subject,
        body=body,
        type="email_1",
    )