with open('email_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# _build_email_1 関数を置き換え（修正版の本文を保持）
new_build_email_1 = '''def _build_email_1(lead: dict, personalized: dict) -> EmailContent:
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
    )'''

# 現在の _build_email_1 を新しいコードで置き換え
import re
pattern = r'def _build_email_1\(lead: dict, personalized: dict\) -> EmailContent:.*?(?=\n    def |\Z)'
content = re.sub(pattern, new_build_email_1, content, flags=re.DOTALL)

with open('email_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ _build_email_1 を修正しました（修正版の本文を保持）')
