from typing import Tuple

from GitHubCrawler.spiders.entities import GitHubSearchPage, ResultPageType


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


class RedirectLinkExtractorUseCase:

    def __init__(self, config_service):
        self.config_service = config_service

    def execute(
            self, web_page: GitHubSearchPage, current_page_type: ResultPageType
    ) -> Tuple[str, ResultPageType]:
        target_page_type = self.config_service.get_search_result_type()

        if target_page_type == ResultPageType.Wikis:
            return ('https://github.com' + web_page.get_wikis_link(), target_page_type)
        if target_page_type == ResultPageType.Issues:
            return ('https://github.com' + web_page.get_issues_link(), target_page_type)

        return ('https://github.com' + web_page.get_repos_link(), target_page_type)
