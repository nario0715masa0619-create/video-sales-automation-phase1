with open('scorer.py', 'r', encoding='utf-8') as f:
    content = f.read()

# score_channels 関数の定義行の直後に1行だけ追加
content = content.replace(
    'def score_channels(channels: list) -> list:',
    'def score_channels(channels: list) -> list:\n    logger.info(f"[score_channels] 開始: {len(channels)}件をスコアリング")'
)

# return sorted_channels の直前に追加
import re
content = re.sub(
    r'(\n    return sorted_channels)',
    r'\n    logger.info(f"[score_channels] 完了: {len(sorted_channels)}件")\n    return sorted_channels',
    content
)

with open('scorer.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ scorer.py にログを追加しました')
