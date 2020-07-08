import scrapy
from scrapy import Request
from twisted.internet.error import TimeoutError, TCPTimedOutError

import config as cfg
import scrapy_ex


class TastemadeSpider(scrapy.Spider):
    name = 'tastemade'
    start_urls = ['https://www.tastemade.com/food/']

    def parse(self, response):
        yield from response.follow_all(css='.verticalsTitle a', callback=self.get_pagination_links)

    def start_requests(self):
        for url in self.start_urls:
            proxy = scrapy_ex.proxy_manager.get_random_proxy()
            self.log("before Request")
            yield scrapy.Request(url=url, callback=self.parse,
                                 headers=cfg.random_headers(),
                                 meta={proxy.split(':')[0]: proxy.split(':')[1]},
                                 errback=self.del_bad_proxy)

    def del_bad_proxy(self, failure):
        self.log("in del bad proxy")
        if failure.check(TimeoutError, TCPTimedOutError):
            self.log("in if timeout error")
            proxy = ""
            for key in failure.meta.keys():
                proxy = key + ":" + failure.meta[key]
                break
            scrapy_ex.proxy_manager.del_proxy(proxy)

    def get_pagination_links(self, response):
        numb_last_page = response.css('ul>li.page-item.null>a::attr(href)').getall()[-1].split('/')[-1]
        for i in range(1, int(numb_last_page) + 1):
            link = '%spage/%d' % (response.url, i)
            yield response.follow(link, self.parse_one_charter)

    def parse_one_charter(self, response):
        yield from response.follow_all(css='.containerVideos>.box a', callback=self.parse_item_page)

    def parse_item_page(self, response) -> dict:
        title = response.css('h1.white ::text').get()
        ingredients = ""
        for items in response.css('.ingredients>div>ul'):
            ingredients += cfg.custom_splitter + items.css("li ::text").get()
        steps_cooking = ""
        for items in response.css('.steps>div>ol'):
            steps_cooking += cfg.custom_splitter + items.css("li ::text").get()
        photo_links = 'https:' + response.css('.image>img ::attr(src)').get()
        # example image link https://truffle-assets.imgix.net/8238b21d-l.png?auto=compress,format&fm=pjpg&w=1200
        video_link = response.css('video ::attr(src)').get()
        # example video link
        # https://renditions3-tastemade.akamaized.net/e5d6ceea-spring-rolls-sakura-petals-l/mp4/e5d6ceea-spring-rolls-sakura-petals-l-540-2000-mp4.mp4
        res = {'table_name': 'food_recipe',
               'title': title,
               'slogan': 'NULL',
               'ingredients': ingredients,
               'steps': steps_cooking,
               'photo_links': photo_links,
               'video_link': video_link,
               'home_url_id': '0'}
        scrapy_ex.saver.add_item_content_to_sql(res)
