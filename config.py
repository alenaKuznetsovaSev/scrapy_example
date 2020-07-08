from random import choice


dbconfig= {'host': '127.0.0.1',
           'user': 'vsearch',
           'password': 'Vsearchpasswd1!',
           'database': 'vsearchlogDB', }

url_for_test_proxy = 'https://2ip.ru'

thread_pool_workers = 50

custom_splitter = 'MyCuStOmSpLiTer'

LOG_FILE = "my_log/my_app_log"


def random_headers() -> {}:
    """create one random http header"""
    agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0', ]

    accept = ['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*',
              'text/html,application/xhtml+xml,application/xml;q=0.9,image/png,image/*;q=0.8,*/*;q=0.5',
              '', ]

    accept_encoding = ['gzip',
                       'gzip,compress,br',
                       'br;q=1.0, gzip;q=0.8, *;q=0.1',
                       '*',
                       'gzip;q=1.0, identity; q=0.5, *;q=0', ]

    accept_language = ['ru, en-gb',
                       'en-gb',
                       'it, en-gb',
                       'ua, en-gb',
                       'de, en-gb;q=0.8',
                       'en', ]

    return {'User-Agent': choice(agents),
            'Accept': choice(accept),
            'Accept-Encoding': choice(accept_encoding),
            'Accept-Language': choice(accept_language), }