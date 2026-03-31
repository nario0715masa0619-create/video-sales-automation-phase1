import asyncio
from playwright.async_api import async_playwright

async def check_detailed(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"\n{'='*60}")
        print(f"URL: {url}")
        print(f"{'='*60}")
        
        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)
        except Exception as e:
            print(f"networkidle 失敗: {e}")
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
        
        await page.wait_for_timeout(5000)
        
        # ページ内容の詳細確認
        html_length = await page.evaluate('() => document.documentElement.outerHTML.length')
        print(f"HTML サイズ: {html_length} bytes")
        
        # iframe の確認
        iframes = await page.query_selector_all('iframe')
        print(f"iframe 数: {len(iframes)}")
        
        # form タグの確認
        forms = await page.query_selector_all('form')
        print(f"form タグ数: {len(forms)}")
        
        # すべての input/textarea/select を確認
        all_inputs = await page.evaluate('''() => {
            return {
                total_inputs: document.querySelectorAll('input').length,
                total_textarea: document.querySelectorAll('textarea').length,
                total_select: document.querySelectorAll('select').length,
                total_all: document.querySelectorAll('input, textarea, select').length
            };
        }''')
        print(f"入力フィールド詳細: {all_inputs}")
        
        # body の最初の HTML スニペット（form 探索）
        body_html = await page.evaluate('''() => {
            return document.body.innerHTML.substring(0, 500);
        }''')
        print(f"Body HTML (最初の500文字): {body_html[:200]}...")
        
        await browser.close()

print("詳細調査開始...")
asyncio.run(check_detailed('https://net-school.co.jp/contact/'))
asyncio.run(check_detailed('https://www.takeda.tv/inquiry/'))
print("\n詳細調査完了")
