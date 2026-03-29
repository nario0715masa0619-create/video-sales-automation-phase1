"""
form_submitter.py
=================
Playwrightを使って問い合わせフォームに自動入力・送信するモジュール。
"""

import asyncio
import re
import logging
from dataclasses import dataclass
from typing import Optional
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

logger = logging.getLogger(__name__)

@dataclass
class FormSubmitResult:
    success: bool
    form_url: str
    company_name: str
    error_message: str = ""
    method: str = "form"

# フォームフィールドの候補キーワード（名前）
NAME_KEYWORDS = ['name', 'お名前', '氏名', '名前', 'your_name', 'contact_name']
# フォームフィールドの候補キーワード（会社名）
COMPANY_KEYWORDS = ['company', '会社', '法人', '社名', '会社名', 'organization']
# フォームフィールドの候補キーワード（メール）
EMAIL_KEYWORDS = ['email', 'mail', 'メール', 'e-mail', 'address']
# フォームフィールドの候補キーワード（電話）
PHONE_KEYWORDS = ['tel', 'phone', '電話', 'telephone']
# フォームフィールドの候補キーワード（本文）
BODY_KEYWORDS = ['message', 'body', '本文', '内容', 'inquiry', 'お問い合わせ内容', 'comment', 'detail']
# 送信ボタンの候補キーワード
SUBMIT_KEYWORDS = ['submit', '送信', '確認', '次へ', 'send', '問い合わせ', '申し込み']


def _match_field(element_attrs: dict, keywords: list) -> bool:
    """要素の属性がキーワードに一致するか判定"""
    check_attrs = ['name', 'id', 'placeholder', 'class', 'aria-label']
    for attr in check_attrs:
        val = str(element_attrs.get(attr, '')).lower()
        if any(kw.lower() in val for kw in keywords):
            return True
    return False


async def submit_form(
    form_url: str,
    company_name: str,
    sender_name: str,
    sender_email: str,
    sender_phone: str,
    message_body: str,
    headless: bool = True,
) -> FormSubmitResult:
    """
    問い合わせフォームに自動入力して送信する。
    """
    result = FormSubmitResult(
        success=False,
        form_url=form_url,
        company_name=company_name,
    )

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()

            # ページを開く
            await page.goto(form_url, timeout=30000, wait_until='domcontentloaded')
            await page.wait_for_timeout(2000)

            filled_count = 0

            # input/textarea要素を全取得
            inputs = await page.query_selector_all('input:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([type="checkbox"]):not([type="radio"]), textarea, select')

            for element in inputs:
                try:
                    attrs = {}
                    for attr in ['name', 'id', 'placeholder', 'class', 'type', 'aria-label']:
                        attrs[attr] = await element.get_attribute(attr) or ''

                    tag = await element.evaluate('el => el.tagName.toLowerCase()')
                    input_type = attrs.get('type', '').lower()

                    # メールフィールド
                    if input_type == 'email' or _match_field(attrs, EMAIL_KEYWORDS):
                        await element.fill(sender_email)
                        filled_count += 1
                        continue

                    # 電話フィールド
                    if input_type == 'tel' or _match_field(attrs, PHONE_KEYWORDS):
                        await element.fill(sender_phone)
                        filled_count += 1
                        continue

                    # 会社名フィールド
                    if _match_field(attrs, COMPANY_KEYWORDS):
                        await element.fill('株式会社ルヴィラ')
                        filled_count += 1
                        continue

                    # 名前フィールド
                    if _match_field(attrs, NAME_KEYWORDS):
                        await element.fill(sender_name)
                        filled_count += 1
                        continue

                    # 本文フィールド（textarea優先）
                    if tag == 'textarea' or _match_field(attrs, BODY_KEYWORDS):
                        await element.fill(message_body)
                        filled_count += 1
                        continue

                except Exception as e:
                    logger.debug(f"フィールド入力エラー: {e}")
                    continue

            if filled_count == 0:
                result.error_message = "入力フィールドが見つかりませんでした"
                await browser.close()
                return result

            logger.info(f"{company_name}: {filled_count}フィールドに入力完了")

            # 送信ボタンを探してクリック
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("送信")',
                'button:has-text("確認")',
                'button:has-text("次へ")',
                'button:has-text("問い合わせ")',
                '*[type="submit"]',
            ]

            submitted = False
            for selector in submit_selectors:
                try:
                    btn = await page.query_selector(selector)
                    if btn and await btn.is_visible():
                        await btn.click()
                        await page.wait_for_timeout(3000)
                        submitted = True
                        logger.info(f"{company_name}: 送信ボタンをクリック ({selector})")
                        break
                except Exception:
                    continue

            if not submitted:
                result.error_message = "送信ボタンが見つかりませんでした"
                await browser.close()
                return result

            result.success = True
            await browser.close()

    except PlaywrightTimeout:
        result.error_message = f"タイムアウト: {form_url}"
        logger.error(f"フォーム送信タイムアウト: {company_name}")
    except Exception as e:
        result.error_message = str(e)
        logger.error(f"フォーム送信エラー [{company_name}]: {e}")

    return result


def submit_form_sync(
    form_url: str,
    company_name: str,
    sender_name: str,
    sender_email: str,
    sender_phone: str,
    message_body: str,
) -> FormSubmitResult:
    """同期版ラッパー（orchestrator.pyから呼び出し用）"""
    return asyncio.run(submit_form(
        form_url=form_url,
        company_name=company_name,
        sender_name=sender_name,
        sender_email=sender_email,
        sender_phone=sender_phone,
        message_body=message_body,
    ))


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

    test_url = sys.argv[1] if len(sys.argv) > 1 else 'https://net-school.co.jp/contact/'
    result = submit_form_sync(
        form_url=test_url,
        company_name='テスト会社',
        sender_name='成相',
        sender_email='biz@luvira.co.jp',
        sender_phone='070-5595-9523',
        message_body='テスト送信です。',
    )
    print(f'結果: {"成功" if result.success else "失敗"}')
    print(f'エラー: {result.error_message}')
