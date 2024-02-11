import datetime
import re
from typing import List, Optional

from dateutil import parser as date_parser
from pyquery import PyQuery

from metallum.models.AlbumTypes import AlbumTypes
from metallum.models.Lyrics import Lyrics
from metallum.models.Metallum import Metallum
from metallum.models.MetallumCollection import MetallumCollection
from metallum.models.MetallumEntity import MetallumEntity
from metallum.models.SimilarArtists import SimilarArtists
from metallum.utils import offset_time, parse_duration, split_genres


class TrackCollection(MetallumCollection):

    def __init__(self, url, album):
        super().__init__(url)

        disc = 1
        overall_number = 1
        rows = (
            self._page("table.table_lyrics")
            .find("tr.odd, tr.even")
            .not_(".displayNone")
        )
        for index, track in enumerate(rows):
            track = Track(rows.eq(index), album, disc, overall_number)
            if index != 0 and track.number == 1:
                disc += 1
                track._disc_number = disc
            overall_number += 1
            self.append(track)


class Band(MetallumEntity):

    def __init__(self, url):
        super().__init__(url)

    def __repr__(self):
        return "<Band: {0}>".format(self.name)

    @property
    def id(self) -> str:
        """
        >>> band.id
        '125'
        """
        url = self._page(".band_name a").attr("href")
        return re.search(r"\d+$", url).group(0)

    @property
    def url(self) -> str:
        return "bands/_/{0}".format(self.id)

    @property
    def added(self) -> Optional[datetime.datetime]:
        """
        >>> type(band.added)
        <class 'datetime.datetime'>
        """
        s = self._page("#auditTrail").find("tr").eq(1).find("td").eq(0).text()[10:]
        try:
            return offset_time(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            return None

    @property
    def modified(self) -> Optional[datetime.datetime]:
        """
        >>> type(band.modified)
        <class 'datetime.datetime'>
        """
        s = self._page("#auditTrail").find("tr").eq(1).find("td").eq(1).text()[18:]
        try:
            return offset_time(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            return None

    @property
    def name(self) -> str:
        """
        >>> band.name
        'Metallica'
        """
        return self._page("h1.band_name").text().strip()

    @property
    def country(self) -> str:
        """
        >>> band.country
        'United States'
        """
        return self._dd_text_for_label("Country of origin:")

    @property
    def location(self) -> str:
        """
        >>> band.location
        'Los Angeles/San Francisco, California'
        """
        return self._dd_text_for_label("Location:")

    @property
    def status(self) -> str:
        """
        >>> band.status
        'Active'
        """
        return self._dd_text_for_label("Status:")

    @property
    def formed_in(self) -> str:
        """
        >>> band.formed_in
        '1981'
        """
        return self._dd_text_for_label("Formed in:")

    @property
    def genres(self) -> List[str]:
        """
        >>> band.genres
        ['Thrash Metal (early)', 'Hard Rock (mid)', 'Heavy/Thrash Metal (later)']
        """
        return split_genres(self._dd_text_for_label("Genre:"))

    @property
    def themes(self) -> List[str]:
        """
        >>> band.themes
        ['Introspection', 'Anger', 'Corruption', 'Deceit', 'Death', 'Life', 'Metal', 'Literature', 'Films']
        """
        return self._dd_text_for_label("Themes:").split(", ")

    @property
    def label(self) -> str:
        """
        >>> band.label
        'Blackened Recordings'
        """
        return self._dd_text_for_label("Current label:")

    @property
    def logo(self) -> Optional[str]:
        """
        >>> band.logo
        'https://www.metal-archives.com/images/1/2/5/125_logo.png'
        """
        url = self._page("#logo").attr("href")
        if not url:
            return None
        return url.split("?")[0]

    @property
    def photo(self) -> Optional[str]:
        """
        >>> band.photo
        'https://www.metal-archives.com/images/1/2/5/125_photo.jpg'
        """
        url = self._page("#photo").attr("href")
        if not url:
            return None
        return url.split("?")[0]

    @property
    def albums(self) -> List["AlbumCollection"]:
        """
        >>> len(band.albums) > 0
        True

        >>> type(band.albums[0])
        <class '__main__.AlbumWrapper'>
        """
        url = "band/discography/id/{0}/tab/all".format(self.id)
        return AlbumCollection(url)

    @property
    def similar_artists(self) -> "SimilarArtists":
        """
                >>> band.similar_artists
        <SimilarArtists: Megadeth (488) | Testament (420) | Exodus (212) | Evile (206) | Anthrax (182) | Death Angel (148) | Diamond Head (119) | Xentrix (115) | Annihilator (111) | Newsted (108) | Metal Church (105) | Heathen (105) | Flotsam and Jetsam (104) | Slayer (71) | Trivium (70) | Overkill (66) | Artillery (58) | Mortal Sin (58) | Volbeat (55) | Sacred Reich (48) | Paradox (44) | Slammer (34) | Pantera (33) | Corrosion of Conformity (30) | Am I Blood (30) | Alice in Chains (25) | Stone (25) | Motörhead (21) | Dark Angel (20) | Vio-lence (20) | Meliah Rage (19) | Machine Head (18) | Onslaught (18) | Tantara (18) | Kreator (17) | Outrage (17) | Blitzkrieg (16) | Znöwhite (16) | Forbidden (15) | Suicidal Tendencies (15) | Cyclone Temple (15) | Whiplash (15) | Havok (14) | Defiance (14) | Accu§er (13) | Deliverance (13) | Lȧȧz Rockit (13) | Reign of Fury (13) | Woslom (13) | Kat (12) | Iced Earth (12) | 4Arm (12) | Acrassicauda (11) | Wrathchild America (11) | Sepultura (11) | Power Trip (11) | Apocalypse (11) | Ellefson (11) | Metal Allegiance (11) | Alcoholica (11) | Wildhunt (11) | Mercyful Fate (10) | Железный Поток (10) | Destruction (10) | Sufosia (10) | Nuclear Assault (9) | Tourniquet (9) | Shah (9) | Faith No More (8) | Channel Zero (8) | Mantic Ritual (8) | Dust Bolt (8) | Hammerhedd (8) | Eradikator (8) | Ramp (8) | Earthquake (8) | Anesthesia (8) | Inciter (8) | Hirax (7) | Shadows Fall (7) | Faith or Fear (7) | Game Over (7) | Holocaust (7) | Sweet Savage (7) | Blackened (7) | Morgana Lefay (7) | Hellraiser (7) | Razor (7) | Posehn (7) | Eternal Decision (6) | Armored Saint (6) | Austrian Death Machine (6) | Hatriot (6) | Vindicator (6) | Dublin Death Patrol (6) | Sylosis (6) | Angelus Apatrida (6) | Addictive (6) | Hunter (6) | Meshiaak (6) | Vader (6) | Living Sacrifice (6) | Thrashback (6) | Venom Inc. (6) | Athena (6) | Prong (5) | Danzig (5) | Thrashsteel (5) | Fallen Angel (5) | Lost Society (5) | Ekhymosis (5) | Attomica (5) | Raven (5) | In.Si.Dia (5) | Turbo (5) | Act of Defiance (5) | Hellripper (5) | Suicidal Angels (5) | Phantom Lord (5) | Sanctity (5) | Wargasm (5) | Seducer (5) | Calipash (5) | Detritus (5) | Enforcer (5) | Mason (5) | Tyrant's Reign (5) | Braindamage (5) | Vortex (5) | Abandoned (5) | Arbitrater (5) | Bleak House (5) | Metallic Ass (5) | Modifidious (5) | Apocalyptica (4) | The Worshyp (4) | Airdash (4) | Mezzrow (4) | White Zombie (4) | DBC (4) | Diamond Plate (4) | Equinox (4) | Excel (4) | Acrophet (4) | Black Track (4) | Panic (4) | Adamantine (4) | Critical Solution (4) | Perzonal War (4) | Phantasm (4) | Shredhead (4) | Steel Fury (4) | Alexander Palitsin (4) | I.N.C. (4) | Wrath (4) | Fight (4) | Kazjurol (4) | King Diamond (4) | Manditory (4) | Allegiance (4) | Altitudes & Attitude (4) | Dead On (4) | Fallout (4) | Hermética (4) | Lethal (4) | Tonic Breed (4) | Wiplash (4) | Animator (4) | Astharoth (4) | Disciples of Power (4) | Extrema (4) | Face of Anger (4) | Fatality (4) | Insecurity (4) | Nasty Savage (4) | Pentagram (4) | Potential Threat (4) | Prophecy (4) | Algebra (4) | Criminal (4) | Nuclear Simphony (4) | Oil (4) | Planleft (4) | Practice to Deceive (4) | Razgate (4) | Revtend (4) | Ritual Servant (4) | Space Chaser (4) | Stormdeath (4) | Teronation (4) | Victim (4) | Vingador (4) | Vulture (4) | Legion (4) | Flacmans Port (4) | Four Noses (4) | Half-Lit (4) | Sabbat (3) | Ancesttral (3) | Target (3) | Симфония Разрушения (3) | Piranha (3) | Hatrix (3) | Souls at Zero (3) | Toranaga (3) | Bitter End (3) | Demolition Train (3) | Killers (3) | Legion (3) | Rhythm of Fear (3) | Sacrifice (3) | Wolfpack Unleashed (3) | Anihilated (3) | Dethrone (3) | Viking (3) | Acridity (3) | Dissolved (3) | Dogma (3) | Exciter (3) | Forced Entry (3) | Nihilist (3) | Quorthon (3) | Taurus (3) | Yosh (3) | Abaxial (3) | Battalion (3) | Disaster Area (3) | Hate FX (3) | Horcas (3) | LawShed (3) | Prowler (3) | Strip Mind (3) | The Force (3) | Glenn Tipton (3) | Next (3) | Against (3) | Deliverance (3) | Hatchet (3) | HI-GH (3) | In Malice's Wake (3) | King Gizzard & the Lizard Wizard (3) | Stone Vengeance (3) | Terror Empire (3) | Thrash Bombz (3) | Thresher (3) | Aleister (3) | Alpha Warhead (3) | Amboog-a-Lard (3) | Anesthesia (3) | Blatant Disarray (3) | Chronical Disturbance (3) | Coldsteel (3) | Cro-Mags (3) | Crossbones (3) | Darkness (3) | DesExult (3) | Disturbed (3) | Drünkards (3) | E.S.T. (3) | Eradicator (3) | F5 (3) | Fierce Allegiance (3) | Filter (3) | Hostile Rage (3) | Incursion Dementa (3) | Jesus Freaks (3) | Metalord (3) | Mystrez (3) | Necrosis (3) | Night Viper (3) | Nightfyre (3) | Serpentor (3) | Total Annihilation (3) | Violator (3)>
        """

        url = "band/ajax-recommendations/id/" + self.id + "/showMoreSimilar/1"
        return SimilarArtists(url, SimilarArtistsResult)


class Track(object):

    def __init__(self, elem, album, disc_number, overall_number):
        self._elem = elem
        self.album = album
        self._disc_number = disc_number
        self._overall_number = overall_number

    def __repr__(self):
        return "<Track: {0} ({1})>".format(self.title, self.duration)

    @property
    def id(self) -> str:
        """
        >>> track.id
        '5018A'
        """
        return self._elem("td").eq(0)("a").attr("name")

    @property
    def number(self) -> int:
        """
        >>> track.number
        1

        >>> multi_disc_album.tracks[0].number
        1

        >>> multi_disc_album.tracks[-1].number
        4
        """
        return int(self._elem("td").eq(0).text()[:-1])

    @property
    def overall_number(self) -> int:
        """
        >>> track.overall_number
        1

        >>> multi_disc_album.tracks[0].overall_number
        1

        >>> multi_disc_album.tracks[-1].overall_number
        8
        """
        return self._overall_number

    @property
    def disc_number(self) -> int:
        """
        >>> track.disc_number
        1

        >>> multi_disc_album.tracks[0].disc_number
        1

        >>> multi_disc_album.tracks[-1].disc_number
        2
        """
        return self._disc_number

    @property
    def full_title(self) -> str:
        """
        >>> track.full_title
        'Battery'

        >>> split_album_track.full_title
        'Lunar Aurora - A haudiga Fluag'
        """
        return self._elem("td").eq(1).text().replace("\n", "").replace("\t", "")

    @property
    def title(self) -> str:
        """
        >>> track.title
        'Battery'

        >>> split_album_track.title
        'A haudiga Fluag'
        """
        title = self.full_title
        # Remove band name from split album track titles
        if self.album.type == AlbumTypes.SPLIT:
            title = title[len(self.band.name) + 3 :]
        return title

    @property
    def duration(self) -> int:
        """
        >>> track.duration
        313
        """
        s = self._elem("td").eq(2).text()
        if s:
            seconds = parse_duration(s)
        else:
            seconds = 0
        return seconds

    @property
    def band(self) -> Band:
        """
        >>> track.band
        <Band: Metallica>

        >>> split_album_track.band
        <Band: Lunar Aurora>
        """
        if self.album.type == AlbumTypes.SPLIT:
            for band in self.album.bands:
                if self.full_title.startswith(band.name):
                    break
        else:
            band = self.album.bands[0]
        return band

    @property
    def lyrics(self) -> "Lyrics":
        """
        >>> str(track.lyrics).split('\\n')[0]
        'Lashing out the action, returning the reaction'
        """
        return Lyrics(self.id)


class Album(MetallumEntity):

    def __init__(self, url):
        super().__init__(url)

    def __repr__(self):
        return "<Album: {0}>".format(self.title)

    @property
    def id(self) -> str:
        """
        >>> album.id
        '547'
        """
        url = self._page(".album_name a").attr("href")
        return re.search(r"\d+$", url).group(0)

    @property
    def url(self) -> str:
        return "albums/_/_/{0}".format(self.id)

    @property
    def bands(self) -> List[Band]:
        """Return a list of band objects. The list will only contain
        multiple bands when the album is of type 'Split'.

        >>> album.bands
        [<Band: Metallica>]

        >>> split_album.bands
        [<Band: Lunar Aurora>, <Band: Paysage d'Hiver>]
        """
        bands = []
        for a in self._page(".band_name").find("a"):
            url = PyQuery(a).attr("href")
            id = re.search(r"\d+$", url).group(0)
            bands.append(Band("bands/_/{0}".format(id)))
        return bands

    @property
    def added(self) -> Optional[datetime.datetime]:
        """
        >>> type(album.added)
        <class 'NoneType'>
        """
        s = self._page("#auditTrail").find("tr").eq(1).find("td").eq(0).text()[10:]
        try:
            return offset_time(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            return None

    @property
    def modified(self) -> Optional[datetime.datetime]:
        """
        >>> type(album.modified)
        <class 'datetime.datetime'>
        """
        s = self._page("#auditTrail").find("tr").eq(1).find("td").eq(1).text()[18:]
        try:
            return offset_time(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S"))
        except ValueError:
            return None

    @property
    def title(self) -> str:
        """
        >>> album.title
        'Master of Puppets'
        """
        return self._page("h1.album_name a").text()

    @property
    def type(self) -> str:
        """
        >>> album.type
        'Full-length'
        """
        element = self._dd_element_for_label("Type:")
        return element.text() if element else ""

    @property
    def duration(self) -> int:
        """
        >>> album.duration
        3290
        """
        s = self._page("table.table_lyrics td strong").text()
        if s:
            return parse_duration(s)
        else:
            return 0

    @property
    def date(self) -> Optional[datetime.datetime]:
        """
        >>> album.date
        datetime.datetime(1986, 3, 3, 0, 0)
        """
        s = self._dd_text_for_label("Release date:")

        # Date has no day portion
        if len(s) > 4 and "," not in s:
            date = datetime.datetime.strptime(s, "%B %Y")
        else:
            date = date_parser.parse(s)
        return date

    @property
    def year(self) -> int:
        """
        >>> album.year
        1986
        """
        return int(self.date.year)

    @property
    def label(self) -> str:
        """
        >>> album.label
        'Elektra Records'

        >>> multi_disc_album.label
        'Osmose Productions'
        """
        element = self._dd_element_for_label("Label:")
        return element("a").text() if element else ""

    def _review_element(self) -> Optional[PyQuery]:
        return self._dd_element_for_label("Reviews:")

    @property
    def score(self) -> Optional[int]:
        """
        >>> album.score
        79

        >>> split_album.score
        94

        >>> multi_disc_album.score
        97
        """
        element = self._review_element()
        if not element:
            return None

        score = re.search(r"(\d{1,3})%", element.text())
        if not score:
            return None

        return int(score.group(1))

    @property
    def review_count(self) -> Optional[int]:
        """
        >>> album.review_count
        39

        >>> split_album.review_count
        1

        >>> multi_disc_album.review_count
        4
        """
        element = self._review_element()
        if not element:
            return None

        count = re.search(r"(\d+)", element.text())
        if not count:
            return None

        return int(count.group(1))

    @property
    def cover(self) -> Optional[str]:
        """
        >>> album.cover
        'https://www.metal-archives.com/images/5/4/7/547.jpg'
        """
        url = self._page("#cover").attr("href")
        if not url:
            return None
        return url.split("?")[0]


class AlbumCollection(MetallumCollection):

    def __init__(self, url):
        super().__init__(url)

        rows = self._page("tr:gt(0)")
        for index in range(len(rows)):
            self.append(AlbumWrapper(elem=rows.eq(index)))


class AlbumWrapper(Metallum):
    """Wrapper class for Album / LazyAlbum

    Album instances are created automatically when an attribute is accessed that
    is not provided by LazyAlbum:

    >>> a = band.albums[1]
    >>> a.label
    'Megaforce Records'

    The above causes an Album instance to be created (requires an extra page request!):

    >>> type(a._album)
    <class '__main__.Album'>
    """

    def __init__(self, url=None, elem=None):
        if url:
            super().__init__(url)
            self._album = Album(url)
        elif elem:
            self._album = LazyAlbum(elem)

    def __repr__(self):
        return "<Album: {0} ({1})>".format(self.title, self.type)

    def __getattr__(self, name):
        if not hasattr(self._album, name) and hasattr(Album, name):
            self._album = Album(self._album.url)
        return getattr(self._album, name)

    @property
    def tracks(self):
        """
        >>> len(album.tracks)
        8
        """
        return TrackCollection(self._album.url, self)

    @property
    def disc_count(self):
        """
        >>> album.disc_count
        1

        >>> multi_disc_album.disc_count
        2
        """
        discs = 0
        for track in self.tracks:
            if track.disc_number > discs:
                discs = track.disc_number
        return discs


class LazyAlbum:

    def __init__(self, elem):
        self._elem = elem

    @property
    def id(self) -> str:
        """
        >>> album.id
        '547'
        """
        url = self._elem("td").eq(0)("a").attr("href")
        return re.search(r"\d+$", url).group(0)

    @property
    def url(self) -> str:
        return "albums/_/_/{0}".format(self.id)

    @property
    def title(self) -> str:
        """
        >>> album.title
        'Master of Puppets'
        """
        return self._elem("td").eq(0)("a").text()

    @property
    def type(self) -> str:
        """
        >>> album.type
        'Full-length'
        """
        return self._elem("td").eq(1).text()

    @property
    def year(self) -> int:
        """
        >>> album.year
        1986
        """
        return int(self._elem("td").eq(2).text())


class SimilarArtistsResult(list):
    """Represents a entry in the similar artists tab"""

    _resultType = Band

    def __init__(self, details):
        super().__init__()
        self._details = details
        for d in details:
            self.append(d)

    @property
    def id(self) -> str:
        # url = PyQuery(self._details[0])('a').attr('href')
        return re.search(r"\d+$", self[0]).group(0)

    @property
    def url(self) -> str:
        return "bands/_/{0}".format(self.id)

    @property
    def name(self) -> str:
        return self[1]

    @property
    def country(self) -> str:
        """
        >>> search_results[0].country
        'United States'
        """
        return self[2]

    @property
    def genres(self) -> List[str]:
        return split_genres(self[3])

    @property
    def score(self) -> int:
        return int(self[4])

    def __repr__(self):
        s = " | ".join(self[1:])
        return "<SimilarArtist: {0}>".format(s)

    def get(self) -> "Metallum":
        return self._resultType(self.url)
