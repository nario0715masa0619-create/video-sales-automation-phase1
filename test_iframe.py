import asyncio
from playwright.async_api import async_playwright

async def check_iframe(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"\n{'='*60}")
        print(f"URL: {url}")
        print(f"{'='*60}")
        
        try:
            await page.goto(url, timeout=30000, wait_until='domcontentloaded')
        except Exception as e:
            print(f"読み込み失敗: {e}")
        
        await page.wait_for_timeout(5000)
        
        # iframe の詳細確認
        iframes_info = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('iframe')).map((el, idx) => ({
                index: idx,
                src: el.src,
                id: el.id,
                name: el.name,
                class: el.className
            }));
        }''')
        
        print(f"iframe 一覧: {iframes_info}")
        
        # iframe 内のフォーム確認
        for i, frame in enumerate(page.frames):
            if frame == page.main_frame:
                print(f"\n[メインフレーム]")
            else:
                print(f"\n[iframe {i}]")
            
            try:
                inputs = await frame.query_selector_all('input, textarea, select, form')
                print(f"  検出フィールド: {len(inputs)}件")
                
                # iframe 内の詳細情報
                details = await frame.evaluate('''() => ({
                    forms: document.querySelectorAll('form').length,
                    inputs: document.querySelectorAll('input').length,
                    textareas: document.querySelectorAll('textarea').length,
                    selects: document.querySelectorAll('select').length,
                    body_html: document.body.innerHTML.substring(0, 300)
                })''')
                print(f"  詳細: {details}")
            except Exception as e:
                print(f"  エラー: {e}")
        
        await browser.close()

print("iframe 調査開始...")
asyncio.run(check_iframe('https://net-school.co.jp/contact/'))
asyncio.run(check_iframe('https://www.takeda.tv/inquiry/'))
print("\niframe 調査完了")
