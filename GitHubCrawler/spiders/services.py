import json
from typing import List


class ConfigService:

    def get_search_keywords(self) -> List[str]:
        config = {}
        with open('input.json') as r:
            content = r.read()
            config = json.loads(content)

        return config['keywords']


class OutputUrlService:

    def save_response(self, urls: List[str]):
        raw_data = json.dumps(urls)
        with open('output.json', 'w+') as w:
            w.write(raw_data)
