import logging
import re
import time
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

logger = logging.getLogger(__name__)

class FormStrategy(ABC):
    """フォーム処理の基底クラス"""

    @abstractmethod
    def detect(self, driver, url: str) -> bool:
        """このフォーム型に該当するか判定"""
        pass

    @abstractmethod
    def fill_and_submit(self, driver, form_data: dict) -> str:
        """フォームを自動入力・送信してメール抽出"""
        pass


class HtmlFormStrategy(FormStrategy):
    """静的 HTML フォーム対応"""

    def detect(self, driver, url: str) -> bool:
        """HTML フォームが存在するか判定"""
        try:
            form = driver.find_element(By.TAG_NAME, "form")
            return form is not None
        except:
            return False

    def fill_and_submit(self, driver, form_data: dict) -> str:
        """HTML フォームを自動入力・送信"""
        try:
            logger.info("HTML フォーム処理開始")
            
            # テキスト入力フィールドを探す
            inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], textarea")
            if len(inputs) >= 1:
                inputs[0].send_keys(form_data.get('company', 'テスト企業'))
                time.sleep(0.3)
            if len(inputs) >= 2:
                inputs[1].send_keys(form_data.get('email', 'test@example.com'))
                time.sleep(0.3)
            if len(inputs) >= 3:
                inputs[2].send_keys(form_data.get('message', 'お問い合わせテスト'))
                time.sleep(0.3)
            
            # 送信ボタンをクリック
            try:
                submit = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
                submit.click()
                logger.info("HTML フォーム送信完了")
            except:
                logger.warning("送信ボタンが見つかりません")
                return ""
            
            time.sleep(2)
            
            # メールアドレスを抽出
            page_text = driver.page_source
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_text)
            return emails[0] if emails else ""
            
        except Exception as e:
            logger.error(f"HTML フォーム処理エラー: {e}")
            return ""


class GoogleFormsStrategy(FormStrategy):
    """Google Forms 対応"""

    def detect(self, driver, url: str) -> bool:
        """Google Forms か判定"""
        return "forms.google.com" in url or "forms.gle" in url

    def fill_and_submit(self, driver, form_data: dict) -> str:
        """Google Forms を自動入力・送信"""
        try:
            logger.info("Google Forms 処理開始")
            
            # テキスト入力フィールドを探す
            inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], textarea")
            if len(inputs) >= 1:
                inputs[0].send_keys(form_data.get('company', 'テスト企業'))
                time.sleep(0.3)
            if len(inputs) >= 2:
                inputs[1].send_keys(form_data.get('email', 'test@example.com'))
                time.sleep(0.3)
            if len(inputs) >= 3:
                inputs[2].send_keys(form_data.get('message', 'お問い合わせテスト'))
                time.sleep(0.3)
            
            # 送信ボタンをクリック
            try:
                submit = driver.find_element(By.CSS_SELECTOR, "button[jsname], button[type='button'][aria-label*='送信']")
                submit.click()
                logger.info("Google Forms 送信完了")
            except:
                logger.warning("Google Forms 送信ボタンが見つかりません")
                return ""
            
            time.sleep(2)
            
            # メールアドレスを抽出
            page_text = driver.page_source
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_text)
            return emails[0] if emails else ""
            
        except Exception as e:
            logger.error(f"Google Forms 処理エラー: {e}")
            return ""


class FormSubmitter:
    """フォーム送信オーケストレータ"""

    def __init__(self):
        self.strategies = [
            HtmlFormStrategy(),
            GoogleFormsStrategy(),
        ]
        logger.info("FormSubmitter 初期化完了")

    def submit_form(self, form_url: str, form_data: dict) -> str:
        """
        フォーム URL に対して自動送信し、メールを抽出
        
        Args:
            form_url: フォーム URL
            form_data: 送信データ {'company', 'email', 'phone', 'message'}
        
        Returns:
            抽出したメールアドレス、見つからない場合は空文字列
        """
        driver = None
        try:
            # Chrome WebDriver 初期化
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            logger.info(f"フォーム URL にアクセス: {form_url}")
            driver.get(form_url)
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
            
            # 適切な Strategy を選択して実行
            for strategy in self.strategies:
                if strategy.detect(driver, form_url):
                    logger.info(f"戦略選択: {strategy.__class__.__name__}")
                    return strategy.fill_and_submit(driver, form_data)
            
            logger.warning(f"対応するフォーム型が見つかりません: {form_url}")
            return ""
            
        except Exception as e:
            logger.error(f"フォーム送信エラー [{form_url}]: {e}")
            return ""
        finally:
            if driver:
                driver.quit()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s'
    )
    
    submitter = FormSubmitter()
    logger.info("✅ FormSubmitter 初期化成功")
