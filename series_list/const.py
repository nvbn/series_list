import os


DOWNLOAD_PATH = os.path.expanduser('~/Downloads/series')

ICON_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'series_list_icon.png')

IN_PROGRESS = 0
OK = 1
FAILED = 2

SERIES_TIMEOUT = None
SUBTITLE_TIMEOUT = 3
POSTER_TIMEOUT = 1

SETTINGS_PATH = os.path.expanduser('~/.config/series_list.json')

POSTERS_LOADER = 'IMDBPosterLoader'
SERIES_LOADER = 'EZTVLoader'
SUBTITLES_LOADER = 'SubliminalLoader'

PREVIEW_MINIMUM = 10

NORMAL = 0
NEED_PAUSE = 1
NEED_RESUME = 2

MAX_RETRY = 5

MAX_LIMIT = 50

NO_DOWNLOAD = 0
DOWNLOAD_PAUSED = 1
DOWNLOADING = 2
DOWNLOAD_FINISHED = 3

NO_PERCENT = -10

DHT_DEFAULT = True
LSD_DEFAULT = True
UPNP_DEFAULT = True
NATPMP_DEFAULT = True
