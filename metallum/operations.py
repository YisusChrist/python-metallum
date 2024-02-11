from urllib.parse import urlencode

from metallum.models import AlbumWrapper, Band
from metallum.models.Lyrics import Lyrics
from metallum.models.Results import AlbumResult, BandResult, SongResult
from metallum.models.Search import Search
from metallum.utils import map_params


def band_for_id(id: str) -> "Band":
    return Band("bands/_/{0}".format(id))


def band_search(
    name,
    strict=True,
    genre=None,
    countries=[],
    year_created_from=None,
    year_created_to=None,
    status=[],
    themes=None,
    location=None,
    label=None,
    additional_notes=None,
    page_start=0,
) -> "Search":
    """Perform an advanced band search."""
    # Create a dict from the method arguments
    params = locals()

    # Convert boolean value to integer
    params["strict"] = str(int(params["strict"]))

    # Map method arguments to their url query string counterparts
    params = map_params(
        params,
        {
            "name": "bandName",
            "strict": "exactBandMatch",
            "countries": "country[]",
            "year_created_from": "yearCreationFrom",
            "year_created_to": "yearCreationTo",
            "status": "status[]",
            "label": "bandLabelName",
            "additional_notes": "bandNotes",
            "page_start": "iDisplayStart",
        },
    )

    # Build the search URL
    url = "search/ajax-advanced/searching/bands/?" + urlencode(params, True)

    return Search(url, BandResult)


def album_for_id(id: str) -> "AlbumWrapper":
    return AlbumWrapper(url="albums/_/_/{0}".format(id))


def album_search(
    title,
    strict=True,
    band=None,
    band_strict=True,
    year_from=None,
    year_to=None,
    month_from=None,
    month_to=None,
    countries=[],
    location=None,
    label=None,
    indie_label=False,
    genre=None,
    catalog_number=None,
    identifiers=None,
    recording_info=None,
    version_description=None,
    additional_notes=None,
    types=[],
    page_start=0,
    formats=[],
) -> "Search":
    """Perform an advanced album search"""
    # Create a dict from the method arguments
    params = locals()

    # Convert boolean value to integer
    params["strict"] = str(int(params["strict"]))
    params["band_strict"] = str(int(params["band_strict"]))
    params["indie_label"] = str(int(params["indie_label"]))

    # Month values must be present if year is supplied
    if year_from and not month_from:
        params["month_from"] = "1"
    if year_to and not month_to:
        params["month_to"] = "12"

    # Map method arguments to their url query string counterparts
    params = map_params(
        params,
        {
            "title": "releaseTitle",
            "strict": "exactReleaseMatch",
            "band": "bandName",
            "band_strict": "exactBandMatch",
            "year_from": "releaseYearFrom",
            "year_to": "releaseYearTo",
            "month_from": "releaseMonthFrom",
            "month_to": "releaseMonthTo",
            "countries": "country[]",
            "label": "releaseLabelName",
            "indie_label": "indieLabel",
            "catalog_number": "releaseCatalogNumber",
            "identifiers": "releaseIdentifiers",
            "recording_info": "releaseRecordingInfo",
            "version_description": "releaseDescription",
            "additional_notes": "releaseNotes",
            "types": "releaseType[]",
            "formats": "releaseFormat[]",
            "page_start": "iDisplayStart",
        },
    )

    # Build the search URL
    url = "search/ajax-advanced/searching/albums/?" + urlencode(params, True)

    return Search(url, AlbumResult)


def song_search(
    title,
    strict=True,
    band=None,
    band_strict=True,
    release=None,
    release_strict=True,
    lyrics=None,
    genre=None,
    types=[],
    page_start=0,
) -> "Search":
    """Perform an advanced song search"""
    # Create a dict from the method arguments
    params = locals()

    # Convert boolean value to integer
    params["strict"] = str(int(params["strict"]))
    params["band_strict"] = str(int(params["band_strict"]))
    params["release_strict"] = str(int(params["release_strict"]))

    # Set genre as '*' if none is given to make sure
    # that the correct number of parameters will be returned
    if params["genre"] is None or len(params["genre"].strip()) == 0:
        params["genre"] = "*"

    # Map method arguments to their url query string counterparts
    params = map_params(
        params,
        {
            "title": "songTitle",
            "strict": "exactSongMatch",
            "band": "bandName",
            "band_strict": "exactBandMatch",
            "release": "releaseTitle",
            "release_strict": "exactReleaseMatch",
            "types": "releaseType[]",
            "page_start": "iDisplayStart",
        },
    )

    # Build the search URL
    url = "search/ajax-advanced/searching/songs/?" + urlencode(params, True)

    return Search(url, SongResult)


def lyrics_for_id(id: int) -> "Lyrics":
    return Lyrics(id)
