import pandas as pd
import numpy as np
from utils import parameters as p

def preprocess_data(data):
    data['unidad'] = np.where(data['price'].str[:2].isin(['UF', 'US']), data['price'].str[:2], '$')
    data['price_clean'] = data.apply(lambda x: x.price.replace(x.unidad, '').replace('.', '').replace('$', ''), axis=1)
    data['price_clean'] = data['price_clean'].astype('int')
    data['proyecto'] = data['m2'].str.contains('[0-9]+ a [0-9]+', regex=True) | data['dormitorios'].str.contains('[0-9]+ a [0-9]+', regex=True) | data['banos'].str.contains('[0-9]+ a [0-9]+', regex=True)
    data['dormitorios_clean'] = pd.to_numeric(np.where(data['proyecto'] == True, np.nan, data['dormitorios'].str.replace(' dormitorios*', '', regex=True)))
    data['banos_clean'] = pd.to_numeric(np.where(data['proyecto'] == True, np.nan, data['banos'].str.replace(' baños*', '', regex=True)))
    data['m2_clean'] = pd.to_numeric(np.where(data['proyecto'] == True, np.nan, data['m2'].str.replace(' m² útiles', '').str.extract('(\d+)')[0]))
    
    data['price_clean_uf'] = np.where(data['proyecto'] == False,
                                    np.where(data['unidad'] == '$',
                                            data['price_clean'] / p.VALUE_UF_TO_CLP,
                                            np.where(data['unidad'] == 'US',
                                                data['price_clean'] * p.VALUE_USD_TO_CLP / p.VALUE_UF_TO_CLP,
                                                data['price_clean'])),
                                    np.nan)

    return data
