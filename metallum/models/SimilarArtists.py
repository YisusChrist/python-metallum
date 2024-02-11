from pyquery import PyQuery

from metallum.models.Metallum import Metallum


class SimilarArtists(Metallum, list):
    """Entries in the similar artists tab"""

    def __init__(self, url, result_handler):
        super().__init__(url)
        data = self._content

        links_list = PyQuery(data)("a")
        values_list = PyQuery(data)("tr")

        # assert(len(links_list) == len(values_list) - 1)
        for i in range(0, len(links_list) - 1):
            details = [links_list[i].attrib.get("href")]
            details.extend(values_list[i + 1].text_content().split("\n")[1:-1])
            self.append(result_handler(details))
            self.result_count = i

    def __repr__(self):

        def similar_artist_str(SimilarArtistsResult):
            return f"{SimilarArtistsResult.name} ({SimilarArtistsResult.score})"

        if not self:
            return "<SimilarArtists: None>"
        names = list(map(similar_artist_str, self))
        s = " | ".join(names)
        return "<SimilarArtists: {0}>".format(s)
