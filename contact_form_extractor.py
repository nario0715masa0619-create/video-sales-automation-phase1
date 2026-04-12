"""
フォーム自動送信モジュール
複数のフォーム型（HTML、JavaScript、Google Forms等）に対応
"""

from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger(__name__)

class FormStrategy(ABC):
    """フォーム処理の基底クラス"""
    
    @abstractmethod
    def detect(self, driver, url: str) -> bool:
        """このフォーム型に該当するか判定"""
        pass
    
    @abstractmethod
    def fill_and_submit(self, driver, form_data: dict) -> str:
        """フォーム入力・送信実行、メール抽出"""
        pass

class HtmlFormStrategy(FormStrategy):
    """静的 HTML フォーム対応"""
    
    def detect(self, driver, url: str) -> bool:
        try:
            form = driver.find_element(By.TAG_NAME, "form")
            return form is not None
        except:
            return False
    
    def fill_and_submit(self, driver, form_data: dict) -> str:
        # フォーム入力・送信ロジック（後で実装）
        logger.info(f"HTML フォーム送信: {form_data}")
        return ""

class GoogleFormsStrategy(FormStrategy):
    """Google Forms 対応"""
    
    def detect(self, driver, url: str) -> bool:
        return "forms.google.com" in url
    
    def fill_and_submit(self, driver, form_data: dict) -> str:
        logger.info(f"Google Forms 送信: {form_data}")
        return ""

class FormSubmitter:
    """フォーム自動送信オーケストレーター"""
    
    def __init__(self):
        self.strategies = [
            HtmlFormStrategy(),
            GoogleFormsStrategy(),
        ]
    
    def submit_form(self, form_url: str, form_data: dict) -> str:
        """フォーム自動送信実行"""
        driver = webdriver.Chrome()
        try:
            driver.get(form_url)
            
            # フォーム型自動判定
            for strategy in self.strategies:
                if strategy.detect(driver, form_url):
                    logger.info(f"フォーム型判定: {strategy.__class__.__name__}")
                    extracted_email = strategy.fill_and_submit(driver, form_data)
                    return extracted_email
            
            logger.warning(f"対応するフォーム型が見つかりません: {form_url}")
            return ""
        
        finally:
            driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    submitter = FormSubmitter()
    # テスト実行
"""
HTML フォーム自動入力・送信の具体実装
"""

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

class HtmlFormStrategy:
    """静的 HTML フォーム対応"""
    
    def detect(self, driver, url: str) -> bool:
        try:
            form = driver.find_element(By.TAG_NAME, "form")
            return form is not None
        except:
            return False
    
    def fill_and_submit(self, driver, form_data: dict) -> str:
        """フォーム入力・送信"""
        try:
            # テキスト入力フィールドを検索・入力
            inputs = driver.find_elements(By.TAG_NAME, "input")
            
            for input_elem in inputs:
                input_type = input_elem.get_attribute("type")
                input_name = input_elem.get_attribute("name")
                placeholder = input_elem.get_attribute("placeholder")
                
                logger.info(f"フォーム入力: name={input_name}, type={input_type}, placeholder={placeholder}")
                
                # 名前フィールド
                if any(kw in (input_name or "").lower() for kw in ["name", "company"]):
                    input_elem.send_keys("テスト企業")
                    time.sleep(0.5)
                
                # メールフィールド
                elif any(kw in (input_name or "").lower() for kw in ["email", "mail"]):
                    input_elem.send_keys("test@example.com")
                    time.sleep(0.5)
                
                # 電話番号フィールド
                elif any(kw in (input_name or "").lower() for kw in ["phone", "tel"]):
                    input_elem.send_keys("09012345678")
                    time.sleep(0.5)
            
            # テキストエリア（メッセージ）を入力
            textareas = driver.find_elements(By.TAG_NAME, "textarea")
            if textareas:
                textareas[0].send_keys("お問い合わせテスト")
                time.sleep(0.5)
            
            # 送信ボタンを検索・クリック
            submit_button = None
            for btn in driver.find_elements(By.TAG_NAME, "button"):
                if "submit" in (btn.get_attribute("type") or "").lower():
                    submit_button = btn
                    break
            
            if not submit_button:
                submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            if submit_button:
                submit_button.click()
                logger.info("フォーム送信完了")
                time.sleep(2)
                
                # 送信後のメールアドレス抽出（ページテキストから）
                page_text = driver.page_source
                import re
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_text)
                if emails:
                    return emails[0]
            
            return ""
        
        except Exception as e:
            logger.error(f"HTML フォーム送信エラー: {e}")
            return ""

class GoogleFormsStrategy(FormStrategy):
    """Google Forms 自動入力・送信"""
    
    def fill_and_submit(self, driver, form_data: dict) -> str:
        """Google Forms 自動入力・送信"""
        try:
            # Google Forms のテキスト入力フィールドを検索
            text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], textarea")
            
            if len(text_inputs) >= 1:
                text_inputs[0].send_keys("テスト企業")
                time.sleep(0.5)
            
            if len(text_inputs) >= 2:
                text_inputs[1].send_keys("test@example.com")
                time.sleep(0.5)
            
            if len(text_inputs) >= 3:
                text_inputs[2].send_keys("お問い合わせテスト")
                time.sleep(0.5)
            
            # 送信ボタンをクリック
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[jsname]")
            submit_button.click()
            logger.info("Google Forms 送信完了")
            
            time.sleep(2)
            
            # 確認画面からメールアドレス抽出
            page_text = driver.page_source
            import re
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_text)
            if emails:
                return emails[0]
            
            return ""
        
        except Exception as e:
            logger.error(f"Google Forms 送信エラー: {e}")
            return ""

# === テスト実行 ===
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    test_form_url = "https://example.com/contact"
    test_form_data = {
        "company": "テスト企業",
        "email": "test@example.com",
        "phone": "09012345678",
        "message": "お問い合わせテスト"
    }
    
    submitter = FormSubmitter()
    try:
        extracted_email = submitter.submit_form(test_form_url, test_form_data)
        print(f"抽出メール: {extracted_email if extracted_email else 'なし'}")
    except Exception as e:
        print(f"エラー: {e}")
