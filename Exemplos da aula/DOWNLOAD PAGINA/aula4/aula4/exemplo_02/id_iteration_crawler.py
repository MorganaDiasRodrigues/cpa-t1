# %%
import itertools
import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError

# %%


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


def crawl_site(url, max_errors=5, num_pages=1):
    num_errors = 0
    for page in range(1, num_pages+1):
        pg_url = f'{url}{page}'
        html = download(pg_url)
        if html is None:
            num_errors += 1
            if num_errors == max_errors:
                # reached max number of errors, so exit
                break
        else:
            num_errors = 0
            # success - can scrape the result
            print(html)


# %%
crawl_site('''http://192.168.1.103:8000/places/default/view/''',
           num_pages=100)
