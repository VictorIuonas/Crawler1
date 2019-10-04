# -*- coding: utf-8 -*-
import json
import logging
from random import randrange

from scrapy import Request, Spider

from GitHubCrawler.spiders.entities import ReposPage
from GitHubCrawler.spiders.factories import build_git_search_result_extractor_use_case, build_search_url_generator

logger = logging.getLogger(__name__)


class SearchRepoSpider(Spider):
    name = 'search_repos'
    allowed_domains = ['github.com']
    start_urls = ['file:///home/victor/Workspace/Python/data/RedPoint/GitHubSearchRepos.html']
    # start_urls = ['https://github.com/search?q=']
    proxy_list = ['http://165.227.71.60:80', 'http://192.140.42.83:52852', 'http://182.52.238.44:37758']

    def start_requests(self):
        print('calling start requests')

        url_generator = build_search_url_generator()

        yield Request(
            url=url_generator.execute(),
            callback=self.parse_proxied_response,
            errback=self.parse_error,
            meta={
                # 'proxy': self.proxy_list[randrange(len(self.proxy_list))],
                'max_retry_times': 0
            }
        )

    def parse(self, response):
        print('not called through proxy')
        request = Request('https://github.com/search?q=nova+css', callback=self.parse_proxied_response)

        yield request

    def parse_error(self, failure):
        print(f'failure: {repr(failure)}')

    def parse_proxied_response(self, response):
        print(f'called through a proxy {response.url}')
        use_case = build_git_search_result_extractor_use_case()
        result = use_case.execute(ReposPage(response))

        return result
