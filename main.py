import json
from datetime import datetime, timedelta
from database import init_db, save_offer, get_last_offer_time
from filters import generate_search_url
from notifier import send_sms
from scraper import get_offers

def load_config():
    """Wczytuje konfigurację z uwzględnieniem parametrów wyszukiwania"""
    try:
        with open('config.json') as f:
            config = json.load(f)
            
            # Generuj parametry URL
            config['otomoto_params'] = {
                'brand': config.get('brand'),
                'model': config.get('model'),
                'price_max': config.get('max_price'),
                'year_from': config.get('min_year'),
                'mileage_max': config.get('max_mileage')
            }
            
            return config
    except FileNotFoundError:
        raise Exception("Brak pliku config.json")


init_db()

def check_new_offers():
    """Główna funkcja sprawdzająca nowe oferty"""
    config = load_config()
    
    # Pobierz ostatnie oferty z Otomoto
    search_url = generate_search_url(config['otomoto_params'])
    offers = get_offers(search_url)
    new_offers = []
    for offer in offers:
        # Generuj unikalne ID na podstawie URL
        offer['id'] = str(hash(offer['url']))
        
        if save_offer(offer):
            new_offers.append(offer)
    
    # if new_offers:
    #     message = "🚗 Nowe oferty spełniające kryteria:\n\n"
    #     for offer in new_offers[:5]:  # Max 5 ofert w SMS
    #         message += f"{offer['title']}\nCena: {offer['price']} zł\n{offer['url']}\n\n"
    #     send_sms(message)
    
    print(f"Znaleziono {len(new_offers)} nowych ofert")

if __name__ == "__main__":
    check_new_offers()