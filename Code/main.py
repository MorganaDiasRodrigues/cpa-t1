# %%
from bs4 import BeautifulSoup
import urllib.request
import re
from urllib.error import URLError, HTTPError, ContentTooShortError
import pandas as pd
import time
import datetime
import hashlib

# %%
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

# %%
# auxiliary functions
def insert_csv(data, columns, first):
    if first: #create csv
        df = pd.DataFrame(columns=columns)
        df.loc[-1] = data
        df.to_csv("../Data/dados_scrapping.csv", index=False)
    else: # update csv (read, write, save) nao eh otimizado
        df = pd.read_csv("../Data/dados_scrapping.csv")
        df.loc[-1] = data
        df.to_csv("../Data/dados_scrapping.csv", index=False)

def save_html(html, name):
    file_name = f'..\Data\htmls\{str(name)}.html'
    f = open(file_name, 'w')
    f.write(html)
    f.close()


# %%
# searches html tags and extracts data,
# also appends time stamp from html download
def scrap_data(html, time_stamp):
    dados = re.findall('"w2p_fw">(.*?)<\/td>', html) # gets all raw data
    for i, dado in enumerate(dados):
        if re.search("([A-Z]*.)<\/a>", dado):
            aux = re.findall("([A-Z]*.)<\/a>", dado)
            aux2 = []
            for item in aux:
                aux2.append(item.strip())
            dados[i] = aux2
    dados.append(time_stamp)
    return dados

# %%
def crawl_sitemap(url, max_errors=5):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    
    for index, link in enumerate(links):
        #download html of each country
        html = download(link)

        # get time-stamp        
        year, month, day, hour, minu = map(int, time.strftime("%Y %m %d %H %M").split())
        time_stamp = f'{day}/{month}/{year} {hour}:{minu}'

        if html is None:
            num_errors += 1
            if num_errors == max_errors:
                print("ERROR MAX")
                break
        else:
            num_errors = 0

            save_html(html, index)
            dados = scrap_data(html, time_stamp)           

            if index == 0: #first interation -> has to get column names for csv
                nome_das_colunas = re.findall('([A-Za-z]*):\s<\/label>', html)
                nome_das_colunas.append('time_stamp')
                insert_csv(dados, nome_das_colunas, True)
            else:
                insert_csv(dados, None, False)



# %%
# monitors web pages: compares hash generated from saved html with "new" html hash
# if it is not a match, then update html and csv file 
def monitoring_page(url):
    
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    while True: #monitora eternamente
        # check each link
        for index, link in enumerate(links):
            f = open(f'..\Data\htmls\{str(index)}.html', 'r', encoding='utf-8')
            previousHtml = f.read() 
            previousHash = hashlib.sha224(previousHtml.encode('utf-8')).hexdigest()#gets hash from file thats already "stored"

            currentHtml = download(link)
            currentHash = hashlib.sha224(currentHtml.encode('utf-8')).hexdigest()
            # get time-stamp (in case there is an update) 
            year, month, day, hour, minu = map(int, time.strftime("%Y %m %d %H %M").split())
            time_stamp = f'{day}/{month}/{year} {hour}:{minu}'

            if previousHash != currentHash: #page has been updated
                # updating stored html
                save_html(currentHtml, index)
                dados = scrap_data(currentHtml, time_stamp)
                # updating csv
                df = pd.read_csv("..\Data\dados_scrapping.csv")
                df.iloc[index] = dados 
                df.to_csv("..\Data\dados_scrapping.csv", index=False)
                
        
# %%
# TAREFA 1, ITENS 1 E 2
crawl_sitemap('''http://127.0.0.1:8000/places/default/sitemap.xml''')
# %%
# TAREFA 1, ITEM 3
monitoring_page('''http://127.0.0.1:8000/places/default/sitemap.xml''')
        
# %%
