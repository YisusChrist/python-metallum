"""Search model for the Metallum class."""

import json

from metallum.models.metallum import Metallum


class Search(Metallum, list):
    """Represents a search result"""

    def __init__(self, url, result_handler):
        super().__init__(url)

        data = json.loads(self._content)
        results = data["aaData"]
        for result in results:
            self.append(result_handler(result))

        self.result_count = int(data["iTotalRecords"])
