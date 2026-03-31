import asyncio
from playwright.async_api import async_playwright

async def check(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)
        except:
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(5000)
        
        # query_selector_all での検出
        print(f"\n{'='*60}")
        print(f"URL: {url}")
        print(f"{'='*60}")
        
        inputs_qs = await page.query_selector_all('input:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([type="checkbox"]):not([type="radio"]), textarea, select')
        print(f"query_selector_all での検出: {len(inputs_qs)}件")
        
        # JavaScript evaluate での検出
        count = await page.evaluate('''() => {
            const all = document.querySelectorAll('input, textarea, select');
            return Array.from(all).map(el => ({
                type: el.type || el.tagName,
                name: el.name,
                id: el.id,
                placeholder: el.placeholder,
                visible: el.offsetParent !== null
            }));
        }''')
        
        print(f"evaluate での検出: {len(count)}件")
        for f in count[:5]:  # 最初の5件のみ表示
            print(f"  {f}")
        if len(count) > 5:
            print(f"  ... 他 {len(count)-5}件")
        
        await browser.close()

print("調査開始...")
asyncio.run(check('https://net-school.co.jp/contact/'))
asyncio.run(check('https://www.takeda.tv/inquiry/'))
print("\n調査完了")
