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
        scenario.when_parsing_the_repo_search_result_page()

        scenario.then_the_request_will_contain_the_input_keywords()
        scenario.then_the_result_will_contain_the_domain_repo_url_list()

    @patch('GitHubCrawler.spiders.services.open')
    @patch('GitHubCrawler.spiders.SearchRepo.Spider')
    def test_spider_parses_wiki_page_to_return_link_list(self, spider_base, open):
        scenario = self.Scenario(spider_base, open)

        scenario.given_an_input_file_asking_for_wikis()
        scenario.given_a_git_repos_search_result_page_with_a_link_to_wikis_results()

        scenario.when_starting_a_request()
        scenario.when_parsing_the_repo_search_result_page()

        scenario.then_the_request_will_contain_the_input_keywords()
        scenario.then_the_parse_result_will_redirect_to_the_wiki_result_page()

        scenario.given_a_git_wikis_search_result_page_with_a_list_of_git_wikis()

        scenario.when_parsing_the_wiki_search_result_page()
        scenario.then_the_result_will_contain_the_domain_wiki_url_list()

    @patch('GitHubCrawler.spiders.services.open')
    @patch('GitHubCrawler.spiders.SearchRepo.Spider')
    def test_spider_parses_issues_page_to_return_issues_list(self, spider_base, open):
        scenario = self.Scenario(spider_base, open)

        scenario.given_an_input_file_asking_for_issues()
        scenario.given_a_git_repos_search_result_page_with_a_link_to_issues_results()

        scenario.when_starting_a_request()
        scenario.when_parsing_the_repo_search_result_page()

        scenario.then_the_request_will_contain_the_input_keywords()
        scenario.then_the_parse_result_will_redirect_to_the_issue_result_page()

        scenario.given_a_git_issues_search_result_page_with_a_list_of_git_issues()

        scenario.when_parsing_the_issue_search_result_page()
        scenario.then_the_result_will_contain_the_domain_issues_url_list()

    class Scenario:
        TEST_REPO_LINKS = ['repo_link1', 'repo_link2', 'repo_link3']
        TEST_WIKIS_LINKS = ['wiki_link1', 'wiki_link2', 'wiki_link3']
        TEST_ISSUES_LINKS = ['issue_link1', 'issue_link2', 'issue_link3']
        TEST_KEYWORDS = ['keyword1', 'keyword2', 'keyword3']
        TEST_LINK_TO_WIKIS = '/a_random_partial_link_to_the_wiki_search_result'
        TEST_LINK_TO_ISSUES = '/a_random_partial_link_to_the_issues_search_result'

        def __init__(self, spider_base = MagicMock(), file_open=MagicMock()):
            self.file_open = file_open
            self.input_file_content = {}

            self.page_data = MagicMock()
            self.search_result_list = []

            self.initial_request = []
            self.requests_from_first_page = []

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

        def given_an_input_file_asking_for_wikis(self):
            self.input_file_content = {
                "keywords": self.TEST_KEYWORDS,
                "proxies": [
                    "194.126.37.94:8080",
                    "13.78.125.167:8080"
                ],
                "type": "Wikis"
            }
            self.file_open.return_value.__enter__.return_value.read.return_value = json.dumps(self.input_file_content)

        def given_an_input_file_asking_for_issues(self):
            self.input_file_content = {
                "keywords": self.TEST_KEYWORDS,
                "proxies": [
                    "194.126.37.94:8080",
                    "13.78.125.167:8080"
                ],
                "type": "Issues"
            }
            self.file_open.return_value.__enter__.return_value.read.return_value = json.dumps(self.input_file_content)

        def given_a_git_repos_search_result_page_with_a_list_of_git_repos(self):
            for link in self.TEST_REPO_LINKS:
                repo_link = MagicMock()
                repo_link.css.return_value.extract_first.return_value = link
                self.search_result_list.append(repo_link)

            self.page_data.css.side_effect = None
            self.page_data.css.return_value.css.return_value = self.search_result_list

        def given_a_git_wikis_search_result_page_with_a_list_of_git_wikis(self):
            self.page_data.css.return_value = MagicMock()
            for link in self.TEST_WIKIS_LINKS:
                wiki_link = MagicMock()
                wiki_link.css.return_value.extract_first.return_value = link
                self.search_result_list.append(wiki_link)

            self.page_data.css.return_value.css.return_value = self.search_result_list

        def given_a_git_issues_search_result_page_with_a_list_of_git_issues(self):
            self.page_data.css.return_value = MagicMock()
            for link in self.TEST_ISSUES_LINKS:
                wiki_link = MagicMock()
                wiki_link.css.return_value.extract_first.return_value = link
                self.search_result_list.append(wiki_link)

            self.page_data.css.return_value.css.return_value.css.return_value = self.search_result_list

        def given_a_git_repos_search_result_page_with_a_link_to_wikis_results(self):
            self.page_data.css.return_value.xpath.return_value.extract_first.return_value = self.TEST_LINK_TO_WIKIS

        def given_a_git_repos_search_result_page_with_a_link_to_issues_results(self):
            self.page_data.css.return_value.xpath.return_value.extract_first.return_value = self.TEST_LINK_TO_ISSUES

        def when_starting_a_request(self):
            self.initial_request = list(self.target.start_requests())

        def when_parsing_the_repo_search_result_page(self):
            redirects = self.target.parse_repo_search_results(self.page_data)
            self.requests_from_first_page = list(redirects) if redirects else []

        def when_parsing_the_wiki_search_result_page(self):
            redirects = self.target.parse_wikis_search_result(self.page_data)
            self.requests_from_first_page = list(redirects) if redirects else []

        def when_parsing_the_issue_search_result_page(self):
            redirects = self.target.parse_issues_search_result(self.page_data)
            self.requests_from_first_page = list(redirects) if redirects else []

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

        def then_the_result_will_contain_the_domain_wiki_url_list(self):
            raw_result = self.file_open.return_value.__enter__.return_value.write.call_args[0][0]
            crawl_result = json.loads(raw_result)

            assert len(crawl_result) == len(self.TEST_WIKIS_LINKS)
            for i in range(len(self.TEST_WIKIS_LINKS)):
               assert crawl_result[i] == f'https://github.com/{self.TEST_WIKIS_LINKS[i]}'

        def then_the_result_will_contain_the_domain_issues_url_list(self):
            raw_result = self.file_open.return_value.__enter__.return_value.write.call_args[0][0]
            crawl_result = json.loads(raw_result)

            assert len(crawl_result) == len(self.TEST_ISSUES_LINKS)
            for i in range(len(self.TEST_ISSUES_LINKS)):
               assert crawl_result[i] == f'https://github.com/{self.TEST_ISSUES_LINKS[i]}'

        def then_the_parse_result_will_redirect_to_the_wiki_result_page(self):
            assert len(self.requests_from_first_page) == 1
            assert self.requests_from_first_page[0].url == f'https://github.com{self.TEST_LINK_TO_WIKIS}'

        def then_the_parse_result_will_redirect_to_the_issue_result_page(self):
            assert len(self.requests_from_first_page) == 1
            assert self.requests_from_first_page[0].url == f'https://github.com{self.TEST_LINK_TO_ISSUES}'
