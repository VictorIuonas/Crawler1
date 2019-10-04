from unittest.mock import MagicMock, patch

from GitHubCrawler.spiders.SearchRepo import SearchRepoSpider


class TestSpiders:

    @patch('GitHubCrawler.spiders.SearchRepo.Spider')
    def test_spider_parses_repo_page_to_return_link_list(self, spider_base):
        scenario = self.Scenario()

        scenario.given_a_git_repos_search_result_page_with_a_list_of_git_repos()

        scenario.when_parsing_the_search_result_page()

        scenario.then_the_result_will_contain_the_domain_repo_url_list()

    class Scenario:
        TEST_REPO_LINKS = ['repo_link1', 'repo_link2', 'repo_link3']

        def __init__(self):
            self.page_data = MagicMock()
            self.repo_list = []

            self.target = SearchRepoSpider()

            self.crawl_result = None

        def given_a_git_repos_search_result_page_with_a_list_of_git_repos(self):
            for link in self.TEST_REPO_LINKS:
                repo_link = MagicMock()
                repo_link.css.return_value.extract_first.return_value = link
                self.repo_list.append(repo_link)

            self.page_data.css.return_value.css.return_value = self.repo_list

        def when_parsing_the_search_result_page(self):
            self.crawl_result = list(self.target.parse_proxied_response(self.page_data))

        def then_the_result_will_contain_the_domain_repo_url_list(self):
            assert len(self.crawl_result) == len(self.TEST_REPO_LINKS)
            for i in range(len(self.TEST_REPO_LINKS)):
                assert self.crawl_result[i] == f'https://github.com/{self.TEST_REPO_LINKS[i]}'
