"""
email_generator.py
==================
Gemini API を使ってリードごとにパーソナライズされた営業メールを生成するモジュール。
【修正: Video Insight 特化版】

【1通目〜4通目のメール役割】
  1通目: Insight テーマ分散の課題 + 動画コメント + 無料診断オファー
  2通目: 事例・ベネフィットの具体例（Insight 正規化による効果）
  3通目: よくある質問（料金・工数・効果）への回答
  4通目: 締めのリマインド（このメールで最後）

【パーソナライズ変数（Gemini 生成）】
  - 会社名、担当者名、チャンネル名、最新動画タイトル
  - 動画への一言コメント（Insight 観点）
  - 改善ポイント（Insight 正規化観点）
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
    【修正: Video Insight 特化版】
    """
    prompt = f"""
あなたは YouTube Insight データ分析のプロフェッショナルです。
以下のYouTubeチャンネルの最新動画を見た際に、
「Insight データの活用観点」からの一言コメントを1〜2文で書いてください。

【チャンネル名】{channel_name}
【最新動画タイトル】{latest_video_title}
【チャンネル説明】{channel_description[:200] if channel_description else "（説明なし）"}

要件：
- 「このテーマは Insight でどう分類されるか」という観点で言及すること
- 「視聴者のコメント分析」「テーマの正規化」など、Insight データに関連した話題を織り交ぜること
- 営業メールの冒頭に使う文章として自然なトーンにすること
- 他のチャンネル名や別の動画タイトルの例を出さないこと
- 箇条書きや「---」「##」などの記号は使わないこと
- 「ためになりました」「勉強になりました」などの過度な褒め言葉は避けること
- 30〜60文字程度の日本語で書くこと
- 文末は「〜という点で、Insight データの活用価値があると感じました」のような形にすること

出力フォーマット：
- 一言コメントのみを1段落で出力してください。
- 前後に説明文や見出し（例：「回答例」「##」）は一切書かないでください。
""".strip()

    try:
        comment = _call_gemini(prompt, max_tokens=128)
        comment = re.sub(r'[\n\r]+', ' ', comment).strip()
        return comment
    except Exception as e:
        logger.warning(f"動画コメント生成失敗: {e}")
        if latest_video_title:
            return f"「{latest_video_title}」で取り上げられていたテーマが、Insight データの分類という観点で活用価値があると感じました"
        else:
            return "動画で取り上げられていたテーマが、Insight データの活用という観点で興味深いと感じました"



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
    【修正: Video Insight 特化版】
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
あなたは YouTube Insight データ分析のコンサルタントです。
以下のYouTubeチャンネルデータを見て、
「Insight データの正規化・活用」という観点から、
具体的な改善余地を1〜2文で指摘してください。

【チャンネル名】{channel_name}
【直近3ヶ月の投稿本数】{videos_3m_count}本
【平均再生数】{avg_view_count:.0f}回
【平均エンゲージメント率】{avg_engagement_rate:.1f}%（{engagement_eval}）
【成長トレンド】{trend}
【総合評価】{rank}ランク

要件：
- 「Insight データでこの{videos_3m_count}本の投稿が『どのテーマに分類されているか』という観点で分析すると、改善余地があります」というような観点で述べること
- Insight データの「正規化」「テーマ統一」に関連した話題を含めること
- 「マーケティング関連は何%か」「テーマの分散度」など、Insight データ特有の指標に言及すること
- 数字を具体的に使って説得力を持たせること
- 過度なネガティブ表現は避け、ポジティブに改善余地を示すこと
- 50〜80文字程度の日本語で書くこと
- 「〜という観点で、Insight データの正規化による改善余地があると考えています」で締めること

改善ポイントのみ出力し、余計な前置きは不要です。
""".strip()

    try:
        hint = _call_gemini(prompt, max_tokens=150)
        hint = re.sub(r'[\n\r]+', ' ', hint).strip()
        return hint
    except Exception as e:
        logger.warning(f"改善ポイント生成失敗: {e}")
        return "Insight データでこれらのテーマがどう分類されているか分析することで、改善余地があると考えています"


def _generate_case_study_detail(
    channel_name: str,
    industry: str = "",
    rank: str = "B",
    videos_3m_count: int = 0,
) -> str:
    """
    事例の具体的な指摘を生成する（2通目メール用）。
    【修正: Video Insight 特化版】
    """
    industry_str = f"（{industry}業界）" if industry else ""

    prompt = f"""
