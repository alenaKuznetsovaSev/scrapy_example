import scrapy
from twisted.internet.error import TimeoutError, TCPTimedOutError

import config as cfg
import scrapy_ex


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):
        self.log("in parse")
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author = quote.css('span small::text').get()
            tags = ""
            for tag in quote.css('div.tags a.tag::text').getall():
                tags += tag + ", "
            scrapy_ex.saver.add_item_content_to_sql({'table_name': self.name,
                                                     'text': text,
                                                     'author': author,
                                                     'tags': tags})
            yield {
                'text': text,
                'author': author,
                'tags': tags,
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def start_requests(self):
        for url in self.start_urls:
            _ = scrapy_ex.proxy_manager.get_random_proxy()
            self.log("before Request")
            yield scrapy.Request(url=url, callback=self.parse,
                                 headers=cfg.random_headers(),
                                 meta={_.split(':')[0]: _.split(':')[1]},
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
