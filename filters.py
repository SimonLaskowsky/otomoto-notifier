def is_good_deal(car):
    """Sprawdza, czy oferta jest dobra (przykładowe warunki)"""
    return car["price"] < 50000 and car["year"] > 2015
