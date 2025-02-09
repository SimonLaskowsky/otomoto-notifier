def is_good_deal(car, config):
    """Sprawdza ofertę względem konfiguracji"""
    basic_checks = [
        car["price"] <= config["max_price"],
        car["year"] >= config["min_year"]
    ]
    
    if config["allowed_brands"]:
        brand = car["title"].split()[0]
        basic_checks.append(brand in config["allowed_brands"])
    
    if config["max_mileage"] is not None:
        basic_checks.append(car.get("mileage", 0) <= config["max_mileage"])
    
    return all(basic_checks)