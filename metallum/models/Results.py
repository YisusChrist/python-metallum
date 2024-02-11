"""Results from a search on Metal Archives"""

import re
from typing import List

from pyquery import PyQuery

from metallum.models import Album, AlbumWrapper, Band, _get_bands_list
from metallum.models.lyrics import Lyrics
from metallum.models.metallum import Metallum
from metallum.utils import split_genres


class SearchResult(list):
    """
    Represents a search result in an advanced search

    Attributes:
        _resultType: The type of the result
    """

    _resultType = None

    def __init__(self, details):
        super().__init__()
        for detail in details:
            if re.match("^<a href.*", detail):
                lyrics_link = re.search(r'id="lyricsLink_(\d+)"', detail)
                if lyrics_link is not None:
                    self.append(lyrics_link[1])
                else:
                    d = PyQuery(detail)
                    self.append(d("a").text())
            else:
                self.append(detail)

    def __repr__(self):
        s = " | ".join(self)
        return f"<SearchResult: {s}>"

    def get(self) -> "Metallum":
        """Return the result as a Metallum object"""
        # ! E1102: self._resultType is not callable (not-callable)
        # ! E1101: Instance of 'SearchResult' has no 'url' member (no-member)
        return self._resultType(self.url)


class BandResult(SearchResult):
    """Represents a band search result"""

    def __init__(self, details):
        super().__init__(details)
        self._details = details
        self._resultType = Band

    @property
    def id(self) -> str:
        """
        ID of the band

        Examples:
            >>> search_results[0].id
            '125'
        """
        url = PyQuery(self._details[0])("a").attr("href")
        return re.search(r"\d+$", url).group(0)

    @property
    def url(self) -> str:
        """
        URL of the band

        Examples:
            >>> search_results[0].url
            'bands/_/125'
        """
        return f"bands/_/{self.id}"

    @property
    def name(self) -> str:
        """
        Name of the band

        Examples:
            >>> search_results[0].name
            'Metallica'
        """
        return self[0]

    @property
    def genres(self) -> List[str]:
        """
        Genres of the band

        Examples:
            >>> search_results[0].genres
            ['Thrash Metal (early)', 'Hard Rock (mid)', 'Heavy/Thrash Metal (later)']
        """
        return split_genres(self[1])

    @property
    def country(self) -> str:
        """
        Country of the band

        Examples:
            >>> search_results[0].country
            'United States'
        """
        return self[2]

    @property
    def other(self) -> str:
        """
        Other information about the band

        Examples:
            >>> search_results[0].other
            'Active since: 1981'
        """
        return self[3:]


class AlbumResult(SearchResult):
    """Represents an album search result"""

    def __init__(self, details):
        super().__init__(details)
        self._details = details
        self._resultType = AlbumWrapper

    @property
    def id(self) -> str:
        """
        ID of the album

        Examples:
            >>> album.id
            '1'
        """
        url = PyQuery(self._details[1])("a").attr("href")
        return re.search(r"\d+$", url).group(0)

    @property
    def url(self) -> str:
        """
        URL of the album

        Examples:
            >>> album.url
            'albums/_/_/1'
        """
        return f"albums/_/_/{self.id}"

    @property
    def title(self) -> str:
        """
        Title of the album

        Examples:
            >>> album.title
            'Tuonela'
        """
        return self[1]

    @property
    def type(self) -> str:
        """
        Type of the album

        Examples:
            >>> album.type
            'Full-length'
        """
        return self[2]

    @property
    def bands(self) -> List["Band"]:
        """
        List of bands that released the album

        Examples:
            >>> album.bands
            [Amorphis]
        """
        page = PyQuery(self._details[0]).wrap("<div></div>")
        return _get_bands_list(page)

    @property
    def band_name(self) -> str:
        """
        Name of the band that released the album

        Examples:
            >>> album.band_name
            'Amorphis'
        """
        return self[0]


class SongResult(SearchResult):
    """Represents a song search result"""

    def __init__(self, details):
        super().__init__(details)
        self._details = details
        self._resultType = None

    def get(self) -> "SongResult":
        """Return the result as a SongResult object"""
        return self

    @property
    def id(self) -> str:
        """
        ID of the song

        Examples:
            >>> song.id
            '3449'
        """
        return re.search(r"(\d+)", self[5]).group(0)

    @property
    def title(self) -> str:
        """
        Title of the song

        Examples:
            >>> song.title
            'Fear of the Dark'
        """
        return self[3]

    @property
    def type(self) -> str:
        """
        Type of the song

        Examples:
            >>> song.type
            'Single'
        """
        return self[2]

    @property
    def bands(self) -> List["Band"]:
        """
        List of bands that released the song

        Examples:
            >>> song.bands
            [Iron Maiden]
        """
        page = PyQuery(self._details[0]).wrap("<div></div>")
        return _get_bands_list(page)

    @property
    def band_name(self) -> str:
        """
        Name of the band that released the song

        Examples:
            >>> song.band_name
            'Iron Maiden'
        """
        return self[0]

    @property
    def album(self) -> "Album":
        """
        Album the song is from

        Examples:
            >>> song.album
            <Album: albums/_/_/1>
        """
        url = PyQuery(self._details[1]).attr("href")
        album_id = re.search(r"\d+$", url).group(0)
        return Album(f"albums/_/_/{album_id}")

    @property
    def album_name(self) -> str:
        """
        Name of the album the song is from

        Examples:
            >>> song.album_name
            'Fear of the Dark'
        """
        return self[1]

    @property
    def genres(self) -> List[str]:
        """
        Genres of the song

        Examples:
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
        Lyrics of the song

        Examples:
            >>> str(song.lyrics).split('\\n')[0]
            'I am a man who walks alone'
        """
        return Lyrics(self.id)
