"""Utility functions for the Metallum package."""

import datetime
import re
from typing import List

from metallum.consts import BASE_URL, UTC_OFFSET


def map_params(params, m):
    """
    Map parameters to their respective keys.

    Args:
        params: The parameters to map.
        m: The mapping.

    Returns:
        dict: The mapped parameters.
    """
    res = {}
    for k, v in params.items():
        if v is not None:
            res[m.get(k, k)] = v
    return res


def split_genres(s: str) -> List[str]:
    """
    Split a string of genres into a list of genres.

    Args:
        s: The string of genres.

    Returns:
        list: The list of genres.

    Examples:
        Split by comma separator:
        >>> split_genres('Thrash Metal (early), Hard Rock/Heavy/Thrash Metal (later)')
        ['Thrash Metal (early)', 'Hard Rock/Heavy/Thrash Metal (later)']

        Split by semicolon separator:
        >>> split_genres('Deathcore (early); Melodic Death/Groove Metal')
        ['Deathcore (early)', 'Melodic Death/Groove Metal']

        Handle no commas:
        >>> split_genres('Heavy Metal')
        ['Heavy Metal']

        Handle commas within parentheses:
        >>> split_genres('Heavy Metal/Hard Rock (early, later), Thrash Metal (mid)')
        ['Heavy Metal/Hard Rock (early, later)', 'Thrash Metal (mid)']
    """
    return re.split(r"(?:,|;)\s*(?![^()]*\))", s)


def make_absolute(endpoint: str) -> str:
    """
    Make relative URLs absolute

    Args:
        endpoint: The relative URL.

    Returns:
        str: The absolute URL.
    """
    return f"{BASE_URL}/{endpoint}"


def offset_time(t: datetime.datetime) -> datetime.datetime:
    """
    Convert server time to UTC

    Args:
        t: The server time.

    Returns:
        datetime.datetime: The UTC time.
    """
    td = datetime.timedelta(hours=UTC_OFFSET)
    return t + td


def parse_duration(s: str) -> int:
    """
    Parse a duration string into seconds.

    Args:
        s: The duration string.

    Returns:
        int: The duration in seconds.

    Examples:
        >>> parse_duration('00:01')
        1
        >>> parse_duration('03:33')
        213
        >>> parse_duration('01:14:00')
        4440
    """
    parts = s.split(":")
    seconds = int(parts[-1])
    if len(parts) > 1:
        seconds += int(parts[-2]) * 60
    if len(parts) == 3:
        seconds += int(parts[0]) * 3600
    return seconds
