"""
test_normalize_url.py
URL 正規化機能のテストスクリプト
"""

from utils import normalize_url

# テストケース
test_cases = [
    # (入力, 期待される出力)
    ("http://www.keieiryoku.jp/）", "http://www.keieiryoku.jp/"),
    ("http://example.com/form?id=123 ", "http://example.com/form?id=123"),
    ("http://example.com/form。", "http://example.com/form"),
    ("http://example.com/inquiry、", "http://example.com/inquiry"),
    ("http://example.com/contact,", "http://example.com/contact"),
    ("http://example.com/form　", "http://example.com/form"),
    ("http://example.com/form)", "http://example.com/form"),
    ("http://example.com/form", "http://example.com/form"),
    ("", ""),
]

print("=" * 60)
print("URL 正規化テスト")
print("=" * 60)

passed = 0
failed = 0

for input_url, expected in test_cases:
    result = normalize_url(input_url)
    is_pass = result == expected
    
    status = "✅ PASS" if is_pass else "❌ FAIL"
    print(f"{status}: {repr(input_url)}")
    print(f"  期待: {repr(expected)}")
    print(f"  結果: {repr(result)}")
    
    if is_pass:
        passed += 1
    else:
        failed += 1
    print()

print("=" * 60)
print(f"結果: {passed}件合格、{failed}件失敗")
print("=" * 60)
