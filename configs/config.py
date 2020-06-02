token = '875689477:AAH49j48TBWQkEb2Ah0gfKA56hN7A0Sk4VM'
app_name = 'MiniVanBot'

url_dollar_google = 'https://www.google.com/search?sxsrf=ALeKk03RR756WLVS2xpoVDpulrupdvUItA%3A1590978628310&ei=RGjUXpSGEvSLk74PvtiE4AI&q=dollar&oq=dolla&gs_lcp=CgZwc3ktYWIQAxgDMgQIABBDMgQIABBDMgQIABBDMgIIADIECAAQQzIECAAQQzIFCAAQywEyBAgAEEMyBAgAEEMyBAgAEEM6BAgAEEc6BAgjECdQoPUBWIr-AWD1jwJoAHADeACAAcEBiAG-BpIBAzAuNZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab'
url_dollar_cb = 'https://www.cbr-xml-daily.ru/daily_json.js'
url_border_countries = 'https://www.wanderlust.co.uk/content/coronavirus-travel-updates/'
url_aviasales = 'http://map.aviasales.ru/prices.json'
url_aviasales_search = 'https://www.aviasales.ru/search/'
url_iata_info = 'https://www.air-port-codes.com/search/results/'

headers_dollar_google = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
long_body = 9000

departure_city = ''
departure_date = ''


questions_borders = [
        'Which European countries have travel restrictions?',
        'Which European countries you can still travel to?',
        'Which North American places have travel restrictions?',
        'Which North American countries have their borders open?',
        'Which Central and South America Countries have travel restrictions?',
        'Which Asian countries have travel restrictions?',
        'Which Asian countries have their borders open?',
        'Which African countries have travel restrictions?',
        'Which African countries still have their borders open?',
        'Which South Pacific countries can you not travel to?',
        'Which Caribbean countries have travel restrictions?',
        'Which Caribbean countries still have their borders open?',
        'Can\'t wait to travel again?'
    ]

parts_world = [
    '✅✈️ Европа',
    '✅✈️ Северная Америка',
    '✅✈️ Азия',
    '✅✈️ Африка',
    '✅✈️ Карибы',

    '❌✈️️ Европа',
    '❌✈️️ Северная Америка',
    '❌✈️️ Южная Америка',
    '❌✈️️ Азия',
    '❌✈️️ Африка',
    '❌✈️️ Океания',
    '❌✈️️ Карибы'
]

departure_cities = {
    'OVB': 'Новосибирск',
    'MOW': 'Москва'
}

europe_permission = []
asia_permission = []
north_permission = []
south_permission = []