あなたは YouTube Insight データ分析のコンサルタントです。
{channel_name}{industry_str}のYouTubeチャンネルについて、
「Insight データの正規化」によって実現できる改善可能性に関する具体的な指摘を1〜2文で書いてください。

要件：
- 「御社のチャンネルも、投稿されている動画に対する視聴者コメントを Insight で分類すると、『マーケティング関連は何%か』という質問にすぐ答えられるようになります。この正規化という観点で、同様の改善余地があると考えています」のようなニュアンスで述べること
- Insight データの「テーマ分散問題」「正規化の効果」に言及すること
- 「現状では Insight が複数のテーマに分散しているが、これを統一することで...」のような観点で述べること
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
        return "御社のチャンネルも Insight データを正規化することで、テーマの分散問題を解決し、経営層への報告がより具体的になると考えています"


def _generate_effect_prediction(
    channel_name: str,
    avg_view_count: float,
    avg_engagement_rate: float,
) -> str:
    """
    効果予測コメントを生成する（3通目メール用）。
    【修正: Video Insight 特化版】
    """
    prompt = f"""
あなたは YouTube Insight データ分析のコンサルタントです。
以下のデータを持つYouTubeチャンネルに対して、
「Insight データを正規化・活用」することによって実現できる効果予測を1〜2文で書いてください。

【チャンネル名】{channel_name}
【平均再生数】{avg_view_count:.0f}回
【平均エンゲージメント率】{avg_engagement_rate:.1f}%

要件：
- 「平均再生数{avg_view_count:.0f}回のチャンネルであれば、Insight データを正規化することで、『この投稿はマーケティング関連は何%か』『どのテーマが最も反応しているか』という分析が可能になります」というような観点で述べること
- Insight データの「テーマ正規化」による具体的な効果（意思決定の迅速化、経営層報告の具体化など）に言及すること
- 現実的かつ前向きな予測を書くこと
- 50〜80文字程度の日本語で書くこと
- 「〜という観点で、Insight データの正規化による改善可能性があると判断しています」で締めること

予測コメントのみ出力し、余計な前置きは不要です。
""".strip()

    try:
        prediction = _call_gemini(prompt, max_tokens=150)
        prediction = re.sub(r'[\n\r]+', ' ', prediction).strip()
        return prediction
    except Exception as e:
        logger.warning(f"効果予測生成失敗: {e}")
        return "Insight データを正規化することで、テーマの分散問題を解決でき、経営層への報告精度向上という観点で改善可能性があると判断しています"


# ==================================================
# メールテンプレートの構築
# ==================================================

