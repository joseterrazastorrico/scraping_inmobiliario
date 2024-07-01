from urllib.request import urlopen
from lxml import etree
import pandas as pd

url = "https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana"
response = urlopen(url)
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)
i = 1

precio_df = []
tamano_df = []
dormitorios_df = []
direccion_df = []
edificio_df = []

while True:
    precio = f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[1]/a[1]/div[1]/div/div/span/span[2]/span[2]'
    tamano = f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[1]/a[1]/div[2]/ul/li[1]'
    dormitorios = f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[1]/a[1]/div[2]/ul/li[2]'
    direccion = f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[1]/a[1]/div[5]/p[1]'
    edificio = f'/html/body/main/div/div[2]/section/ol/li[{i}]/div/div/div[1]/a[1]/div[5]/p[3]'

    try:
        precio_i = tree.xpath(precio)[0].text
        tamano_i = tree.xpath(tamano)[0].text
        dormitorios_i = tree.xpath(dormitorios)[0].text
        direccion_i = tree.xpath(direccion)[0].text
        edificio_i = tree.xpath(edificio)[0].text

        precio_df.append(precio_i)
        tamano_df.append(tamano_i)
        dormitorios_df.append(dormitorios_i)
        direccion_df.append(direccion_i)
        edificio_df.append(edificio_i)
    except:
        print(i)
        break
    i = i + 1

df = pd.DataFrame({
    'precio': precio_df,
    'tamano': tamano_df,
    'dormitorio': dormitorios_df,
    'direccion': direccion_df,
    'edificio': edificio_df
})

print(df)