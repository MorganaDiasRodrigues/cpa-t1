# def para realizar em todos os sites
def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each link
    for link in links:
        html = download(link)
        soup = BeautifulSoup(html, "html5lib")
        print(html)
        
        #info_complete = soup.find_all("td")
        
#crawl_sitemap('''http://127.0.0.1:8000/places/default/sitemap.xml''')


# Modularizar código do main.py?

# from bs4 import BeautifulSoup
# import urllib.request
# import re
# from urllib.error import URLError, HTTPError, ContentTooShortError
# import pandas as pd
# import time

# # Crawler e Download
# def download(url, user_agent='wswp', num_retries=2, charset='utf-8'):
#     print('Downloading:', url)
#     request = urllib.request.Request(url)
#     request.add_header('User-agent', user_agent)
#     try:
#         resp = urllib.request.urlopen(request)
#         cs = resp.headers.get_content_charset(failobj=charset)
#         html = resp.read().decode(cs)
#     except (URLError, HTTPError, ContentTooShortError) as e:
#         print('Download error:', e.reason)
#         html = None
#         if num_retries > 0:
#             if hasattr(e, 'code') and 500 <= e.code < 600:
#                 # recursively retry 5xx HTTP errors
#                 return download(url, num_retries - 1)
#     return html

# def scrap_data(regex_string, html):
#     scraped_data = re.findall(regex_string, html)
#     return scraped_data

# def scrap_href_data(regex_string, data):
#     for index, dado in enumerate(data):
#         if re.search(regex_string, data):
#             aux = re.findall("([A-Z]*.)<\/a>", dado)
#             aux2 = []
#             for item in aux:
#                 aux2.append(item.strip())
#             data[index] = aux2
#     return data

# def scrap_name_for_columns(regex_string, html):
#     return re.findall(regex_string, html)

# def time_stamp():
#     year, month, day, hour, minu = map(int, time.strftime("%Y %m %d %H %M").split())
#     time_stamp = f'{day}/{month}/{year} {hour}:{minu}'
#     return time_stamp

# def create_csv(data, columns):
#     df = pd.DataFrame(columns=columns)
#     df.loc[-1] = data
#     df.to_csv("../Data/dados_scrapping.csv", index=False)



# def crawl_site(url, max_errors=5):
#     num_errors = 0
#     pg_url = url
#     html = download(pg_url)
#     if html is None:
#         num_errors += 1
#         if num_errors == max_errors:
#             print("ERROR MAX")
#         else:
#             num_errors = 0
#     data = scrap_data('"w2p_fw">(.*?)<\/td>', html)
#     data = scrap_href_data('([A-Z]*.)<\/a>', data)
#     data.append(time_stamp())
#     nome_das_colunas = scrap_name_for_columns('([A-Z]*.)<\/a>', html)
#     nome_das_colunas.append('time_stamp')
#     create_csv(data, nome_das_colunas)

# crawl_site('''http://127.0.0.1:8000/places/default/view/32''') # Site do Brasil