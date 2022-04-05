from attr import attr
import pandas as pd
import requests
import csv
from bs4 import BeautifulSoup

# Dirección de la página web
url = "https://www.contraloria.cl/web/cgr/base-de-datos-municipales"

# Ejecutar GET-Request
response = requests.get(url)

# Analizar sintácticamente el archivo HTML de BeautifulSoup del texto fuente
html = BeautifulSoup(response.text, 'html.parser')

html

# Extraer todas las citas y autores del archivo HTML
tabcontent_html = html.find_all('div', class_ = 'tabcontent')
tabcontent_html.select('a')

url_data = []

for i in tabcontent_html:
    tmp = i.select('a')
    print(tmp.get('href'))
    