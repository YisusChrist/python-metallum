"""Base class for all Metallum classes"""

import time

import requests_cache
from pyquery import PyQuery

from metallum.consts import CACHE_FILE, REQUEST_TIMEOUT
from metallum.utils import make_absolute, get_user_agent


class Metallum:
    """Base metallum class - represents a metallum page"""

    def __init__(self, url):
        self._session = requests_cache.CachedSession(cache_name=CACHE_FILE)
        self._session.hooks = {"response": self._make_throttle_hook()}
        self._session.headers = {
            # "User-Agent": get_user_agent(),
            "Accept-Encoding": "gzip",
        }

        self._content = self._fetch_page_content(url)
        self._page = PyQuery(self._content)

    def _make_throttle_hook(self):
        """
        Returns a response hook function which sleeps for `timeout` seconds if
        response is not cached
        """

        def hook(response, *args, **kwargs):
            is_cached = getattr(response, "from_cache", False)
            if not is_cached:
                time.sleep(REQUEST_TIMEOUT)
            # print("{}{}".format(response.request.url, " (CACHED)" if is_cached else ""))
            return response

        return hook

    def _fetch_page_content(self, url) -> str:
        """
        Fetch the page content

        Args:
            url: The URL of the page to fetch

        Returns:
            str: The page content
        """
        res = self._session.get(make_absolute(url))
        return res.text
