import re
from typing import List

from pyquery import PyQuery

from metallum.models import Album, AlbumWrapper, Band
from metallum.models.Lyrics import Lyrics
from metallum.models.Metallum import Metallum
from metallum.utils import split_genres


class SearchResult(list):
    """Represents a search result in an advanced search"""

    _resultType = None

    def __init__(self, details):
        super().__init__()
        for detail in details:
            if re.match("^<a href.*", detail):
                lyrics_link = re.search('id="lyricsLink_(\d+)"', detail)
                if lyrics_link is not None:
                    self.append(lyrics_link[1])
                else:
                    d = PyQuery(detail)
                    self.append(d("a").text())
            else:
                self.append(detail)

    def __repr__(self):
        s = " | ".join(self)
        return "<SearchResult: {0}>".format(s)

    def get(self) -> "Metallum":
        return self._resultType(self.url)


class BandResult(SearchResult):

    def __init__(self, details):
        super().__init__(details)
        self._details = details
        self._resultType = Band

    @property
    def id(self) -> str:
        """
        >>> search_results[0].id
        '125'
        """
        url = PyQuery(self._details[0])("a").attr("href")
        return re.search(r"\d+$", url).group(0)

    @property
    def url(self) -> str:
        return "bands/_/{0}".format(self.id)

    @property
    def name(self) -> str:
        """
        >>> search_results[0].name
        'Metallica'
        """
        return self[0]

    @property
    def genres(self) -> List[str]:
        """
        >>> search_results[0].genres
        ['Thrash Metal (early)', 'Hard Rock (mid)', 'Heavy/Thrash Metal (later)']
        """
        return split_genres(self[1])

    @property
    def country(self) -> str:
        """
        >>> search_results[0].country
        'United States'
        """
        return self[2]

    @property
    def other(self) -> str:
        return self[3:]


class AlbumResult(SearchResult):

    def __init__(self, details):
        super().__init__(details)
        self._details = details
        self._resultType = AlbumWrapper

    @property
    def id(self) -> str:
        url = PyQuery(self._details[1])("a").attr("href")
        return re.search(r"\d+$", url).group(0)

    @property
    def url(self) -> str:
        return "albums/_/_/{0}".format(self.id)

    @property
    def title(self) -> str:
        return self[1]

    @property
    def type(self) -> str:
        return self[2]

    @property
    def bands(self) -> List["Band"]:
        bands = []
        el = PyQuery(self._details[0]).wrap("<div></div>")
        for a in el.find("a"):
            url = PyQuery(a).attr("href")
            id = re.search(r"\d+$", url).group(0)
            bands.append(Band("bands/_/{0}".format(id)))
        return bands

    @property
    def band_name(self) -> str:
        return self[0]


class SongResult(SearchResult):

    def __init__(self, details):
        super().__init__(details)
        self._details = details
        self._resultType = None

    def get(self) -> "SongResult":
        return self

    @property
    def id(self) -> str:
        """
        >>> song.id
        '3449'
        """
        return re.search(r"(\d+)", self[5]).group(0)

    @property
    def title(self) -> str:
        return self[3]

    @property
    def type(self) -> str:
        return self[2]

    @property
    def bands(self) -> List["Band"]:
        bands = []
        el = PyQuery(self._details[0]).wrap("<div></div>")
        for a in el.find("a"):
            url = PyQuery(a).attr("href")
            id = re.search(r"\d+$", url).group(0)
            bands.append(Band("bands/_/{0}".format(id)))
        return bands

    @property
    def band_name(self) -> str:
        return self[0]

    @property
    def album(self) -> "Album":
        url = PyQuery(self._details[1]).attr("href")
        id = re.search("\d+$", url).group(0)
        return Album("albums/_/_/{0}".format(id))

    @property
    def album_name(self) -> str:
        return self[1]

    @property
    def genres(self) -> List[str]:
        """
        >>> song.genres
        ['Heavy Metal', 'NWOBHM']
        """
        genres = []
        for genre in self[4].split(" | "):
            genres.extend(split_genres(genre.strip()))
        return genres

    @property
    def lyrics(self) -> "Lyrics":
        """
        >>> str(song.lyrics).split('\\n')[0]
        'I am a man who walks alone'
        """
        return Lyrics(self.id)
