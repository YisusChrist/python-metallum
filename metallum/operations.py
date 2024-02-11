"""Operations module for the Metallum API."""

from urllib.parse import urlencode

from metallum.models import AlbumWrapper, Band
from metallum.models.lyrics import Lyrics
from metallum.models.results import AlbumResult, BandResult, SongResult
from metallum.models.search import Search
from metallum.utils import map_params


def band_for_id(band_id: str) -> "Band":
    """
    Get a band by its ID.

    Args:
        band_id: The band's ID.

    Returns:
        Band: The band with the given ID.
    """
    return Band(f"bands/_/{band_id}")


def band_search(
    name,
    strict=True,
    genre=None,
    countries=None,
    year_created_from=None,
    year_created_to=None,
    status=None,
    themes=None,
    location=None,
    label=None,
    additional_notes=None,
    page_start=0,
) -> "Search":
    """
    Perform an advanced band search.

    Args:
        name: The band's name.
        strict: Whether the search should be strict.
        genre: The band's genre.
        countries: The band's countries.
        year_created_from: The year the band was created from.
        year_created_to: The year the band was created to.
        status: The band's status.
        themes: The band's themes.
        location: The band's location.
        label: The band's label.
        additional_notes: Additional notes about the band.
        page_start: The page to start the search from.

    Returns:
        Search: The search results.
    """
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


def album_for_id(album_id: str) -> "AlbumWrapper":
    """
    Get an album by its ID.

    Args:
        album_id: The album's ID.

    Returns:
        AlbumWrapper: The album with the given ID.
    """
    return AlbumWrapper(url=f"albums/_/_/{album_id}")


def album_search(
    title,
    strict=True,
    band=None,
    band_strict=True,
    year_from=None,
    year_to=None,
    month_from=None,
    month_to=None,
    countries=None,
    location=None,
    label=None,
    indie_label=False,
    genre=None,
    catalog_number=None,
    identifiers=None,
    recording_info=None,
    version_description=None,
    additional_notes=None,
    types=None,
    page_start=0,
    formats=None,
) -> "Search":
    """
    Perform an advanced album search

    Args:
        title: The album's title.
        strict: Whether the search should be strict.
        band: The album's band.
        band_strict: Whether the band search should be strict.
        year_from: The year the album was released from.
        year_to: The year the album was released to.
        month_from: The month the album was released from.
        month_to: The month the album was released to.
        countries: The album's countries.
        location: The album's location.
        label: The album's label.
        indie_label: Whether the label is an indie label.
        genre: The album's genre.
        catalog_number: The album's catalog number.
        identifiers: The album's identifiers.
        recording_info: The album's recording info.
        version_description: The album's version description.
        additional_notes: Additional notes about the album.
        types: The album's types.
        page_start: The page to start the search from.
        formats: The album's formats.

    Returns:
        Search: The search results.
    """
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
    types=None,
    page_start=0,
) -> "Search":
    """
    Perform an advanced song search

    Args:
        title: The song's title.
        strict: Whether the search should be strict.
        band: The song's band.
        band_strict: Whether the band search should be strict.
        release: The song's release.
        release_strict: Whether the release search should be strict.
        lyrics: The song's lyrics.
        genre: The song's genre.
        types: The song's types.
        page_start: The page to start the search from.

    Returns:
        Search: The search results.
    """
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


def lyrics_for_id(lyrics_id: int) -> "Lyrics":
    """
    Get lyrics by their ID.

    Args:
        id: The lyrics' ID.

    Returns:
        Lyrics: The lyrics with the given ID.
    """
    return Lyrics(lyrics_id)
