with open('crm_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# update_fields に送信ステータスを追加
old_update_fields = '''            update_fields = {
                "チャンネル登録者数": lead_data.get("チャンネル登録者数", old_record.get("チャンネル登録者数")),
                "投稿数（直近3ヶ月）": lead_data.get("投稿数（直近3ヶ月）", old_record.get("投稿数（直近3ヶ月）")),
                "平均再生数": lead_data.get("平均再生数", old_record.get("平均再生数")),
                "平均エンゲージメント率": lead_data.get("平均エンゲージメント率", old_record.get("平均エンゲージメント率")),
                "成長トレンド": lead_data.get("成長トレンド", old_record.get("成長トレンド")),
                "投稿頻度スコア": lead_data.get("投稿頻度スコア", old_record.get("投稿頻度スコア")),
                "再生数スコア": lead_data.get("再生数スコア", old_record.get("再生数スコア")),
                "エンゲージメントスコア": lead_data.get("エンゲージメントスコア", old_record.get("エンゲージメントスコア")),
                "トレンドスコア": lead_data.get("トレンドスコア", old_record.get("トレンドスコア")),
                "総合スコア": lead_data.get("総合スコア", old_record.get("総合スコア")),
                "ランク": lead_data.get("ランク", old_record.get("ランク")),
                "最新動画タイトル": lead_data.get("最新動画タイトル", old_record.get("最新動画タイトル", "")),
                "問い合わせフォームURL": lead_data.get("問い合わせフォームURL", old_record.get("問い合わせフォームURL")),
                "メールアドレス": lead_data.get("メールアドレス", old_record.get("メールアドレス")),
                "最終更新日": now,
            }'''

new_update_fields = '''            update_fields = {
                "チャンネル登録者数": lead_data.get("チャンネル登録者数", old_record.get("チャンネル登録者数")),
                "投稿数（直近3ヶ月）": lead_data.get("投稿数（直近3ヶ月）", old_record.get("投稿数（直近3ヶ月）")),
                "平均再生数": lead_data.get("平均再生数", old_record.get("平均再生数")),
                "平均エンゲージメント率": lead_data.get("平均エンゲージメント率", old_record.get("平均エンゲージメント率")),
                "成長トレンド": lead_data.get("成長トレンド", old_record.get("成長トレンド")),
                "投稿頻度スコア": lead_data.get("投稿頻度スコア", old_record.get("投稿頻度スコア")),
                "再生数スコア": lead_data.get("再生数スコア", old_record.get("再生数スコア")),
                "エンゲージメントスコア": lead_data.get("エンゲージメントスコア", old_record.get("エンゲージメントスコア")),
                "トレンドスコア": lead_data.get("トレンドスコア", old_record.get("トレンドスコア")),
                "総合スコア": lead_data.get("総合スコア", old_record.get("総合スコア")),
                "ランク": lead_data.get("ランク", old_record.get("ランク")),
                "最新動画タイトル": lead_data.get("最新動画タイトル", old_record.get("最新動画タイトル", "")),
                "問い合わせフォームURL": lead_data.get("問い合わせフォームURL", old_record.get("問い合わせフォームURL")),
                "メールアドレス": lead_data.get("メールアドレス", old_record.get("メールアドレス")),
                "送信ステータス": lead_data.get("送信ステータス", old_record.get("送信ステータス", "")),
                "最終送信日": lead_data.get("最終送信日", old_record.get("最終送信日", "")),
                "最終更新日": now,
            }'''

content = content.replace(old_update_fields, new_update_fields)

with open('crm_manager.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ update_fields に送信ステータスと最終送信日を追加しました')
