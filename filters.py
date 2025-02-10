def generate_search_url(params):
    """Generuje URL Otomoto na podstawie parametrów"""
    base_url = "https://www.otomoto.pl/osobowe"
    
    if params.get('brand'):
        base_url += f"/{params['brand'].lower()}"
        if params.get('model'):
            base_url += f"/{params['model'].lower()}"
    
    query_params = []
    
    if params.get('price_max'):
        query_params.append(f"search[filter_float_price:to]={params['price_max']}")
    
    if params.get('year_from'):
        query_params.append(f"search[filter_float_year:from]={params['year_from']}")
    
    if params.get('mileage_max'):
        query_params.append(f"search[filter_float_mileage:to]={params['mileage_max']}")
    
    # Sortowanie od najnowszych
    query_params.append("search[order]=created_at:desc")
    
    return f"{base_url}?{'&'.join(query_params)}" if query_params else base_url