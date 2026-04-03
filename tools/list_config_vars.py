import config

print('=== config.py の利用可能な変数 ===')
for attr in dir(config):
    if 'KEYWORD' in attr or 'SEARCH' in attr or attr.isupper():
        print(f'{attr} = {getattr(config, attr)}')
