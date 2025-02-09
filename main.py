import json
from filters import is_good_deal
from notifier import send_sms

def load_config():
    """Wczytuje konfigurację z pliku JSON z domyślnymi wartościami"""
    default_config = {
        "max_price": 50000,
        "min_year": 2015,
        "allowed_brands": [],
        "max_mileage": None
    }
    
    try:
        with open('config.json') as f:
            config = json.load(f)
            return {**default_config, **config}
    except FileNotFoundError:
        return default_config

# Wczytaj konfigurację
config = load_config()

# Symulacja pobranych ofert
offers = [
    {"title": "Audi A4 2018", "price": 45000, "year": 2018, "url": "https://otomoto.pl/audi1", "mileage": 120000},
    {"title": "BMW 3 2016", "price": 52000, "year": 2016, "url": "https://otomoto.pl/bmw2", "mileage": 180000},
    {"title": "Skoda Octavia 2019", "price": 49000, "year": 2019, "url": "https://otomoto.pl/skoda3", "mileage": 90000},
]

for car in offers:
    if is_good_deal(car, config):
        message = f"🚗 {car['title']} za {car['price']} zł! 🔥 {car['url']}"
        send_sms(message)