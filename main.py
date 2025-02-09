from filters import is_good_deal
from notifier import send_sms

# Symulacja pobranych ofert (docelowo API Otomoto)
offers = [
    {"title": "Audi A4 2018", "price": 45000, "year": 2018, "url": "https://otomoto.pl/audi1"},
    {"title": "BMW 3 2016", "price": 52000, "year": 2016, "url": "https://otomoto.pl/bmw2"},
    {"title": "Skoda Octavia 2019", "price": 49000, "year": 2019, "url": "https://otomoto.pl/skoda3"},
]

# Przeszukujemy oferty
for car in offers:
    if is_good_deal(car):
        message = f"🚗 {car['title']} za {car['price']} zł! 🔥 {car['url']}"
        send_sms(message)
