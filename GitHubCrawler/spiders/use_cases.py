from typing import Iterator

from GitHubCrawler.spiders.entities import GitHubSearchPage


class SearchResultLinkExtractorUseCase:

    def execute(self, web_page: GitHubSearchPage) -> Iterator[str]:
        for link in web_page.get_list_of_links():
            yield f'https://github.com/{link}'
