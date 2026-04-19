import re

# 札幌011が何にマッチしているか確認
phone1 = '01234567890'
pattern1_011 = r'^011\d{7}$'
pattern1_other = r'^0[1-9]\d{9}$'

print(f"Phone: {phone1}")
print(f"  Pattern ^011\\d{{7}}$: {bool(re.match(pattern1_011, phone1))}")
print(f"  Pattern ^0[1-9]\\d{{9}}$: {bool(re.match(pattern1_other, phone1))}")
print()

# 国際電話が何にマッチしているか確認
phone2 = '+81312345678'
pattern2 = r'^\+81\d{9,11}$'
remaining_digits = phone2[3:]
print(f"Phone: {phone2}")
print(f"  Pattern ^\\+81\\d{{9,11}}$: {bool(re.match(pattern2, phone2))}")
print(f"  Digits after +81: {remaining_digits} (length: {len(remaining_digits)})")