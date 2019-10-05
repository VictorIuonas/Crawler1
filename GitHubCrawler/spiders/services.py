import json
from typing import List

from GitHubCrawler.spiders.entities import ResultPageType


class ConfigService:
    result_page_type_converter = {
        'wikis': ResultPageType.Wikis,
        'issues': ResultPageType.Issues,
        'repositories': ResultPageType.Repos
    }

    def __init__(self):
        self.config = {}
        with open('input.json') as r:
            content = r.read()
            self.config = json.loads(content)

    def get_search_keywords(self) -> List[str]:
        return self.config['keywords']

    def get_search_result_type(self) -> ResultPageType:
        return self.result_page_type_converter[self.config['type'].lower()]


class OutputUrlService:

    def save_response(self, urls: List[str]):
        raw_data = json.dumps(urls)
        with open('output.json', 'w+') as w:
            w.write(raw_data)
