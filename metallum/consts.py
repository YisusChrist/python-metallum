"""Constants used throughout the package."""

import os
import tempfile


CACHE_FILE = os.path.join(tempfile.gettempdir(), "metallum_cache")

# Site details
BASE_URL = "https://www.metal-archives.com"

# HTML entities
BR = "<br/>"
CR = "&#13;"

# Timeout between page requests, in seconds
REQUEST_TIMEOUT = 1.0

# UTC offset
UTC_OFFSET = 4
