#!/usr/bin/env python
# encoding: utf-8
"""Python interface for www.metal-archives.com"""

import requests_cache
from requests_cache.core import remove_expired_responses

from metallum.consts import CACHE_FILE
from metallum.models.AlbumTypes import AlbumTypes
from metallum.operations import album_for_id, band_search

requests_cache.install_cache(cache_name=CACHE_FILE, expire_after=300)
remove_expired_responses()


if __name__ == "__main__":
    import doctest

    # Test objects
    search_results = band_search("metallica")
    band = search_results[0].get()
    album = band.albums.search(type=AlbumTypes.FULL_LENGTH)[2]
    track = album.tracks[0]

    # Objects for split album tests
    split_album = album_for_id("42682")
    split_album_track = split_album.tracks[2]

    # Objects for multi-disc album testing
    multi_disc_album = album_for_id("338756")

    doctest.testmod(globs=locals())
