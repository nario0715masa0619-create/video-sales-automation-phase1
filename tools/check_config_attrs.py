import config
print('=== config.py のメール関連定数 ===')
for attr in dir(config):
    if 'MY' in attr or 'COMPANY' in attr or 'NAME' in attr or 'SIGNATURE' in attr:
        print(f'{attr} = {getattr(config, attr)}')
