from bs4 import BeautifulSoup
import urllib.request
import re
from urllib.error import URLError, HTTPError, ContentTooShortError
import pandas as pd
import time

# Crawler e Download
def download(url, user_agent='wswp', num_retries=2, charset='utf-8'):
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset(failobj=charset)
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html

def scrap_data():
    pass


def create_csv(data, columns):
    df = pd.DataFrame(columns=columns)
    df.loc[-1] = data
    df.to_csv("../Data/dados_scrapping.csv", index=False)

    

def crawl_site(url, max_errors=5):
    num_errors = 0
    pg_url = url
    html = download(pg_url)
    if html is None:
        num_errors += 1
        if num_errors == max_errors:
            print("ERROR MAX")
        else:
            num_errors = 0
    dados = re.findall('"w2p_fw">(.*?)<\/td>', html)
    for index, dado in enumerate(dados):
        if re.search("([A-Z]*.)<\/a>", dado):
            aux = re.findall("([A-Z]*.)<\/a>", dado)
            aux2 = []
            for item in aux:
                aux2.append(item.strip())
            dados[index] = aux2
    year, month, day, hour, minu = map(int, time.strftime("%Y %m %d %H %M").split())
    time_stamp = f'{day}/{month}/{year} {hour}:{minu}'
    dados.append(time_stamp)
    nome_das_colunas = re.findall('([A-Za-z]*):\s<\/label>', html)
    nome_das_colunas.append('time_stamp')
    create_csv(dados, nome_das_colunas)

crawl_site('''http://127.0.0.1:8000/places/default/view/32''') # Site do Brasil