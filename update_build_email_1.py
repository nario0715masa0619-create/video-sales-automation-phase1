with open('email_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# _build_email_1 関数を置き換え
new_build_email_1 = '''def _build_email_1(lead: dict, personalized: dict) -> EmailContent:
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

    company = (lead.get('会社名') or "").strip()
    recipient_line = f"{company} 御中" if company else "ご担当者様"

    body = f"""
{recipient_line}

はじめまして。{config.MY_COMPANY_NAME}の{config.MY_NAME}と申します。

御社のYouTubeチャンネル「{lead.get('チャンネル名', '')}」を拝見し、
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

print('✅ _build_email_1 を修正しました')
