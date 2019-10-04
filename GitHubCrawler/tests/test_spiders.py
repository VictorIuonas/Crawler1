import json
from unittest.mock import MagicMock, patch, mock_open

from GitHubCrawler.spiders.SearchRepo import SearchRepoSpider


class TestSpiders:

    @patch('GitHubCrawler.spiders.services.open')
    @patch('GitHubCrawler.spiders.SearchRepo.Spider')
    def test_spider_parses_repo_page_to_return_link_list(self, spider_base, open):
        scenario = self.Scenario(spider_base, open)

        scenario.given_an_input_file_asking_for_repos()
        scenario.given_a_git_repos_search_result_page_with_a_list_of_git_repos()

        scenario.when_starting_a_request()
        scenario.when_parsing_the_search_result_page()

        scenario.then_the_request_will_contain_the_input_keywords()
        scenario.then_the_result_will_contain_the_domain_repo_url_list()

    class Scenario:
        TEST_REPO_LINKS = ['repo_link1', 'repo_link2', 'repo_link3']
        TEST_KEYWORDS = ['keyword1', 'keyword2', 'keyword3']

        def __init__(self, spider_base = MagicMock(), file_open=MagicMock()):
            self.file_open = file_open
            self.input_file_content = {}

            self.page_data = MagicMock()
            self.repo_list = []

            self.initial_request = []

            self.target = SearchRepoSpider()

            self.crawl_result = None

        def given_an_input_file_asking_for_repos(self):
            self.input_file_content = {
                "keywords": self.TEST_KEYWORDS,
                "proxies": [
                    "194.126.37.94:8080",
                    "13.78.125.167:8080"
                ],
                "type": "Repositories"
            }
            self.file_open.return_value.__enter__.return_value.read.return_value = json.dumps(self.input_file_content)

        def given_a_git_repos_search_result_page_with_a_list_of_git_repos(self):
            for link in self.TEST_REPO_LINKS:
                repo_link = MagicMock()
                repo_link.css.return_value.extract_first.return_value = link
                self.repo_list.append(repo_link)

            self.page_data.css.return_value.css.return_value = self.repo_list

        def when_starting_a_request(self):
            self.initial_request = list(self.target.start_requests())

        def when_parsing_the_search_result_page(self):
            self.target.parse_proxied_response(self.page_data)

        def then_the_request_will_contain_the_input_keywords(self):
            assert len(self.initial_request) == 1
            keyword_query_string = str.join('+', self.TEST_KEYWORDS)
            assert self.initial_request[0].url == f'https://github.com/search?q={keyword_query_string}'

        def then_the_result_will_contain_the_domain_repo_url_list(self):
            raw_result = self.file_open.return_value.__enter__.return_value.write.call_args[0][0]
            crawl_result = json.loads(raw_result)

            assert len(crawl_result) == len(self.TEST_REPO_LINKS)
            for i in range(len(self.TEST_REPO_LINKS)):
               assert crawl_result[i] == f'https://github.com/{self.TEST_REPO_LINKS[i]}'
