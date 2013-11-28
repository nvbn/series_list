import os


DOWNLOAD_PATH = os.path.expanduser('~/Downloads/series')

ICON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'series_list_icon.png')

IN_PROGRESS = 0
OK = 1
FAILED = 2

SERIES_TIMEOUT = 0
SUBTITLE_TIMEOUT = 3
POSTER_TIMEOUT = 1
