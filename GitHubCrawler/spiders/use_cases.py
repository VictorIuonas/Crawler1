from typing import Iterator

from GitHubCrawler.spiders.entities import GitHubSearchPage


class SearchResultLinkExtractorUseCase:

    def execute(self, web_page: GitHubSearchPage) -> Iterator[str]:
        for link in web_page.get_list_of_links():
            yield f'https://github.com/{link}'


class SearchUrlGeneratorUseCase:

    def __init__(self, config_service):
        self.config_service = config_service

    def execute(self) -> str:
        return 'https://github.com/search?q=' + str.join('+', self.config_service.get_search_keywords())
