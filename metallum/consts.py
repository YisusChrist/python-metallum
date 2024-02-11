"""Constants used throughout the package."""

import os
import tempfile


CACHE_FILE = os.path.join(tempfile.gettempdir(), "metallum_cache")

# Site details
BASE_URL = "https://www.metal-archives.com"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36"

# HTML entities
BR = "<br/>"
CR = "&#13;"

# Timeout between page requests, in seconds
REQUEST_TIMEOUT = 1.0

# UTC offset
UTC_OFFSET = 4
