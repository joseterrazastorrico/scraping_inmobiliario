import pandas as pd
import numpy as np
import argparse
from utils.scraperinmobiliarios import ScraperInmbobiliario
from utils import utils as ut
from utils import parameters as p

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='Scraping properties',
                        description='This program extract information about properties from a portal web',
                        )

    parser.add_argument('-s', '--status', default='venta', help='options: [venta, arriendo]', action='store_true')
    parser.add_argument('-p', '--property', default='departamento', help='options: [casa, departamento]', action='store_true')
    parser.add_argument('-r', '--region', default='region', help='region from Chile', action='store_true')
    args = parser.parse_args()
    status = args.status
    property = args.property
    region= args.region
    comunas_failed = []
    for comuna in p.COMUNAS[region]:

        scraper = ScraperInmbobiliario(status=status, property=property, comuna=comuna, region=region)

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
        data.to_excel(f'../data/Propiedades_{status}_{property}_{comuna}.xlsx')