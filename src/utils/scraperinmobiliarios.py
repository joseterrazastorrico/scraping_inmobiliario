import requests
from bs4 import BeautifulSoup

class ScraperInmbobiliario:
    def __init__(self, status='venta', inmueble='departamento',
                 comuna='Las Condes', region='metropolitana') -> None:
        base_url = "https://www.portalinmobiliario.com/{status}/{inmueble}/{comuna}-{region}"
        comuna = '-'.join(comuna.lower().split(' '))
        self.url = base_url.format(status=status, inmueble=inmueble, comuna=comuna, region=region)

    def get_page_content(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')

    def extract_info(self, card):
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

    def scrape_page(self, page):
        results = []
        soup = self.get_page_content(f"{self.url}_Desde_{(page-1)*50}")
        cards = soup.select('ol > li > div.ui-search-result__wrapper')
        for card in cards:
            try:
                results.append(self.extract_info(card))
            except:
                pass
        return results
