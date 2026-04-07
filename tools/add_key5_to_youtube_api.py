with open('youtube_api_optimized.py', 'r', encoding='utf-8') as f:
    content = f.read()

# KEY4 の後に KEY5 を追加
old_code = '''            if os.getenv("YOUTUBE_API_KEY4"):
                self.api_keys.append(os.getenv("YOUTUBE_API_KEY4"))'''

new_code = '''            if os.getenv("YOUTUBE_API_KEY4"):
                self.api_keys.append(os.getenv("YOUTUBE_API_KEY4"))
            if os.getenv("YOUTUBE_API_KEY5"):
                self.api_keys.append(os.getenv("YOUTUBE_API_KEY5"))'''

content = content.replace(old_code, new_code)

with open('youtube_api_optimized.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ YOUTUBE_API_KEY5 を youtube_api_optimized.py に追加しました')
