"""Lyrics model"""

from metallum.consts import BR, CR
from metallum.models.metallum import Metallum


class Lyrics(Metallum):
    """Represents a song's lyrics page"""

    def __init__(self, lyrics_id):
        super().__init__(f"release/ajax-view-lyrics/id/{lyrics_id}")

    def __str__(self):
        lyrics = self._page("p").html()
        if not lyrics:
            return ""
        return lyrics.replace(BR * 2, "\n").replace(BR, "").replace(CR, "").strip()

    def __repr__(self):
        return f"<Lyrics: {self.__str__()}>"
