import asyncio
from playwright.async_api import async_playwright

async def check_buttons(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"\nURL: {url}")
        print(f"{'='*60}")
        
        try:
            await page.goto(url, timeout=30000, wait_until='networkidle')
        except:
            await page.goto(url, timeout=30000, wait_until='domcontentloaded')
        
        await page.wait_for_timeout(5000)
        
        # すべてのボタン/送信要素を検出
        buttons = await page.evaluate('''() => {
            const buttons = Array.from(document.querySelectorAll('button, input[type="submit"], a[class*="btn"]')).map(el => ({
                tag: el.tagName,
                type: el.type,
                text: el.textContent?.trim() || el.value || '',
                class: el.className,
                id: el.id,
                onclick: el.onclick ? 'yes' : 'no',
                visible: el.offsetParent !== null
            }));
            return buttons;
        }''')
        
        print(f"検出されたボタン・送信要素: {len(buttons)}件")
        for i, btn in enumerate(buttons):
            print(f"  [{i}] {btn}")
        
        # form の詳細
        forms = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('form')).map(form => ({
                id: form.id,
                name: form.name,
                method: form.method,
                action: form.action,
                class: form.className
            }));
        }''')
        
        print(f"\nフォーム情報: {len(forms)}件")
        for form in forms:
            print(f"  {form}")
        
        # ページの HTML スニペット（submit や button を含む行）
        html = await page.content()
        lines = html.split('\n')
        print(f"\nsubmit/button を含む行:")
        for i, line in enumerate(lines):
            if any(kw in line.lower() for kw in ['submit', 'button', '<a ', 'onclick']):
                if '<form' not in line.lower() and len(line) < 300:
                    print(f"  Line {i}: {line.strip()[:200]}")
        
        await browser.close()

asyncio.run(check_buttons('https://net-school.co.jp/contact/kojin/'))