def _build_email_1(lead: dict, personalized: dict) -> EmailContent:
    """
    1通目: Insight テーマ分散課題を直撃するメール
    【修正: Video Insight 特化版】
    """
    channel_name = lead.get('チャンネル名', '')
    latest_title = (lead.get('最新動画タイトル') or "").strip()
    company_name = (lead.get('会社名') or channel_name or '御社').strip()
    
    subject = (
        f"YouTube Insight「{channel_name}」のテーマが"
        f"168個に分散している課題"
    )

    company = lead.get('会社名', '').strip()
    recipient_line = f"{company} 様" if company else "ご担当者様"

    body = f"""
{recipient_line}

はじめまして。{config.MY_COMPANY_NAME}の{config.MY_NAME}と申します。

YouTube Studio から取得できる Insight データって、
「複数の同じテーマが別名で記録される」という課題、
ご存知ですか？

例えば、{channel_name}の場合だと：
「コンテンツ制作」「動画制作」「映像制作」「クリエイティブ制作」

これらは全部「同じ意味」なのに、別々に記録されます。

結果として、テーマが 168 個に分散し、
「{latest_title or '直近の動画'}」のような動画があっても
「マーケティング関連は全体の何%か」
という質問にすぐ答えられない状態になってます。

当社は「日本語に特化した AI」で、
この 168 個を「6 つに完全整理」するサービスを提供しています。

✅ 完全正規化（Unmapped = 0%）
✅ Semantic Purity 0.54 → 0.61（+13%）
✅ 毎月 2～3 時間の手作業が削減

{personalized.get('video_comment', '')}

{personalized.get('improvement_hint', '')}

デモ分析（無料）で、実際の分類結果を見てみませんか？

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
    2通目: Insight 正規化による事例・効果
    【修正: Video Insight 特化版】
    """
    channel_name = lead.get('チャンネル名', '')
    industry = lead.get('業種', '')
    
    subject = f"【事例】Insight 正規化で『マーケティング関連 68%』が判明した話"

    company = lead.get('会社名', '').strip()
    recipient_line = f"{company} 様" if company else "ご担当者様"

    body = f"""
{recipient_line}

先日ご連絡した{config.MY_COMPANY_NAME}の{config.MY_NAME}です。

ご多忙の中恐れ入ります。
今回は参考になるかと思い、事例をご紹介させてください。

■ 類似ケースの改善事例
YouTube Insight データを正規化した企業様で、
テーマ分析と改善提案を実施したところ、
・「マーケティング関連」が全体の 68% と判明
・それに基づいて施策の優先順位を即座に決定可能に
・経営層への報告が「具体的な数字」で説得力UP
という結果が出ています。

{personalized.get('case_study_detail', '')}

無料診断は 30 分程度のオンライン MTG で完結します。
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
    3通目: Insight 正規化に関する FAQ
    【修正: Video Insight 特化版】
    """
    subject = "Insight 正規化について、よくあるご質問にお答えします"

    company = lead.get('会社名', '').strip()
    recipient_line = f"{company} 様" if company else "ご担当者様"

    body = f"""
{recipient_line}

{config.MY_COMPANY_NAME}の{config.MY_NAME}です。

これまでにご検討いただいた企業様からよくいただくご質問に
事前にお答えしておきます。

Q. 本当に「168 個が 6 つに整理」されるのですか？
A. はい。当社の AI は日本語に特化しているため、
   「コンテンツ制作」「動画制作」「映像制作」のような
   同義語を正しく認識して統一できます。
   実績: Unmapped = 0%（完全正規化）

Q. 自社の工数はかかりますか？
A. ヒアリング（30 分）以外は弊社側で完結します。
   納品は JSON 形式で自動出力されます。

Q. 料金はどのくらいですか？
A. まず無料診断から始めていただけます。
   その後のご支援は内容によって異なります。
   詳しくは診断後にお見積もりいたします。

Q. 本当に効果がありますか？
A. {lead.get('会社名', '御社')}様のチャンネルの場合、
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
    【修正: Video Insight 特化版】
    """
    channel_name = lead.get('チャンネル名', '')
    subject = f"「Insight 正規化」{channel_name}様への最終提案"

    company = lead.get('会社名', '').strip()
    recipient_line = f"{company} 様" if company else "ご担当者様"

    body = f"""
{recipient_line}

{config.MY_COMPANY_NAME}の{config.MY_NAME}です。

これまで 3 回ご連絡させていただきました。

タイミングが合わなかったのであれば、
いつでもお気軽にお声がけください。

■ 無料デモで分かること
✅ 「Unmapped Rate」（現在の未分類率）
   推定：YouTube Insight の平均 30～50% が Tubular でも未分類

✅ 「Semantic Purity」（テーマ統一度）
   改善後：0.61 以上（ビジネス報告に使える水準）

✅ 「マーケティング関連は何%か」
   → JSON で自動出力（すぐに経営層報告可能）

✅ 毎月の手作業
   → 2～3 時間削減

「試してみる価値があるな」と思われたら、
このメールに返信していただくだけで結構です。

日程調整させていただきます。

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
    channel_description = lead.get("チャンネル説明", "")
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
            channel_name, latest_title, channel_description
        )
        personalized["improvement_hint"] = _generate_improvement_hint(
            channel_name, videos_3m, avg_view, avg_engagement, trend, rank
        )

    elif email_num == 2:
        # 2通目: 事例の具体的な指摘が必要
        personalized["case_study_detail"] = _generate_case_study_detail(
            channel_name, industry, rank, videos_3m
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
    logger.info("=== email_generator.py 単体テスト（Video Insight 特化版） ===")
    logger.info("※ GEMINI_API_KEY が必要です")

    # テスト用リードデータ
    test_lead = {
        "会社名": "グリーンライフ株式会社",
        "担当者名": "鈴木様",
        "チャンネル名": "GreenLife公式チャンネル",
        "最新動画タイトル": "オーガニック野菜の選び方｜失敗しない5つのポイント",
        "チャンネル説明": "オーガニック野菜とサスティナビリティについての情報発信",
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
        print(f"本文:\n{content.body[:300]}...")
