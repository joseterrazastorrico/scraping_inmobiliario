import pandas as pd
import numpy as np
import argparse
from utils.scraperinmobiliarios import ScraperInmbobiliario
from utils import utils as ut
from utils import parameters as p

status = 'venta'
inmueble = 'departamento'
region= 'metropolitana'

def main():
    comunas_failed = []
    for comuna in p.COMUNAS[region]:

        scraper = ScraperInmbobiliario(status=status, inmueble=inmueble, comuna=comuna, region=region)

        page_id = 1
        results = []
        while True:
            print(f'page {page_id}')
            result_page = scraper.scrape_page(page_id)
            results += result_page
            if len(result_page) == 0:
                break
            page_id += 1

        data = pd.DataFrame(results)
        try:
            data = ut.preprocess_data(data)
        except:
            comunas_failed.append(comuna)
        data.to_excel(f'../data/Propiedades_{status}_{inmueble}_{comuna}.xlsx')