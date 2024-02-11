
from metallum.consts import BR, CR
from metallum.models.Metallum import Metallum


class Lyrics(Metallum):

    def __init__(self, id):
        super().__init__("release/ajax-view-lyrics/id/{0}".format(id))

    def __str__(self):
        lyrics = self._page("p").html()
        if not lyrics:
            return ""
        return lyrics.replace(BR * 2, "\n").replace(BR, "").replace(CR, "").strip()
