import config as cfg
from concurrent.futures import ThreadPoolExecutor
import datetime
import requests
from bs4 import BeautifulSoup
from random import choice
import my_log


class ProxyManager:

    def __init__(self):
        self.url_for_test_proxy = cfg.url_for_test_proxy
        self.headers = cfg.random_headers()
        self.thread_pool = ThreadPoolExecutor(max_workers=cfg.thread_pool_workers)
        self.proxy_options = {}
        self.proxies = []
        self.my_log = my_log.get_logger(__name__)

    def get_proxies(self) -> 'list of proxies':
        """отдает список живых прокси,
         если в списке proxies пусто - трясет новый список."""
        if self.proxies:
            return self.proxies

        while not self.proxies:
            self.my_log.debug('в списке proxies[] нет живых. Запрашиваю новый список.')
            self.update_proxies()
        return self.proxies

    def get_random_proxy(self) -> 'proxy':
        """возвращает один случайный прокси из списка proxies вида 123.234.023.12:8080"""
        proxy = choice(self.get_proxies())
        return proxy

    def update_proxies(self) -> None:
        """обновляет статусы прокси, заново ища и тестируя их, оставляет в списке только живые"""
        self.my_log.debug('start update_proxies')
        if self.proxy_options == {}:
            self.update_proxies_pretenders()
        self.refresh_proxies_status()
        self.proxies = [proxy for proxy, options in self.proxy_options.items() if options.get('alive')]
        self.proxy_options = {proxy: options for proxy, options in self.proxy_options.items() if options.get('alive')}
        self.my_log.debug('update_proxies done %d alive proxies' % len(self.proxies))

    def update_proxies_pretenders(self):
        """перезаписывает список proxies для тестирования на пригодность"""
        self.my_log.debug('start update_proxies_pretenders')
        try:
            proxy_options = {}
            # sources of proxy list: https://www.free-proxy-list.net/  https://www.socks-proxy.net/
            response = requests.get('https://www.free-proxy-list.net/', headers=self.headers, timeout=(9, 27))

            soup = BeautifulSoup(response.text, 'html.parser')
            proxy_list = soup.select('table#proxylisttable tr')
            for p in proxy_list:
                info = p.find_all('td')
                if len(info):
                    proxy = ':'.join([info[0].text, info[1].text])
                    proxy_options.update({proxy: {'country_code': info[2].text,
                                            'country': info[3].text,
                                            'privacy': info[4].text,
                                            'last_checked': None,
                                            'alive': True,
                                            'detected_ip': 'Not checked yet',
                                            'response_headers': 'Not checked yet'}})
            self.proxy_options = proxy_options
            if not proxy_options:
                self.my_log.warn('get no proxies in update_proxies_pretenders')
                self.my_log.warn('bad header - %s' % self.headers)
                self.my_log.debug('update headers')
                self.headers = cfg.random_headers()
                self.my_log.debug('call update_proxies_pretenders again')
                self.update_proxies_pretenders()
            else:
                self.my_log.debug('useful headers - %s' % self.headers)
        except Exception as e:
            self.my_log.error('Unable to update proxy list, exception : {}'.format(e))
        self.my_log.debug('update_proxies_pretenders done %d' % len(self.proxy_options))

    def refresh_proxies_status(self) -> 'proxies dict':
        """многопоточно тестирует proxy на пригодность о тестовый url(см.конфиг), возвращает список словарей
        proxies, где key - это прокси вида '123.23.167.10:80', а values - словарь опций info
        тем прокси, которые не прошли тестирования выставляет в ключ 'alive' - False"""
        self.my_log.debug('start refresh_proxies_status')

        def __check_proxy_status(proxy, info):
            info['last_checked'] = datetime.datetime.now()
            try:
                headers = cfg.random_headers()
                resp = requests.get(self.url_for_test_proxy,
                                    proxies={'proxyType': 'manual',
                                             'https': proxy,
                                             'socksProxy': proxy,
                                             'socksVersion': 4}, headers=headers, timeout=(4, 8))
                # timeout 4 sec - connect, 8-response
                info['response_headers'] = resp.headers
                info['detected_ip'] = 'Nice!!!'
                resp.raise_for_status()
            except Exception as e:
                info['alive'] = False
                info['response_headers'] = e
                info['detected_ip'] = 'Error!!! Have not response server!'
            else:
                info['alive'] = True
            return {proxy: info}
        with self.thread_pool as tp:
            try:
                results = [tp.submit(__check_proxy_status, k, v) for k, v in self.proxy_options.items()]
            except Exception as ex:
                print(ex)
        for res in results:
            result = res.result()
            self.proxy_options.update(result)
        self.my_log.debug('refresh_proxies_status done %d' % len(self.proxy_options))

    def del_proxy(self, proxy) -> None:
        """удаляет proxy из списка proxies, если список опустел, запрашивает его наполнение"""
        self.my_log.debug('del proxy - %s' % proxy)
        self.proxies.remove(proxy)
        self.proxy_options.pop(proxy)
        if not self.proxies:
            self.get_proxies()
