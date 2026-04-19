"""
test_phone_extractor.py
phone_extractor.py の単体テスト
"""
import sys
sys.path.insert(0, 'D:\\AI_スクリプト成果物\\営業自動化プロジェクト\\video-sales-automation-phase1')

from phone_extractor import is_valid_phone

# テストケース: (電話番号, 期待値(True/False), 説明)
test_cases = [
    # 有効な番号
    ('09012345678', True, '携帯（090）'),
    ('07012345678', True, '携帯（070）'),
    ('08012345678', True, '携帯（080）'),
    ('0312345678', True, '固定電話（東京03、10桁）'),
    ('0612345678', True, '固定電話（大阪06、10桁）'),
    ('01134567890', True, '固定電話（札幌011、11桁）'),
    ('03-1234-5678', True, '固定電話（ハイフン付き）'),
    ('0120123456', True, 'フリーダイヤル（0120）'),
    ('0570123456', True, 'ナビダイヤル（0570）'),
    ('+81312345678', True, '国際電話（+81、9桁）'),

    # 無効な番号
    ('0001249439', False, '00プレフィックス'),
    ('021001061529', False, '02市外局番（実在しない）'),
    ('02100106152', False, '02市外局番（実在しない）'),
    ('00000000000', False, '全同一数字'),
    ('0394898', False, '桁数不足（7桁）'),
    ('', False, '空文字列'),
    ('012345', False, '桁数不足（6桁）'),
    ('0111111111111111', False, '桁数超過（16桁）'),
]

print("=" * 80)
print("📱 phone_extractor.py 単体テスト")
print("=" * 80)

passed = 0
failed = 0

for phone, expected, description in test_cases:
    result = is_valid_phone(phone)
    status = "✅ PASS" if result == expected else "❌ FAIL"
    
    if result == expected:
        passed += 1
    else:
        failed += 1
    
    print(f"{status} | 入力: '{phone}' | 期待値: {expected} | 実結果: {result} | {description}")

print("=" * 80)
print(f"📊 結果: {passed} 件合格、{failed} 件失敗 (合格率: {passed}/{passed+failed})")
print("=" * 80)