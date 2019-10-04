from typing import Iterator

from GitHubCrawler.spiders.entities import GitHubSearchPage


class SearchResultLinkExtractorUseCase:

    def __init__(self, output_service):
        self.output_service = output_service

    def execute(self, web_page: GitHubSearchPage):
        result = []
        for link in web_page.get_list_of_links():
            result.append(f'https://github.com/{link}')

        self.output_service.save_response(result)


class SearchUrlGeneratorUseCase:

    def __init__(self, config_service):
        self.config_service = config_service

    def execute(self) -> str:
        return 'https://github.com/search?q=' + str.join('+', self.config_service.get_search_keywords())
