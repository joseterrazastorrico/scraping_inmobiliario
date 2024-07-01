import requests
from bs4 import BeautifulSoup

status = 'venta'
inmueble = 'departamento'
comuna = 'las-condes'
region = 'metropolitana'
base_url = f"https://www.portalinmobiliario.com/{status}/{inmueble}/{comuna}-{region}"

def get_page_content(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def extract_info(card):
    link = card.find('a')['href']
    price = card.find('div', class_="ui-search-price__second-line ui-search-price__second-line--decimal").text
    attributes = card.select('li', class_="ui-search-card-attributes__attribute")
    dormitorios = attributes[0].text
    banos = attributes[1].text
    m2 = attributes[2].text
    return {
        'link': link,
        'price': price,
        'dormitorios': dormitorios,
        'banos': banos,
        'm2': m2,
    }

def scrape_all_pages(base_url):
    current_page = 1
    all_listings = []

    while True:
        soup = get_page_content(f"{base_url}_Desde_{(current_page-1)*50}")
        cards = soup.select('ol > li > div.ui-search-result__wrapper')
        if not cards:
            break
        for card in cards:
            try:
                all_listings.append(extract_info(card))
            except:
                pass
        current_page += 1

    return all_listings

listings = scrape_all_pages(base_url)
for listing in listings:
    print(listing)

