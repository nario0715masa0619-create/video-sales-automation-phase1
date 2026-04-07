with open('youtube_api_optimized.py', 'r', encoding='utf-8') as f:
    content = f.read()

# KEY3 の後に KEY4 を追加
old_code = '''            if os.getenv("YOUTUBE_API_KEY3"):
                self.api_keys.append(os.getenv("YOUTUBE_API_KEY3"))'''

new_code = '''            if os.getenv("YOUTUBE_API_KEY3"):
                self.api_keys.append(os.getenv("YOUTUBE_API_KEY3"))
            if os.getenv("YOUTUBE_API_KEY4"):
                self.api_keys.append(os.getenv("YOUTUBE_API_KEY4"))'''

content = content.replace(old_code, new_code)

with open('youtube_api_optimized.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ YOUTUBE_API_KEY4 を youtube_api_optimized.py に追加しました')
