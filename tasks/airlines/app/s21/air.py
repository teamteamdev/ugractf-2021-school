import random
from random import choice as pick
from random import randint as rint

MAX_PRICE = 5000

flights = [
    ("Ханты-Мансийск", "HMA", 0),
    ("Краснодар", "KRR", 4000),
    ("Сочи", "AER", 4100),
    ("Сургут", "SGC", 1540),
    ("Калининград", "KGD", 4000),
    ("Санкт-Петербург", "LED", 3532),
    ("Москва (Домодедово)", "DME", 2855),
    ("Казань", "KZN", 2995),
    ("Тюмень", "TJM", 2094),
    ("Омск", "OMS", 2093),
    ("Новосибирск", "OVB", 4001),
    ("Красноярск", "KJA", 4954),
    ("Владивосток", "VVO", 10543),
    ("Пермь", "PEE", 3550),
    ("Нижний Новгород", "GOJ", 2956),
]


def parse_search_form(form):
    fields = ['from', 'to', 'date']
    values = tuple(form.get(f) for f in fields)
    
    if all(values):
        return values
    else:
        return False


def parse_cookies(session):
    fields = ["number", "date", "city"]
    values = {f: session.get(f) for f in fields}

    if all(values):
        return values
    else:
        return False


def search(city):
    result = filter(lambda x: x[0] == city, flights)
    result = list(result)
    if len(result) > 0:
        return result[0]
    else:
        return tuple()


def time_strings(r):
    return [f"{x:02}" for x in r]


def coeff(hits):
    return 1 + 3**min(hits-1, 6) / 100


def build_search_results(origin, date, hits):
    random.seed(f"a seed for flight from {origin} at {date}")

    price_coeff = coeff(hits)
    base_flight = search(origin)
    if not base_flight:
        return []
    city, airport, base_price = base_flight
    
    hours = time_strings(range(0, 24))
    minutes = time_strings(range(0, 60, 5))
    
    flights = range(rint(1, 4))
    numbers = random.sample(range(100, 1000), len(flights))
    times = [f"{pick(hours)}:{pick(minutes)}" for _ in flights]
    
    prices = [int(base_price * (1 + rint(0, 100) / 100)) for _ in flights]
    if not list(filter(lambda x: x < MAX_PRICE, prices)):
        prices[rint(0, len(prices) - 1)] = MAX_PRICE - rint(1, 99)

    results = [(
        city,
        airport,
        date,
        int(prices[i] * price_coeff),
        times[i],
        numbers[i]
    ) for i in flights]

    return sorted(results, key=lambda x: int(x[4].split(':')[0]))


    
    
