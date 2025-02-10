import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('offers.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS offers (
            id TEXT PRIMARY KEY,
            title TEXT,
            price INTEGER,
            year INTEGER,
            mileage INTEGER,
            url TEXT UNIQUE,
            created_at TIMESTAMP,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_offer(offer):
    conn = sqlite3.connect('offers.db')
    c = conn.cursor()
    try:
        c.execute('''
    INSERT INTO offers 
    (id, title, price, year, mileage, url, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (
    offer['id'], 
    offer['title'], 
    offer['price'], 
    offer['year'], 
    offer['mileage'],
    offer['url'],
    datetime.now()
))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Oferta już istnieje
    finally:
        conn.close()

def get_last_offer_time():
    conn = sqlite3.connect('offers.db')
    c = conn.cursor()
    c.execute('SELECT MAX(created_at) FROM offers')
    result = c.fetchone()[0]
    conn.close()
    return result if result else datetime.min