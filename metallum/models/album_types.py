"""Enum of all possible album types"""


from enum import Enum


class AlbumTypes(Enum):
    """Enum of all possible album types"""

    FULL_LENGTH = "Full-length"
    EP = "EP"
    SINGLE = "Single"
    DEMO = "Demo"
    VIDEO = "Video/VHS"
    COMPILATION = "Compilation"
    DVD = "DVD"
    LIVE = "Live album"
    SPLIT = "Split"
