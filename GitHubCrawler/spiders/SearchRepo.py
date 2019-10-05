# -*- coding: utf-8 -*-
import logging

from scrapy import Request, Spider

from GitHubCrawler.spiders.entities import ReposPage, ResultPageType, WikisPage, IssuesPage
from GitHubCrawler.spiders.factories import build_git_search_result_extractor_use_case, build_search_url_generator, \
    build_redirect_link_extractor_use_case

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
            callback=self.parse_repo_search_results,
            errback=self.parse_error,
            meta={
                # 'proxy': self.proxy_list[randrange(len(self.proxy_list))],
                'max_retry_times': 0
            }
        )

    def parse(self, response):
        print('not called through proxy')
        request = Request('https://github.com/search?q=nova+css', callback=self.parse_repo_search_results)

        yield request

    def parse_error(self, failure):
        print(f'failure: {repr(failure)}')

    def parse_repo_search_results(self, response):
        print(f'response for github repos search results {response.url}')

        redirect_link_extractor = build_redirect_link_extractor_use_case()
        redirect_link, target_page = redirect_link_extractor.execute(ReposPage(response), ResultPageType.Repos)

        if target_page == ResultPageType.Wikis:
            yield Request(url=redirect_link, callback=self.parse_wikis_search_result, meta={
                'max_retries_times': 0
            })
        elif target_page == ResultPageType.Issues:
            yield Request(url=redirect_link, callback=self.parse_issues_search_result, meta={
                'max_retries_times': 0
            })
        else:
            link_extractor = build_git_search_result_extractor_use_case()
            link_extractor.execute(ReposPage(response))

    def parse_wikis_search_result(self, response):
        print(f'response for github wikis search results {response.url}')

        link_extractor = build_git_search_result_extractor_use_case()
        link_extractor.execute(WikisPage(response))

    def parse_issues_search_result(self, response):
        print(f'response for github wikis search results {response.url}')

        link_extractor = build_git_search_result_extractor_use_case()
        link_extractor.execute(IssuesPage(response))
