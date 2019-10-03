# -*- coding: utf-8 -*-
import logging
from random import randrange

import scrapy
from scrapy import Request

logger = logging.getLogger(__name__)


class SearchRepoSpider(scrapy.Spider):
    name = 'search_repos'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/search?q=nova+css/']
    proxy_list = ['http://165.227.71.60:80', 'http://192.140.42.83:52852', 'http://182.52.238.44:37758']

    def start_requests(self):
        print('calling start requests')
        yield Request(
            url='https://github.com/search?q=nova+css',
            callback=self.parse_proxied_response,
            errback=self.parse_error,
            meta={
                # 'proxy': self.proxy_list[randrange(len(self.proxy_list))],
                'max_retry_times': 0
            }
        )

    def parse(self, response):
        print('not called through proxy')
        request = scrapy.Request('https://github.com/search?q=nova+css', callback=self.parse_proxied_response)

        yield request

    def parse_error(self, failure):
        print(f'failure: {repr(failure)}')

    def parse_proxied_response(self, response):
        print(f'called through a proxy {response.url}')

        repo_list = response.css('.repo-list')
        print(str(repo_list))
        repo_list_items = repo_list.css('.repo-list-item')
        for item in repo_list_items:
            link = item.css('a::attr(href)').extract_first()
            print(str(link))

        pass
