import json
from typing import List


class ConfigService:

    def get_search_keywords(self) -> List[str]:
        config = {}
        with open('input.json') as r:
            content = r.read()
            config = json.loads(content)

        return config['keywords']
