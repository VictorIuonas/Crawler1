import abc
from typing import Iterator

from scrapy.http import Response

class GitHubSearchPage(abc.ABC):

    @abc.abstractmethod
    def get_list_of_links(self):
        pass


class ReposPage(GitHubSearchPage):

    def __init__(self, scrapped_page: Response):
        self.scrapped_page = scrapped_page

    def get_list_of_links(self) -> Iterator[str]:
        repo_list = self.scrapped_page.css('.repo-list')
        repo_list_items = repo_list.css('.repo-list-item')
        for item in repo_list_items:
            link = item.css('a::attr(href)').extract_first()
            print(str(link))
            yield link

