import abc
from enum import Enum
from typing import Iterator

from scrapy.http import Response


class ResultPageType(Enum):
    Repos = 0,
    Wikis = 1,
    Issues = 2


class GitHubSearchPage(abc.ABC):

    def __init__(self, scrapped_page: Response):
        self.scrapped_page = scrapped_page

    @abc.abstractmethod
    def get_list_of_links(self) -> Iterator[str]:
        pass

    def get_wikis_link(self) -> str:
        link_value = self.scrapped_page.css('span[data-search-type="Wikis"]').xpath('../@href').extract_first()

        return link_value

    def get_issues_link(self) -> str:
        link_value = self.scrapped_page.css('span[data-search-type="Issues"]').xpath('../@href').extract_first()

        return link_value

    def get_repos_link(self) -> str:
        link_value = self.scrapped_page.css('span[data-search-type="Repositories"]').xpath('../@href').extract_first()

        return link_value

class ReposPage(GitHubSearchPage):

    def get_list_of_links(self) -> Iterator[str]:
        repo_list = self.scrapped_page.css('.repo-list')
        repo_list_items = repo_list.css('.repo-list-item')
        for item in repo_list_items:
            link = item.css('a::attr(href)').extract_first()
            print(str(link))
            yield link


class WikisPage(GitHubSearchPage):

    def get_list_of_links(self) -> Iterator[str]:
        wikis_links = self.scrapped_page.css('#wiki_search_results').css('.h5')
        for link_component in wikis_links:
            link = link_component.css('::attr(href)').extract_first()
            print(link)
            yield link


class IssuesPage(GitHubSearchPage):

    def get_list_of_links(self) -> Iterator[str]:
        issuess_links = self.scrapped_page.css('.issue-list').css('h3').css('a')
        for link_component in issuess_links:
            link = link_component.css('::attr(href)').extract_first()
            print(link)
            yield link
