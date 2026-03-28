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
    自己紹介 + 動画への一言コメント + 無料診断オファー
    """
    latest_title = (lead.get('最新動画タイトル') or "").strip()
    subject_title = latest_title if latest_title else "YouTube動画"

    subject = (
    f"{lead.get('会社名', '御社')}様の"
    f"「{subject_title[:20]}」を拝見しました"
    )

    company = lead.get('会社名', '').strip()
    recipient_line = f"{company} 御中" if company else "ご担当者様"

    body = f"""
{recipient_line}

はじめまして。{config.MY_COMPANY_NAME}の{config.MY_NAME}と申します。

御社のYouTubeチャンネル「{lead.get('チャンネル名', '')}」を拝見し、\
特に「{latest_title or '直近の動画'}」の内容でご連絡いたしました。

{personalized.get('video_comment', '')}

弊社では、動画を活用したマーケ・営業の改善に特化した
「動画チャンネル無料診断」を提供しています。

御社のチャンネルを簡単に拝見したところ、
{personalized.get('improvement_hint', '')}

よろしければ、5分程度のお時間をいただき、
簡単な診断結果をお伝えできればと思います。

ご都合のよい日程をご返信いただければ幸いです。
{config.EMAIL_SIGNATURE}
""".strip()

    return EmailContent(
        email_num=1,
        subject=subject,
        body=body,
        personalized_comment=personalized.get('video_comment', ''),
        improvement_hint=personalized.get('improvement_hint', ''),
    )


def _build_email_2(lead: dict, personalized: dict) -> EmailContent:
    """
    2通目: 事例・ベネフィットの具体例
    """
    subject = "【事例】動画改善で問い合わせ数が2.3倍になった話"

    company = lead.get('会社名', '').strip()
    recipient_line = f"{company} 御中" if company else "ご担当者様"

    body = f"""
{recipient_line}

先日ご連絡した{config.MY_COMPANY_NAME}の{config.MY_NAME}です。

ご多忙の中恐れ入ります。
今回は参考になるかと思い、事例をご紹介させてください。

■ 類似ケースの改善事例
動画マーケティングに取り組む企業様で、
チャンネル分析と改善提案を実施したところ、
・問い合わせ数：+130%（3ヶ月後）
・動画の平均視聴維持率：+45%
という結果が出ています。

{personalized.get('case_study_detail', '')}

無料診断は30分程度のオンラインMTGで完結します。
一度お試しいただけませんか？

ご返信をお待ちしております。
{config.EMAIL_SIGNATURE}
""".strip()

    return EmailContent(
        email_num=2,
        subject=subject,
        body=body,
    )


def _build_email_3(lead: dict, personalized: dict) -> EmailContent:
    """
    3通目: FAQ対応（料金・工数・効果への回答）
    """
    subject = "よくあるご質問にお答えします（料金・工数・効果）"

    company = lead.get('会社名', '').strip()
    recipient_line = f"{company} 御中" if company else "ご担当者様"

    body = f"""
{recipient_line}

{config.MY_COMPANY_NAME}の{config.MY_NAME}です。

これまでにご検討いただいた企業様からよくいただくご質問に
事前にお答えしておきます。

Q. 料金はどのくらいかかりますか？
A. まず無料診断から始めていただけます。
   その後のご支援は内容によって5〜30万円/月が目安ですが、
   まずは診断結果をご覧いただいてから検討いただければ十分です。

Q. 自社の工数はかかりますか？
A. ヒアリング（30分）以外は弊社側で完結します。

Q. 本当に効果がありますか？
A. {lead.get('会社名', '御社')}様のチャンネルの場合、\
{personalized.get('effect_prediction', '')}

一度だけお話を聞いていただけませんか？
{config.EMAIL_SIGNATURE}
""".strip()

    return EmailContent(
        email_num=3,
        subject=subject,
        body=body,
    )


def _build_email_4(lead: dict, personalized: dict) -> EmailContent:
    """
    4通目: 締めのリマインド（最後のメール）
    """
    subject = f"最後のご連絡です（{lead.get('会社名', '御社')}様へ）"

    company = lead.get('会社名', '').strip()
    recipient_line = f"{company} 御中" if company else "ご担当者様"

    body = f"""
{recipient_line}

{config.MY_COMPANY_NAME}の{config.MY_NAME}です。

