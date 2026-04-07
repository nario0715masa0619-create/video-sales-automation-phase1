import os

excluded = {'collect.py', 'config.py', 'target_scraper.py', 'scorer.py', 'crm_manager.py', 'email_extractor.py', 'email_sender.py', 'send_email.py', 'cache_manager.py', 'youtube_api_optimized.py', 'utils.py', 'form_submitter.py', 'orchestrator.py', 'send.py', 'smtp_sender.py', 'smtp_test.py', 'send_form.py', 'target_scraper_backup.py', 'target_scraper_OLD.py'}

py_files = sorted([f for f in os.listdir('.') if f.endswith('.py') and f not in excluded])

classification = {'keep_root': [], 'tools': [], 'delete': []}

for f in py_files:
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read(500)
        
        if any(keyword in f.lower() for keyword in ['check_', 'analyze_', 'verify_', 'test_', 'diagnose_', 'fix_', 'show_', 'trace_', 'list_', 'restore_']):
            classification['tools'].append(f)
        elif 'backup' in f.lower() or 'old' in f.lower():
            classification['delete'].append(f)
        else:
            if 'def ' in content and any(x in content.lower() for x in ['test', 'check', 'debug']):
                classification['tools'].append(f)
            else:
                classification['keep_root'].append(f)
    except:
        classification['tools'].append(f)

print('=== ファイル分類結果 ===')
print(f'\nルートに残す: {len(classification["keep_root"])} 個')
for f in classification['keep_root']:
    print(f'  {f}')

print(f'\ntools に移動: {len(classification["tools"])} 個')
for f in classification['tools'][:10]:
    print(f'  {f}')
if len(classification['tools']) > 10:
    print(f'  ... 他 {len(classification["tools"]) - 10} 個')

print(f'\ndelete の対象: {len(classification["delete"])} 個')
for f in classification['delete']:
    print(f'  {f}')
