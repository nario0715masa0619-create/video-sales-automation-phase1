import asyncio
from playwright.async_api import async_playwright
import time

async def check_js_generated(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"\n{'='*60}")
        print(f"URL: {url}")
        print(f"{'='*60}")
        
        await page.goto(url, timeout=30000, wait_until='domcontentloaded')
        
        # 段階的な待機でフォーム生成を確認
        for wait_sec in [2, 5, 10, 15]:
            await page.wait_for_timeout(wait_sec * 1000)
            forms_count = await page.evaluate('() => document.querySelectorAll("form").length')
            inputs_count = await page.evaluate('() => document.querySelectorAll("input").length')
            print(f"待機後 {wait_sec}秒: form {forms_count}件, input {inputs_count}件")
        
        # page.content() でフルHTMLをダンプ（デバッグ）
        html = await page.content()
        
        # "contact" や "form" キーワードを含む行を検索
        lines = html.split('\n')
        for i, line in enumerate(lines):
            if any(kw in line.lower() for kw in ['<form', 'name=', 'contact', 'inquiry', 'input type=']):
                if len(line) < 200:
                    print(f"  Line {i}: {line[:150]}")
        
        await browser.close()

print("JavaScript 動的生成調査開始...")
asyncio.run(check_js_generated('https://net-school.co.jp/contact/'))
asyncio.run(check_js_generated('https://www.takeda.tv/inquiry/'))
print("\n調査完了")