これまで数回ご連絡させていただきましたが、
本メールを最後のご連絡とさせていただきます。

もしタイミングが合わなかっただけであれば、
いつでもお声がけください。

■ 無料診断でわかること
・チャンネルの「伸び代スコア」（独自指標）
・競合チャンネルとの差異分析
・今すぐできる改善アクション3つ

ご興味があれば、このメールにご返信いただくだけで
診断の日程調整が可能です。

ありがとうございました。
{config.EMAIL_SIGNATURE}
""".strip()

    return EmailContent(
        email_num=4,
        subject=subject,
        body=body,
    )


# ==================================================
# メイン生成関数
# ==================================================

def generate_email(lead: dict, email_num: int) -> EmailContent:
    """
    リードデータと通数を元に、パーソナライズされたメール文を生成する。

    Args:
        lead: CRMから取得したリードデータの辞書
            キー例: 会社名、チャンネル名、最新動画タイトル、
                    平均再生数、平均エンゲージメント率、ランク 等
        email_num: 送信する通数（1〜4）

    Returns:
        EmailContent: 生成されたメールコンテンツ

    Raises:
        ValueError: email_num が 1〜4 の範囲外の場合
    """
    if email_num not in range(1, config.EMAIL_MAX_SEQUENCE + 1):
        raise ValueError(f"email_num は 1〜{config.EMAIL_MAX_SEQUENCE} の範囲で指定してください")

    channel_name = lead.get("チャンネル名", "")
    company_name = lead.get("会社名", "")
    latest_title = lead.get("最新動画タイトル", "")
    avg_view = float(lead.get("平均再生数", 0) or 0)
    avg_engagement = float(str(lead.get("平均エンゲージメント率", 0) or 0).replace('%', ''))
    trend = lead.get("成長トレンド", "横ばい")
    rank = lead.get("ランク", "B")
    industry = lead.get("業種", "")
    videos_3m = int(lead.get("投稿数（直近3ヶ月）", 0) or 0)

    logger.info(f"メール生成開始: {company_name} - {email_num}通目")

    # Gemini を使ったパーソナライズコンテンツの生成
    personalized: dict = {}

    if email_num == 1:
        # 1通目: 動画コメント + 改善ポイント が必要
        personalized["video_comment"] = _generate_video_comment(
            channel_name, latest_title
        )
        personalized["improvement_hint"] = _generate_improvement_hint(
            channel_name, videos_3m, avg_view, avg_engagement, trend, rank
        )

    elif email_num == 2:
        # 2通目: 事例の具体的な指摘が必要
        personalized["case_study_detail"] = _generate_case_study_detail(
            channel_name, industry, rank
        )

    elif email_num == 3:
        # 3通目: 効果予測が必要
        personalized["effect_prediction"] = _generate_effect_prediction(
            channel_name, avg_view, avg_engagement
        )

    # 4通目はパーソナライズ不要（定型文でOK）

    # テンプレートビルダーで組み立て
    builders = {
        1: _build_email_1,
        2: _build_email_2,
        3: _build_email_3,
        4: _build_email_4,
    }

    email_content = builders[email_num](lead, personalized)

    if not email_content.is_valid():
        logger.error(f"メール生成失敗（空の件名または本文）: {company_name} - {email_num}通目")
    else:
        logger.info(f"メール生成完了: {email_content}")

    return email_content


# ==================================================
# メイン処理（単体テスト用）
# ==================================================

if __name__ == "__main__":
    logger.info("=== email_generator.py 単体テスト ===")
    logger.info("※ GEMINI_API_KEY が必要です")

    # テスト用リードデータ
    test_lead = {
        "会社名": "グリーンライフ株式会社",
        "担当者名": "鈴木様",
        "チャンネル名": "GreenLife公式チャンネル",
        "最新動画タイトル": "オーガニック野菜の選び方｜失敗しない5つのポイント",
        "投稿数（直近3ヶ月）": 10,
        "平均再生数": 3200,
        "平均エンゲージメント率": 4.5,
        "成長トレンド": "上昇",
        "ランク": "A",
        "業種": "EC/D2C",
    }

    for num in range(1, 5):
        print(f"\n{'='*60}")
        print(f"【{num}通目】")
        content = generate_email(test_lead, num)
        print(f"件名: {content.subject}")
        print(f"本文:\n{content.body[:200]}...")
