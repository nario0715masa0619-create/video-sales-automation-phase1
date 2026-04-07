with open('youtube_api_optimized.py', 'r', encoding='utf-8') as f:
    content = f.read()

# YOUTUBE_API_KEY2 の後に KEY3 を追加
old_pattern = 'if os.getenv(\"YOUTUBE_API_KEY2\"):\n                self.api_keys.append(os.getenv(\"YOUTUBE_API_KEY2\"))'

new_pattern = '''if os.getenv(\"YOUTUBE_API_KEY2\"):
                self.api_keys.append(os.getenv(\"YOUTUBE_API_KEY2\"))
            if os.getenv(\"YOUTUBE_API_KEY3\"):
                self.api_keys.append(os.getenv(\"YOUTUBE_API_KEY3\"))'''

content = content.replace(old_pattern, new_pattern)

with open('youtube_api_optimized.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ YOUTUBE_API_KEY3 を追加しました')
