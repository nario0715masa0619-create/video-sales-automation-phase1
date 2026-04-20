import time
import random

# email_generator.py を読む
with open('email_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# リトライ用のヘルパー関数を追加（imports の後）
retry_function = '''
def _call_gemini_with_retry(prompt, max_retries=3, base_wait=5):
    """
    Gemini API を呼び出し、ResourceExhausted エラー時にリトライ
    
    Args:
        prompt: 生成用プロンプト
        max_retries: 最大リトライ回数（デフォルト3回）
        base_wait: 初回待機秒数（デフォルト5秒）
    
    Returns:
        str: 生成結果テキスト
    """
    import time
    import random
    from google.api_core.exceptions import ResourceExhausted
    
    model = genai.GenerativeModel(
        model_name=config.GEMINI_MODEL,
    )
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except ResourceExhausted as e:
            if attempt < max_retries - 1:
                wait_time = base_wait * (2 ** attempt) + random.uniform(0, 5)
                logger.warning(f"ResourceExhausted: retry {attempt + 1}/{max_retries} 後 {wait_time:.1f}秒待機")
                time.sleep(wait_time)
            else:
                logger.error(f"ResourceExhausted: リトライ {max_retries} 回失敗")
                raise
        except Exception as e:
            logger.error(f"Gemini API エラー: {e}")
            raise
'''

# 現在の genai.GenerativeModel 呼び出しを置換
content = content.replace(
    '''    model = genai.GenerativeModel(
        model_name=config.GEMINI_MODEL,
    )
    response = model.generate_content(prompt)
    return response.text.strip()''',
    '''    return _call_gemini_with_retry(prompt)'''
)

# ファイルに書き込む
with open('email_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ リトライロジック追加完了")
