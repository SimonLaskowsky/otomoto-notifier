from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from database import get_last_offer_time  # Dodaj brakujący import

def safe_find(element, xpath, default=None):
    try:
        return element.find_element(By.XPATH, xpath)
    except:
        return default

def safe_get_text(element, xpath, default=None):
    elem = safe_find(element, xpath)
    return elem.text if elem else default

def safe_find_attr(element, xpath, attr, default=None):
    try:
        return element.find_element(By.XPATH, xpath).get_attribute(attr)
    except:
        return default

def parse_price(price_str):
    try:
        return int(price_str.replace(' ', '').replace('zł', '')) if price_str else None
    except:
        return None

def parse_mileage(mileage_str):
    try:
        return int(mileage_str.replace(' ', '').replace('km', '')) if mileage_str else None
    except:
        return None
    
def offer_is_new(offer, last_known_date):
    """Sprawdza czy oferta jest nowsza niż ostatnio sprawdzana"""
    # Tutaj potrzebna dodatkowa logika porównania dat
    return True  # Tymczasowe zawsze zwraca True

def get_offers(search_url):
    """Pobiera oferty z podanego URL z uwzględnieniem filtrowania"""
    # Inicjalizacja opcji Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(search_url)
    
    try:
        last_known_date = get_last_offer_time()
        new_offers = []
        
        while True:
            WebDriverWait(driver, 15).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//main//article'))
            )  # Dodano brakujący nawias
            
            articles = driver.find_elements(By.XPATH, '//main//article')
            
            for article in articles:
                offer = extract_offer_data(article)
                print(f"Oferta: {offer}")
                if offer_is_new(offer, last_known_date):
                    new_offers.append(offer)
                else:
                    return new_offers
            
            if not paginate(driver):
                break
                
        return new_offers
    
    finally:
        driver.quit()

def extract_offer_data(article):
    """Ekstrahuje dane z pojedynczego ogłoszenia"""
    return {
        'title': safe_get_text(article, './/h2//a') or 'Brak tytułu',
        'price': parse_price(safe_get_text(article, './/h3')),
        'year': safe_get_text(article, './/dd[@data-parameter="year"]'),
        'mileage': parse_mileage(safe_get_text(article, './/dd[@data-parameter="mileage"]')),
        'url': safe_find_attr(article, './/h2//a', 'href')
    }

def paginate(driver):
    """Obsługa paginacji"""
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@title="Go to next Page"]'))
        )

        if next_button.get_attribute("aria-disabled") == "true":
            return False

        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        driver.execute_script("arguments[0].click();", next_button)
        
        # Poprawiony brakujący nawias i formatowanie
        WebDriverWait(driver, 15).until(
            EC.invisibility_of_element_located((By.XPATH, '//div[@data-testid="loading-spinner"]'))
        )
        time.sleep(random.uniform(0.5, 2))
        return True
    
    except Exception as e:
        print(f"Błąd paginacji: {str(e)[:200]}")
        return False
