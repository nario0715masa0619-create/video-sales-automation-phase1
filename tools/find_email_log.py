with open('email_extractor.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 'メール取得成功' というログメッセージを検索
import re
matches = re.finditer(r'メール取得成功|メール発見', content)
for match in matches:
    # マッチ位置の前後100文字を表示
    start = max(0, match.start() - 100)
    end = min(len(content), match.end() + 100)
    context = content[start:end]
    print(f'Match: {match.group()}')
    print(f'Context: ...{context}...\n')
