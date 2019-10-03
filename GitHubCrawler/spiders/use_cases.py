from typing import Iterator

from GitHubCrawler.spiders.entities import GitHubSearchPage


class SearchResultLinkExtractorUseCase:

    def execute(self, web_page: GitHubSearchPage) -> Iterator[str]:
        return web_page.get_list_of_links()
